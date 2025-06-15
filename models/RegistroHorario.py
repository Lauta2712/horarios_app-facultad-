from flask_sqlalchemy import SQLAlchemy
from models.Trabajador import db

class RegistroHorario(db.Model):
    __tablename__ = 'registrohorario'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    horaentrada = db.Column(db.Time, nullable=True)
    horasalida = db.Column(db.Time, nullable=True)
    dependencia = db.Column(db.String(3), nullable=False)

    idtrabajador = db.Column(db.Integer, db.ForeignKey('trabajador.legajo'), nullable=False)

    trabajador = db.relationship('Trabajador', backref='registros')
