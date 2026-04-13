from app.controllers.rol_controller import RolController
from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from app.decorators.rol_access import rol_access

roles = Blueprint('roles', __name__, url_prefix='/roles')

@roles.route('/')
@jwt_required()
def get_all():
    return RolController.get_all()

@roles.route('/<int:id>')
@jwt_required()
def show(id):
    return RolController.show(id)

@roles.route("/", methods=['POST'])
@jwt_required()
@rol_access(['admin'])
def create():
    return RolController.create(request.get_json())

@roles.route("/<int:id>", methods=['PUT'])
@jwt_required()
@rol_access(['admin'])
def update(id):
    return  RolController.update(request=request.get_json(), id=id)
    

@roles.route("/<int:id>", methods=['DELETE'])
@jwt_required()
@rol_access(['admin'])
def destroy(id):
    return RolController.destroy(id)
