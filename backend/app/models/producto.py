from app.models.base_model import BaseModel
from app.models import db

class Producto(BaseModel):
    __tablename__ = 'productos'
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio_costo = db.Column(db.Numeric(10, 2), nullable=False)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=True)
    categoria = db.relationship('Categoria', back_populates='productos')
    proveedor = db.relationship('Proveedor', back_populates='productos')
    movimientos_stock = db.relationship('MovimientoStock')

    def __init__(self, nombre, precio_costo, precio_venta, categoria_id, descripcion=None, stock_actual:int=0, stock_minimo:int=0, proveedor_id=None) -> None:
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_costo = precio_costo
        self.precio_venta = precio_venta
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.categoria_id = categoria_id
        self.proveedor_id = proveedor_id

    def to_dict(self, incluye_categoria=True, incluye_proveedor=True) -> dict:
        data = super().to_dict()
        data.update({
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_costo': str(self.precio_costo),
            'precio_venta': str(self.precio_venta),
            'stock_actual': self.stock_actual,
            'stock_minimo': self.stock_minimo,
        })
        if incluye_categoria:
            data['categoria'] = self.categoria.to_dict(incluye_productos=False) if self.categoria else None
        if incluye_proveedor:
            data['proveedor'] = self.proveedor.to_dict(incluye_productos=False) if self.proveedor else None
        return data
