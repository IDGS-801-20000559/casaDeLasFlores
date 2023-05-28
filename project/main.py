from flask import Blueprint, flash, render_template, request
from flask_login import login_required
from flask_security import roles_accepted
from .models import Comentarios, Ventas
from . import db

import logging

import io
from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import dates as mdates
from datetime import datetime
import math

main = Blueprint('main', __name__)

@main.route("/")
def inicio():
    return render_template('index.html')

@main.route('/login', methods = ['GET', 'POST'])
def index():
    return render_template('login.html')

@main.route('/contacto', methods = ['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        email = request.form.get('correo')
        mensaje = request.form.get('mensaje')
        comentario = Comentarios(correo=email, mensaje=mensaje)

        db.session.add(comentario)
        db.session.commit()
        flash('GRACIAS POR TUS COMENTARIOS.')
        return render_template('contactanos.html')
    
    return render_template('contactanos.html')

@main.route('/sobre-nosotros', methods = ['GET', 'POST'])
def sobreNosotros():
    return render_template('sobre_nosotros.html')

@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@main.route('/comentarios')
@login_required
@roles_accepted("Administrador")
def obtenerComentarios():
    comments = Comentarios.query.all()

    return render_template('admin/consultarComentarios.html', comentarios = comments)

@main.route('/moduloGrafica')
@login_required
@roles_accepted("Administrador")
def moduloGrafica():
    valores = [300, 900, 600, 567.09, 800, 650, 210, 379.2, 200.77]
    suma = 0.0
    for valor in valores:
        suma = suma + float(valor)

    promedio = suma/len(valores)
    promedio = round(promedio, 2)

    return render_template('grafica.html', promedio = promedio)

@main.route('/grafica')
def grafica():
    fechas = ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01', '2022-06-01', '2022-07-01', '2022-08-01', '2022-09-01']
    valores = [300, 900, 600, 567.09, 800, 650, 210, 379.2, 200.77]

    # Convierte la lista de fechas a objetos datetime
    fechas = [datetime.strptime(fecha, '%Y-%m-%d').date() for fecha in fechas]
    
    # Crea la figura de la gráfica
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    # Agrega los datos a la gráfica
    axis.plot(fechas, valores, color='darkorange')

    axis.scatter(fechas, valores, color='yellow')

    # Configura el eje x de la gráfica con formato de fecha
    axis.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    
    #Establece el color de fondo de la grafica
    axis.set_facecolor('#F5F5F5')
    #Establece una etiqueta en los vectores de x, y
    axis.set_xlabel('Mes de ventas')
    axis.set_ylabel('Ventas (en pesos)')
    #Establece un titulo a la grafica
    axis.set_title('Promedio de ventas del periodo Enero-Septiembre 2022')

    # Agrega los valores en los puntos
    for fecha, valor in zip(fechas, valores):
        axis.text(fecha, valor, str(valor))

    # Genera la imagen de la gráfica
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)

    # Crea la respuesta HTTP con la imagen de la gráfica
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'

    return response

@main.route('/imprimirEstadistica')
def printEstadistica():
    return render_template('admin/estadisticas.html')

def registrarLogs(mensaje, tipoMensaje, file):
    # Crea un objeto logger:
    logger = logging.getLogger(__name__)
    # Configurar el nivel de registro para el logger
    logger.setLevel(logging.INFO)
    #Crea un manejador de archivos para almacenar los logs en un archivo
    if file == 'transaccion':
        log_file = 'registroTransacciones.log'
    if file == 'error':
        log_file = 'registroErrores.log'
    if file == 'bitacora':
        log_file = 'registroBitacora.log'

    file_handler = logging.FileHandler(log_file)
    # Configura el formato del mensaje de log:
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    #Agrega el manejador de archivos al logger
    logger.addHandler(file_handler)

    if tipoMensaje == 'error':
        logger.error(mensaje)
    elif tipoMensaje == 'info':
        logger.info(mensaje)
    elif tipoMensaje == 'warn':
        logger.warn(mensaje)
    elif tipoMensaje == 'debug':
        logger.debug(mensaje)
