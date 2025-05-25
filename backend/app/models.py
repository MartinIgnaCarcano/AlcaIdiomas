from . import db
from datetime import datetime

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    contrasena = db.Column(db.String(200), nullable=False)
    fecha_registro = db.Column(db.Date, default=db.func.current_timestamp())
    rol = db.Column(db.String(20), default='user')
    
    def __repr__(self):
        return f'<Usuario {self.nombre}>'