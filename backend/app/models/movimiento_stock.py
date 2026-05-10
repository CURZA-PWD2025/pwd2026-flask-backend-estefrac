from app.models.base_model import BaseModel
from app.models import db

class MovimientoStock(BaseModel):
    __tablename__ = 'movimientos_stock'
    tipo = db.Column(db.String(10), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(200), nullable=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    producto = db.relationship('Producto', back_populates='movimientos_stock')
    user = db.relationship('User', back_populates='movimientos_stock')

    def __init__(self, tipo, cantidad, producto_id, user_id, motivo=None) -> None:
        self.tipo = tipo
        self.cantidad = cantidad
        self.motivo = motivo
        self.producto_id = producto_id
        self.user_id = user_id

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update(
            {
            'tipo': self.tipo,
            'cantidad': self.cantidad,
            'motivo': self.motivo,
            'producto_id': self.producto_id,
            'user_id': self.user_id
            })
        return data
