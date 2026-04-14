from dotenv import load_dotenv
from flask import Flask
from app.models import db
from app.config import config
from app.routes.user_routes import users
from app.routes.rol_routes import roles
from app.routes.auth_routes import auth_bp
from app.routes.categoria_routes import categorias
from app.routes.proveedor_routes import proveedores
from app.routes.producto_routes import productos
from app.routes.movimiento_stock_routes import movimientos_stock
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

load_dotenv(override = True)
import os
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    app.register_blueprint(users)
    app.register_blueprint(roles)
    app.register_blueprint(auth_bp)
    app.register_blueprint(categorias)
    app.register_blueprint(proveedores)
    app.register_blueprint(productos)
    app.register_blueprint(movimientos_stock)
    
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    jwt.init_app(app)
    return app
    
