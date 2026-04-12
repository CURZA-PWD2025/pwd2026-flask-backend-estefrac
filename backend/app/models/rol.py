from app.models.base_model import BaseModel
from app.models import db

class Rol(BaseModel):
    __tablename__="roles"
    nombre = db.Column(db.String, unique = True)
    activo = db.Column(db.String(1), default = 'S')
    
    
    def __init__(self, nombre) -> None:
        self.nombre = nombre
        
    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
            'nombre': self.nombre
            })
        return data
    
