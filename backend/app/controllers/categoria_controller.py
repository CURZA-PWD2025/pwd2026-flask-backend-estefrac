from sqlalchemy.exc import IntegrityError
from app.models.categoria import Categoria
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller

class CategoriaController (Controller):

    @staticmethod
    def get_all() -> tuple[Response, int]:
        categorias_list = db.session.execute(db.select(Categoria).order_by(db.desc(Categoria.id))).scalars().all()
        if len(categorias_list) > 0:
            categorias_to_dict = [categoria.to_dict() for categoria in categorias_list ]
            return jsonify(categorias_to_dict), 200 
        return jsonify({"message": 'datos no encontrados'}), 404

    @staticmethod
    def show(id)->tuple[Response, int]:
        categoria = db.session.get(Categoria, id)
        if categoria:
            return jsonify(categoria.to_dict()), 200
        return jsonify({"message": 'categoria no encontrada'}), 404

    @staticmethod
    def create(request) -> tuple[Response, int]:
        nombre:str = request.get('nombre')
        descripcion:str | None = request.get('descripcion')

        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'

        if error is None:
            try:
                categoria = Categoria(nombre=nombre, descripcion=descripcion)
                db.session.add(categoria)
                db.session.commit()
                return jsonify({'message': "categoria creada con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "categoria ya registrada"}), 409
        return jsonify ({'message': error}), 422

    @staticmethod
    def update(request, id)->tuple[Response, int]:
        nombre:str | None = request.get('nombre')
        descripcion:str | None = request.get('descripcion')
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'

        if error is None:
            categoria = db.session.get(Categoria, id)
            if categoria:
                try:
                    categoria.nombre = nombre
                    categoria.descripcion = descripcion
                    db.session.commit()
                    return jsonify({'message':'categoria modificada con exito'}), 200
                except IntegrityError:
                    error = 'el nombre ya existen' 
                    return jsonify({'message':error}), 409
            else:
                error = 'categoria no encontrada'

        return jsonify({'message':error}), 404

    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        categoria = db.session.get(Categoria, id)
        
        if not categoria:
            return jsonify({'message': 'categoria no encontrada'}), 404
        if categoria.productos:
            return jsonify({'message': 'No se puede eliminar la categoria porque tiene productos asociados'}), 409
        db.session.delete(categoria)
        db.session.commit()
        return jsonify({'message':'categoria eliminada con exito'}), 200
