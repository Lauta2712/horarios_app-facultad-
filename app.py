from flask import Flask, render_template
from models.Trabajador import db
from flask import request, redirect, render_template
from models.Trabajador import db, Trabajador
from datetime import datetime, date
from models.RegistroHorario import RegistroHorario 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'clave-secreta'

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar_entrada', methods=['GET', 'POST'])
def registrar_entrada():
    mensaje = None
    if request.method == 'POST':
        legajo = request.form['legajo']
        dni = request.form['dni']
        dependencia = request.form['dependencia']

        trabajador = Trabajador.query.filter_by(legajo=legajo).first()
        if not trabajador or trabajador.dni[-4:] != dni:
            mensaje = "Datos inválidos"
        else:
            hoy = date.today()
            ya_registrado = RegistroHorario.query.filter_by(
                idtrabajador=legajo, fecha=hoy
            ).first()

            if ya_registrado:
                mensaje = "Ya existe un registro de entrada para hoy"
            else:
                nuevo_registro = RegistroHorario(
                    fecha=hoy,
                    horaentrada=datetime.now().time(),
                    dependencia=dependencia,
                    idtrabajador=legajo
                )

                db.session.add(nuevo_registro)
                db.session.commit()
                mensaje = "Entrada registrada correctamente"

    return render_template('registrar_entrada.html', mensaje=mensaje)

@app.route('/registrar_salida', methods=['GET', 'POST'])
def registrar_salida():
    mensaje = None
    if request.method == 'POST':
        legajo = request.form['legajo']
        dni = request.form['dni']

        trabajador = Trabajador.query.filter_by(legajo=legajo).first()
        if not trabajador or trabajador.dni[-4:] != dni:
            mensaje = "Datos inválidos"
        else:
            hoy = date.today()
            registro = RegistroHorario.query.filter_by(
                idtrabajador=legajo, fecha=hoy
            ).first()


            if not registro:
                mensaje = "No hay registro de entrada para hoy"
            elif registro.horasalida:
                mensaje = "Ya se registró salida para hoy"
            else:
                registro.horasalida = datetime.now().time()
                db.session.commit()
                mensaje = "Salida registrada correctamente"

    return render_template('registrar_salida.html', mensaje=mensaje)

@app.route('/consultar_registros', methods=['GET', 'POST'])
def consultar_registros():
    mensaje = None
    registros = []

    if request.method == 'POST':
        legajo = request.form['legajo']
        dni = request.form['dni']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']

        trabajador = Trabajador.query.filter_by(legajo=legajo).first()
        if not trabajador or trabajador.dni[-4:] != dni:
            mensaje = "Datos inválidos"
        else:
            registros = RegistroHorario.query.filter(
                RegistroHorario.idtrabajador == legajo,
                RegistroHorario.fecha >= fecha_inicio,
                RegistroHorario.fecha <= fecha_fin
            )

            if not registros:
                mensaje = "No se encontraron registros para el período seleccionado"

    return render_template('consultar_registros.html', mensaje=mensaje, registros=registros)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
