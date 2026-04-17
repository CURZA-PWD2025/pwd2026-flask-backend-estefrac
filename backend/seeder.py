from app import create_app
from app.models import db
from app.models.rol import Rol
from app.models.user import User
from app.models.categoria import Categoria
from app.models.proveedor import Proveedor
from app.models.producto import Producto

app = create_app()

with app.app_context():
    # Roles
    rol_admin = Rol(nombre='admin')
    rol_op    = Rol(nombre='operador')
    db.session.add_all([rol_admin, rol_op])
    db.session.commit()

    # Usuarios
    admin = User(nombre='admin', email='admin@stock.com', rol_id=rol_admin.id, password='admin123')
    admin.generate_password('admin123')

    op1 = User(nombre='operador1', email='op1@stock.com', rol_id=rol_op.id, password='op1234')
    op1.generate_password('op1234')

    op2 = User(nombre='operador2', email='op2@stock.com', rol_id=rol_op.id, password='op1234')
    op2.generate_password('op1234')

    db.session.add_all([admin, op1, op2])
    db.session.commit()

    # Categorías
    alm = Categoria(nombre='Almacén', descripcion='Productos secos')
    lim = Categoria(nombre='Limpieza', descripcion='Artículos de limpieza')
    beb = Categoria(nombre='Bebidas', descripcion='Bebidas y jugos')
    db.session.add_all([alm, lim, beb])

    # Proveedores
    prov1 = Proveedor(nombre='Distribuidora Norte', telefono='2994001234')
    prov2 = Proveedor(nombre='Comercial Sur', telefono='2994005678', email='sur@comercial.com')
    prov3 = Proveedor(nombre='Mayorista Centro', contacto='Carlos López', telefono='2994009999')
    db.session.add_all([prov1, prov2, prov3])
    db.session.commit()

    # Productos
    db.session.add_all([
        Producto(nombre='Harina 000', precio_costo=280, precio_venta=350,
                 stock_actual=50, stock_minimo=10,
                 categoria_id=alm.id, proveedor_id=prov1.id),
        Producto(nombre='Arroz largo fino', precio_costo=320, precio_venta=420,
                 stock_actual=40, stock_minimo=10,
                 categoria_id=alm.id, proveedor_id=prov1.id),
        Producto(nombre='Aceite girasol 1L', precio_costo=900, precio_venta=1200,
                 stock_actual=25, stock_minimo=5,
                 categoria_id=alm.id, proveedor_id=prov2.id),
        Producto(nombre='Lavandina 1L', precio_costo=150, precio_venta=210,
                 stock_actual=30, stock_minimo=5,
                 categoria_id=lim.id, proveedor_id=prov1.id),
        Producto(nombre='Detergente 500ml', precio_costo=200, precio_venta=280,
                 stock_actual=20, stock_minimo=5,
                 categoria_id=lim.id, proveedor_id=prov2.id),
        Producto(nombre='Agua mineral 500ml', precio_costo=80, precio_venta=130,
                 stock_actual=100, stock_minimo=20,
                 categoria_id=beb.id, proveedor_id=prov3.id),
        Producto(nombre='Jugo naranja 1L', precio_costo=350, precio_venta=480,
                 stock_actual=35, stock_minimo=10,
                 categoria_id=beb.id, proveedor_id=prov3.id),
    ])
    db.session.commit()
    print("Seed completado.")
