from app.models.base_model import BaseModel
from app.models import db

class Categoria(BaseModel):
    __tablename__ = 'categorias'
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    productos = db.relationship('Producto')

    def __init__(self, nombre, descripcion=None) -> None:
        self.nombre = nombre
        self.descripcion = descripcion

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update(
            {
            'nombre': self.nombre,
            'descripcion': self.descripcion
            })
        return data
