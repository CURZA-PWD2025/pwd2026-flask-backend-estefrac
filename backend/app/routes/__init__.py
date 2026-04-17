from app.routes.auth_routes import auth_bp
from app.routes.user_routes import users
from app.routes.rol_routes import roles
from app.routes.categoria_routes import categorias
from app.routes.proveedor_routes import proveedores
from app.routes.producto_routes import productos
from app.routes.movimiento_stock_routes import movimientos_stock
from flask import Blueprint

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')
api_v1.register_blueprint(auth_bp)
api_v1.register_blueprint(users)
api_v1.register_blueprint(roles)
api_v1.register_blueprint(categorias)
api_v1.register_blueprint(proveedores)
api_v1.register_blueprint(productos)
api_v1.register_blueprint(movimientos_stock)


