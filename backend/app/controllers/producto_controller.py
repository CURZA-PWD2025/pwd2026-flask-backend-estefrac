from sqlalchemy.exc import IntegrityError
from app.models.categoria import Categoria
from app.models.producto import Producto
from app.models.proveedor import Proveedor
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller

class ProductoController (Controller):

    @staticmethod
    def get_all() -> tuple[Response, int]:
        producto_list = db.session.execute(db.select(Producto).order_by(db.desc(Producto.id))).scalars().all()
        if len(producto_list) > 0:
            producto_to_dict = [producto.to_dict() for producto in producto_list ]
            return jsonify(producto_to_dict), 200
        return jsonify({"message": 'datos no encontrados'}), 404

    @staticmethod
    def show(id)->tuple[Response, int]:
        producto = db.session.get(Producto, id)
        if producto:
            return jsonify(producto.to_dict()), 200
        return jsonify({"message": 'producto no encontrado'}), 404

    @staticmethod
    def create(request) -> tuple[Response, int]:
        nombre:str | None = request.get('nombre')
        descripcion:str | None = request.get('descripcion')
        precio_costo:float | None = request.get('precio_costo')
        precio_venta:float | None = request.get('precio_venta')
        stock_actual:int | None = request.get('stock_actual')
        stock_minimo:int | None = request.get('stock_minimo')
        categoria_id:int | None = request.get('categoria_id')
        proveedor_id:int | None = request.get('proveedor_id')

        error :str | None = None

        if nombre is None:
            error = 'El nombre es requerido'
        if precio_costo is None:
            error = 'El precio de costo es requerido'
        if precio_venta is None:
            error = 'El precio de venta es requerido'
        if categoria_id is None:
            error = 'La categoria es requerida'
        if categoria_id is not None:
            categoria = db.session.get(Categoria, categoria_id)
            if categoria is None:
                error = 'La categoria no existe'
        if proveedor_id is not None:
            proveedor = db.session.get(Proveedor, proveedor_id)
            if proveedor is None:
                error = 'El proveedor no existe'

        if error is None:
            try:
                producto = Producto(nombre=nombre, descripcion=descripcion, precio_costo=precio_costo, precio_venta=precio_venta, stock_actual=stock_actual or 0, stock_minimo=stock_minimo or 0, categoria_id=categoria_id, proveedor_id=proveedor_id)
                db.session.add(producto)
                db.session.commit()
                return jsonify({'message': "producto creado con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "producto ya registrado"}), 409
        return jsonify ({'message': error}), 422
    
    @staticmethod
    def update(request, id)->tuple[Response, int]:
        nombre:str | None = request.get('nombre')
        descripcion:str | None = request.get('descripcion')
        precio_costo:float | None = request.get('precio_costo')
        precio_venta:float | None = request.get('precio_venta')
        stock_actual:int | None = request.get('stock_actual')
        stock_minimo:int | None = request.get('stock_minimo')
        categoria_id:int | None= request.get('categoria_id')
        proveedor_id:int | None = request.get('proveedor_id')
        
        error :str | None = None

        if nombre is None:
            error = 'El nombre es requerido'
        if precio_costo is None:
            error = 'El precio de costo es requerido'
        if precio_venta is None:
            error = 'El precio de venta es requerido'
        if categoria_id is None:
            error = 'La categoria es requerida'
        if categoria_id is not None:
            categoria = db.session.get(Categoria, categoria_id)
            if categoria is None:
                error = 'La categoria no existe'
        if proveedor_id is not None:
            proveedor = db.session.get(Proveedor, proveedor_id)
            if proveedor is None:
                error = 'El proveedor no existe'

        if error is None:
            producto = db.session.get(Producto, id)
            if producto:
                try:
                    producto.nombre = nombre
                    producto.descripcion = descripcion
                    producto.precio_costo = precio_costo
                    producto.precio_venta = precio_venta
                    producto.stock_actual = stock_actual or 0
                    producto.stock_minimo = stock_minimo or 0
                    producto.categoria_id = categoria_id
                    producto.proveedor_id = proveedor_id
                    db.session.commit()
                    return jsonify({'message':'producto modificado con exito'}), 200
                except IntegrityError:
                    error = 'el nombre ya existen' 
                    return jsonify({'message':error}), 409
            return jsonify({"message": 'producto no encontrado'}), 404
        return jsonify({'message':error}), 422

    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        producto = db.session.get(Producto, id)
        if not producto:
            return jsonify({'message': 'producto no encontrado'}), 404
        if producto.movimientos_stock:
            return jsonify({'message': 'No se puede eliminar el producto porque tiene movimientos de stock asociados'}), 409
        db.session.delete(producto)
        db.session.commit()
        return jsonify({'message': 'producto eliminado con exito'}), 200


