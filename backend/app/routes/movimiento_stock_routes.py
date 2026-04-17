from app.controllers.movimiento_stock_controller import MovimientoStockController
from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from app.decorators.rol_access import rol_access

movimientos_stock = Blueprint('movimientos', __name__, url_prefix='/movimientos')

@movimientos_stock.route('/')
@jwt_required()
@rol_access(['admin'])
def get_all():
    return MovimientoStockController.get_all()

@movimientos_stock.route('/mis')
@jwt_required()
def get_me():
    return MovimientoStockController.get_me()

@movimientos_stock.route('/', methods=['POST'])
@jwt_required()
def create():
    return MovimientoStockController.create(request.get_json())

