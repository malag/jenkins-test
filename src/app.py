#!/bin/python3

from flask import Flask, request, Response, jsonify
import requests, urllib.parse
from bs4 import BeautifulSoup
from markupsafe import escape
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image
import io
import numpy as np
import matplotlib.pyplot as plt
import base64
from sklearn.linear_model import LinearRegression
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, CDK classroom!'

@app.route('/saludo/<persona>')
def saludoDinamico(persona):
    return 'Hola %s, bienvenido!!' % persona

@app.route('/cuadrado/<float:num>')
def calculaCuadrado(num):
    resp = num * num
    return 'Respuesta: %f' % resp

@app.route('/curso', methods=['POST', 'GET'])
def webScrap():
    textReturn = "Método no aceptado"
    if request.method == 'POST':
        data = request.get_json()
        try:
            busqueda = data['busqueda']
            textReturn = "<p>Tu termino de busqueda es: <em>" + busqueda +"</em></p><ul>"
            busquedaText = busqueda.lower()
            busqueda = urllib.parse.quote(busqueda)
            page = requests.get('https://www.tecgurus.net/cursos?busqueda=' + busqueda)

            # Create a BeautifulSoup object
            soup = BeautifulSoup(page.text, 'html.parser')

            cursos_list = soup.find(class_='right-service-box')

            # Pull text from all instances of <a> tag within BodyText div
            cursos_items = cursos_list.find_all('img')

            for curso in cursos_items:
                tituloCurso = curso.get('alt');
                if tituloCurso.lower().find(busquedaText) != -1:
                    textReturn += "<li>" + curso.get('alt') + "</li>"
            textReturn +='</ul>'
        except:
            textReturn = "Ocurrio un error al procesar"            
    return textReturn

@app.route('/audiosaludo/<msgText>')
def audiotext(msgText):
	saludohtml = "<audio controls autoplay> <source src='https://code.responsivevoice.org/getvoice.php?text=%s&lang=es-MX&engine=g1&name=&pitch=0.5&rate=0.5&volume=1&key=uu8DEkxz&gender=female' type='audio/mpeg'> </audio>" % msgText	
	return saludohtml

@app.route('/convertir', methods=['POST', 'GET'])
def cambio_base():
    data = request.get_json()
    decimal = int(data['decimal'])
    base = int(data['base'])
    conversion = ''
    while decimal // base != 0:
        conversion = str(decimal % base) + conversion
        decimal = decimal // base
    return str(decimal) + conversion

#### Procedimiento para graficar ####
@app.route('/grafica.png', methods=['POST', 'GET'])
def plot_png():
   if request.method == 'POST':
      data = request.get_json()
      print(data)
      if data['tipo'] == 'pie':
         fig = pie(data)
      elif data['tipo'] == 'bar':
         fig = bar(data)
      else:
         fig = line(data)
      output = io.BytesIO()
      FigureCanvas(fig).print_png(output)
      return Response(output.getvalue(), mimetype='image/png')
   else:
      return "Petición GET no es válida"

def bar(datos):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    #data = {'apples': 10, 'oranges': 15, 'lemons': 5, 'limes': 20}
    #names = list(data.keys())
    #values = list(data.values())
    axis.bar(datos['nombres'], datos['valores'])
    return fig

def pie(datos):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.pie(datos['valores'], labels=datos['nombres'], autopct='%1.1f%%',
         shadow=True, startangle=90)
    axis.axis('equal')
    return fig

def line(datos):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(datos['nombres'], datos['valores'])
    return fig

###########

@app.route('/evidencia', methods=['POST', 'GET'])
def consumo():    
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        imagen = Image.open('./comida.jpg')
        imagen.show()
        return "<b>Se mando: título </b> %s" %data['titulo'] + ", <b> descripción: </b> %s " %data['descripcion']  + "  <b> calorías: </b> %i" %data['caloria'] + " <b> fecha: </b> %s" %data['fecha']
    else:
        return "Not found method"

@app.route("/reglin/", methods=["GET", "POST"])
def predecir():
    if request.method == "POST":
        data = request.get_json()
        if (data != None) and ('x' in data) and (type(data['x']) is list) and ('y' in data) and (type(data['y']) is list):
            valores_x = np.array(data['x'])
            valores_y = np.array(data['y'])
            # Entrenamiento
            regresion_lineal = LinearRegression()
            regresion_lineal.fit(valores_x.reshape(-1,1), valores_y)

            modelo_w = regresion_lineal.coef_
            modelo_b = regresion_lineal.intercept_

            # Realiza la prediccion
            if ('predicciones' in data) and int(data['predicciones']) > 0:
                numero_predicciones = int(data['predicciones'])
                maximo_x = valores_x.max()
                inicio_nuevos_x = maximo_x + 1
                fin_nuevos_x = maximo_x + numero_predicciones + 1
                step_nuevos = 1
                nuevos_x = np.arange(inicio_nuevos_x, fin_nuevos_x, step_nuevos)
                predicciones_y = regresion_lineal.predict(nuevos_x.reshape(-1,1))
                # Grafico
                plt.scatter(nuevos_x, predicciones_y, label="data", color="blue")
                plt.title("Predicciones")
                picIObytes = io.BytesIO()
                plt.savefig(picIObytes, format="png")
                picIObytes.seek(0)
                imgBase64Data = base64.b64encode(picIObytes.read())
                imgAsStr = imgBase64Data.decode('ascii')
                # Respuesta a devolver
                respuesta = {
                    "status": True,
                    "data": {
                        "x": nuevos_x.tolist(),
                        "y": predicciones_y.tolist(),
                        "chart": imgAsStr
                    }
                }
                return jsonify(respuesta)
            else:
                return "error"
        else:
            respuesta = {
                "status": False,
                "message": 'Error en la petición. Usa { x:[1,2, ... n], y:[1,2,3 ... n], predicciones: num }'
            }
            return jsonify(respuesta)
    elif request.method == "GET":
        return "Hola, GET!"

@app.route('/rlineal', methods=['POST','GET'])
def preRLinea():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        vx = data['vx']
        vy = data['vy']
        x = data['x']
        #return "y_obj: " + str(controller.getRLineal(vx, vy, x))
        return getRLineal(vx, vy, x)
    else:
        return "not found"

def getRLineal(v_x, v_y, x_pos):
    #v_x = [2014, 2015, 2016, 2017, 2018, 2019]
    #v_y = [530, 560, 610, 690, 720, 830]
    #x_pos = 202_0
    n = len(v_x)
    x, y, xy, xx = [0.0 for _ in range(4)]
    for i in range(n):
        x += v_x[i]
        y += v_y[i]
        xy += v_x[i] * v_y[i]
        xx += v_x[i] ** 2
    m = ((n * xy) - (x * y)) / ((n * xx) - (x ** 2))
    b = (y - (m * x)) / n
    y_obj = (m * x_pos) + b
    return json.dumps({"status": "ok", "y_obj":y_obj})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
