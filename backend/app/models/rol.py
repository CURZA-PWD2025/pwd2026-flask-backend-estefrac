from typing import Any, cast
from app.models.base_model import BaseModel
from app.models import db

class Rol(BaseModel):
    __tablename__="roles"
    nombre = db.Column(db.String, unique = True)
    activo = db.Column(db.String(1), default = 'S')
    users = db.relationship('User', back_populates='rol')
    
    
    def __init__(self, nombre) -> None:
        self.nombre = nombre
        
    def to_dict(self, incluye_users=True) -> dict:
        data = super().to_dict()
        data.update ({
            'nombre': self.nombre
        })
        if incluye_users:
            data['users'] = [user.to_dict(incluye_rol=False) for user in cast(list[Any], self.users)]
        return data
