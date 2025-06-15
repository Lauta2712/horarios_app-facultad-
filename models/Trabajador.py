from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Trabajador(db.Model):
    __tablename__ = 'trabajador'

    legajo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    horas = db.Column(db.Integer, nullable=False)
    funcion = db.Column(db.String(2), nullable=False)  

    def __repr__(self):
        return f'<Trabajador {self.legajo} - {self.apellido}, {self.nombre}>'
