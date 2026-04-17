from app.models.movimiento_stock import MovimientoStock
from app.models.producto import Producto
from app.models import db
from flask import Response, jsonify
from flask_jwt_extended import get_jwt_identity

class MovimientoStockController ():

    @staticmethod
    def get_all() -> tuple[Response, int]:
        movimientos_list = db.session.execute(db.select(MovimientoStock).order_by(db.desc(MovimientoStock.id))).scalars().all()
        if len(movimientos_list) > 0:
            movimientos_to_dict = [movimiento.to_dict() for movimiento in movimientos_list ]
            return jsonify(movimientos_to_dict), 200
        return jsonify({"message": 'Sin movimientos'}), 404
    
    @staticmethod
    def get_me() -> tuple[Response, int]:
        user_id = get_jwt_identity()
        movimientos_list = db.session.execute(db.select(MovimientoStock).filter_by(user_id=user_id).order_by(db.desc(MovimientoStock.id))).scalars().all()
        if len(movimientos_list) > 0:
            movimientos_to_dict = [movimiento.to_dict() for movimiento in movimientos_list ]
            return jsonify(movimientos_to_dict), 200
        return jsonify({"message": 'Sin movimientos'}), 404

    @staticmethod
    def create(request) -> tuple[Response, int]:
        tipo:str | None = request.get('tipo')
        cantidad:int | None = request.get('cantidad')
        motivo:str | None = request.get('motivo')
        producto_id:int | None = request.get('producto_id')
        user_id = get_jwt_identity()

        error :str | None = None

        if tipo is None:
            error = 'El tipo es requerido'
        if cantidad is None:
            error = 'La cantidad es requerida'
        if producto_id is None:
            error = 'El producto es requerido'
        if tipo not in ['entrada', 'salida']:
            error = 'El tipo debe ser "entrada" o "salida"'
        if cantidad is not None and cantidad <= 0:
            error = 'La cantidad debe ser un número positivo'

        if error is None:

            producto = db.session.get(Producto, producto_id)
            if producto is None:
                return jsonify({'message': "Producto no encontrado"}), 404
            if tipo == 'entrada':
                producto.stock_actual += cantidad or 0
            if tipo == 'salida':
                if producto.stock_actual < (cantidad or 0):
                    return jsonify({'message': "Stock insuficiente para registrar salida"}), 400
                producto.stock_actual -= cantidad or 0

            movimiento = MovimientoStock(tipo=tipo, cantidad=cantidad, motivo=motivo, producto_id=producto_id, user_id=user_id)
            db.session.add(movimiento)
            db.session.commit()
            return jsonify({'message': "Movimiento registrado con exito"}), 201
        return jsonify ({'message': error}), 422
