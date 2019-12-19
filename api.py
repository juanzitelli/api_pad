# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask import render_template, request, make_response, redirect
from selenium import webdriver
import requests
import datetime
import pickle
import requests
from flask_cors import CORS
import os
from os import listdir
import csv
import json
import sys
import ast
# from gestorDialogo import get, post, delete

# db
import pymysql
import pymysql.cursors
# WordCloud
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from json import dump
import random
import string
# % matplotlib inline


"""
Documentar las api/

/pad
/pad/<todo_id>
/pad/contactosAiniciar/'
/pad/getContactos/'
/addcontact2/<contact>'
/addcontact/'


"""


def getConfig(vdato):  # configuracion.json
    try:
        arch_config = open("./Configuracion/configuracion.json", 'r')
        r = eval(arch_config.read())[vdato]
        return r
    except:
        return "none"


# region constantes ---------------------------------------------------------

vurlapi = getConfig('URLAPI')
URLAPI = vurlapi if vurlapi != 'none' else "http://127.0.0.1:5000/"

# URLAPI = 'http://167.86.94.15:5000/'

# URLAPI_TG = "http://chatbot-v2-api.baitsoftware.com"

URLAPI_TG = 'http://chatbot-v2-api.baitsoftware.com/api/'

arr_chat = []

env = {'rta': 'none'}

# endregion -----------------------------------------------------------------------

# region Configuraciones (ponele)
app = Flask(__name__)
CORS(app)
api = Api(app)

db_pad2 = {}

pad_store = {'key1': 'valor'}

comando = ['none']

arreglo_qr = ['none']

json_pr = {}

json_sonda = {
    'idProyecto': '1013',
    'vinit_mode': 'auto',
    'categoria_contactos': 'none',
    'nombrePrueba': 'np1',
    'varchivo_nro_cat': ''
}

TODOS = {
    'init': {'valor': 'init_chat', 'descp': 'Inicia el script de scrap'},
    'menu': {'valor': '0', 'descript': "0=no iniciado 1=cargando contactos 2="},
    'todo3': {'valor': 'valor'},
    'help': {'get': "curl http://localhost:5000/pad  -- curl http://localhost:5000/pad/help",
             'post': "curl http://localhost:5000/todos -d valor=1 -X POST -v",
             'put': "curl http://localhost:5000/todos/d1 -d valor=1 -X PUT -v"},
    'api': {'http://127.0.0.1:5000/IniciarChat/': 'Api de iniciación de conversaciones',
            '/pad/<todo_id>': 'help, api, init, menu',
            '/pad/contactosAiniciar/': 'api que devuelve los nros que inicialiaron el chat', '/pad/getContactos/': '',
            '/addcontact2/<contact>': '', '/addcontact/': ''}
}

Contactos2 = {'nro': 'estado'}

contactosToAdd = {'a': '12345'}
# endregion


def db2string(vsql):
    # dbServer = 'localhost'  # ip del servidor
    # dbUser = 'pad'  # usurio autorizado para leer la base de datos
    # dbPass = 'dalas'  # clave de la base de datos
    # dbBase = 'pad2'  # nombre de la base de datos

    dbServer = 'localhost'  # ip del servidor
    dbUser = 'root'  # usurio autorizado para leer la base de datos
    dbPass = ''  # clave de la base de datos
    dbBase = 'pad2'  # nombre de la base de datos

    result = ""

    db = pymysql.connect(host=dbServer, user=dbUser, passwd=dbPass, db=dbBase, cursorclass=pymysql.cursors.DictCursor,
                         database="mysql")

    cur = db.cursor()

    # vsql coantiene la query (ejemplo, select * from tabla where campo=valor)
    cur.execute(vsql)

    result = cur.fetchall()

    return result


@app.route('/pad/analizador222/', methods=['POST', 'GET'])
def analizador222():
    
    jsonToPost = ArmameElJSON_Bro(request.args.get('empresa'), request.args.get('experiencia'), request.args.get('num-telefono'), request.args.get(
        'pregunta'), request.args.get('respuesta'), request.args.get('fechadesde'), request.args.get('fechahasta'), request.args.get('horadesde'), request.args.get('horahasta'))
    modo = 1
    return render_template("pivote-output.html", json=jsonToPost, modo=modo)
  
    

# region Filtros


def ArmameElJSON_Bro(reqEMPRESA, reqEXPERIENCIA, reqNUMTELEFONO, reqPREGUNTA, reqRESPUESTA, reqFECHA_DESDE, reqFECHA_HASTA, reqHORA_DESDE, reqHORA_HASTA):
    query = ""
    consultaCamposTexto = ""
    if (not reqEMPRESA) and (not reqEXPERIENCIA) and (
            not reqNUMTELEFONO) and (not reqPREGUNTA) and (
            not reqRESPUESTA) and (not reqFECHA_DESDE) and (
                not reqHORA_DESDE and (not reqFECHA_HASTA)) and (
            not reqHORA_HASTA):
        query = "SELECT pad2.datos.empresa, pad2.datos.experiencia, pad2.datos.numtelefono, pad2.datos.pregunta," \
                "pad2.datos.respuesta, pad2.datos.hora, pad2.datos.fecha FROM pad2.datos; "
    else:
        consultaCamposTexto = Filtrar_Texto(reqEMPRESA,
                                            reqEXPERIENCIA,
                                            reqNUMTELEFONO,
                                            reqPREGUNTA,
                                            reqRESPUESTA)
        query = "SELECT pad2.datos.empresa, pad2.datos.experiencia, pad2.datos.numtelefono, pad2.datos.pregunta," \
                "pad2.datos.respuesta, pad2.datos.hora, pad2.datos.fecha FROM pad2.datos WHERE " + \
            consultaCamposTexto
        consultaCamposFecha = Filtrar_Fecha(reqFECHA_DESDE,
                                            reqHORA_DESDE,
                                            reqFECHA_HASTA,
                                            reqHORA_HASTA)
        query = query + consultaCamposFecha + " "
        if consultaCamposFecha == '':
            query = query[:-5]
            query = query + ";"

    resultadoRecienSacadoDeLaDB = db2string(query)

    for obj in resultadoRecienSacadoDeLaDB:
        obj["fecha"] = "'" + str(obj["fecha"]) + "'"
    jsonToPost = json.dumps(
        resultadoRecienSacadoDeLaDB, indent=4, sort_keys=True, default=str)
    return jsonToPost


def Filtrar_Texto(contenidoEmpresa, contenidoExperiencia, contenidoNumtelefono, contenidoPregunta, contenidoRespuesta):
    # Aca va todo menos fechas y horas
    subQueryuery = ""
    contadorDeContenidosSeteados = 0
    contenidosSeteados = []
    camposDBSeteados = []
    if contenidoEmpresa:
        contadorDeContenidosSeteados += 1
        contenidosSeteados.append(contenidoEmpresa)
        camposDBSeteados.append("pad2.datos.empresa")
    if contenidoExperiencia:
        contadorDeContenidosSeteados += 1
        contenidosSeteados.append(contenidoExperiencia)
        camposDBSeteados.append("pad2.datos.experiencia")
    if contenidoNumtelefono:
        contadorDeContenidosSeteados += 1
        contenidosSeteados.append(contenidoNumtelefono)
        camposDBSeteados.append("pad2.datos.numtelefono")
    if contenidoPregunta:
        contadorDeContenidosSeteados += 1
        contenidosSeteados.append(contenidoPregunta)
        camposDBSeteados.append("pad2.datos.pregunta")
    if contenidoRespuesta:
        contadorDeContenidosSeteados += 1
        contenidosSeteados.append(contenidoRespuesta)
        camposDBSeteados.append("pad2.datos.respuesta")
    contadorFor = 0
    for x in range(contadorDeContenidosSeteados):
        subQueryuery = subQueryuery + camposDBSeteados[contadorFor] + " LIKE " + "'%'" + '"' + contenidosSeteados[
            contadorFor] + '"' + "'%'" + " AND "
        contadorFor += 1
    return subQueryuery


def Filtrar_Fecha(contenidoFechadesde, contenidoHoradesde, contenidoFechahasta, contenidoHorahasta):
    subQuery = ""

    if contenidoFechadesde:
        contenidoFechadesde = "'" + contenidoFechadesde + "'"
    if contenidoHorahasta:
        contenidoHorahasta = "'" + contenidoHorahasta + "'"
    if contenidoHoradesde:
        contenidoHoradesde = "'" + contenidoHoradesde + "'"
    if contenidoFechahasta:
        contenidoFechahasta = "'" + contenidoFechahasta + "'"

    if contenidoFechadesde and contenidoFechahasta and contenidoHorahasta and contenidoHoradesde:
        subQuery = "(pad2.datos.fecha >= " + contenidoFechadesde + " AND pad2.datos.hora >= " + contenidoHoradesde + \
            ") AND ( pad2.datos.fecha <= " + contenidoFechahasta + \
            " AND pad2.datos.hora <= " + contenidoHorahasta + ");"

    if contenidoFechadesde and contenidoFechahasta and contenidoHorahasta and (not contenidoHoradesde):
        subQuery = "(pad2.datos.fecha >= " + contenidoFechadesde + ") AND ( pad2.datos.fecha <= " + \
            contenidoFechahasta + " AND pad2.datos.hora <= " + contenidoHorahasta + ");"

    if contenidoFechadesde and contenidoFechahasta and (not contenidoHorahasta) and contenidoHoradesde:
        subQuery = "(pad2.datos.fecha >= " + contenidoFechadesde + " AND pad2.datos.hora >= " + \
            contenidoHoradesde + \
            ") AND ( pad2.datos.fecha <= " + contenidoFechahasta + ");"

    if contenidoFechadesde and contenidoFechahasta and not (contenidoHorahasta) and not (contenidoHoradesde):
        subQuery = "(pad2.datos.fecha >= " + contenidoFechadesde + \
            ") AND ( pad2.datos.fecha <= " + contenidoFechahasta + ");"

    if contenidoFechadesde and not(contenidoFechahasta) and contenidoHorahasta and contenidoHoradesde:
        subQuery = "(pad2.datos.fecha >= " + contenidoFechadesde + " AND pad2.datos.hora >= " + \
            contenidoHoradesde + \
            ") AND (pad2.datos.hora <= " + contenidoHorahasta + ");"

    if contenidoFechadesde and not(contenidoFechahasta) and not (contenidoHorahasta) and not (contenidoHoradesde):
        subQuery = "(pad2.datos.fecha >= " + contenidoFechadesde + ");"

    if contenidoFechadesde and not(contenidoFechahasta) and not (contenidoHorahasta) and contenidoHoradesde:
        subQuery = "(pad2.datos.fecha >= " + contenidoFechadesde + \
            " AND pad2.datos.hora >= " + contenidoHoradesde + ");"

    if contenidoFechadesde and not(contenidoFechahasta) and contenidoHorahasta and not(contenidoHoradesde):
        subQuery = "(pad2.datos.fecha >= " + contenidoFechadesde + \
            ") AND ( pad2.datos.hora <= " + contenidoHorahasta + ");"

    if not (contenidoFechadesde) and contenidoFechahasta and not (contenidoHorahasta) and not (contenidoHoradesde):
        subQuery = "(pad2.datos.fecha <= " + contenidoFechahasta + ");"

    if not (contenidoFechadesde) and not (contenidoFechahasta) and not (contenidoHorahasta) and contenidoHoradesde:
        subQuery = "(pad2.datos.hora <= " + contenidoHorahasta + ");"

    if not (contenidoFechadesde) and not (contenidoFechahasta) and contenidoHorahasta and not (contenidoHoradesde):
        subQuery = "(pad2.datos.hora <= " + contenidoHorahasta + ");"

    if not (contenidoFechadesde) and not (contenidoFechahasta) and contenidoHorahasta and contenidoHoradesde:
        subQuery = "(pad2.datos.hora >= " + contenidoHoradesde + \
            ") AND (pad2.datos.hora <= " + contenidoHorahasta + ");"

    if not (contenidoFechadesde) and contenidoFechahasta and not (contenidoHorahasta) and contenidoHoradesde:
        subQuery = "(pad2.datos.hora >= " + contenidoHoradesde + \
            ") AND ( pad2.datos.fecha <= " + contenidoFechahasta + ");"

    if not (contenidoFechadesde) and contenidoFechahasta and contenidoHorahasta and not (contenidoHoradesde):
        subQuery = "(pad2.datos.fecha <= " + contenidoFechahasta + \
            " AND pad2.datos.hora <= " + contenidoHorahasta + ");"

    if not(contenidoFechadesde) and contenidoFechahasta and contenidoHorahasta and contenidoHoradesde:
        subQuery = "(pad2.datos.hora >= " + contenidoHoradesde + ") AND ( pad2.datos.fecha <= " + \
            contenidoFechahasta + " AND pad2.datos.hora <= " + contenidoHorahasta + ");"

    return subQuery
# endregion

# region Rutas de interés - Rutas de interés - Rutas de interés - Rutas de interés - Rutas de interés

@app.route("/pivotemain")
def pivotemain():
    return render_template("pivote-filters.html")


@app.route('/analizador', methods=['POST', 'GET'])
def analizador():
    return render_template("pivote-filters.html")


@app.route('/analisis-conversaciones', methods=['POST', 'GET'])
def analisisconversaciones():
    jsonToPost = json.dumps(request.form['json'])
    postedInfoMadeJson = json.loads(request.form['json']) #No sirve de una garcha
    try:
        jsonMadePyList = ast.literal_eval(request.form['json']) # QUE ESTO QUEDE ASI CARAJO
    except:
        jsonMadePyList = []
    if(len(jsonMadePyList) != 0):
        return render_template("pivote-analysis.html", json=jsonToPost)
    # Hasta aca
    else:
        return render_template("noresults.html")

    


@app.route('/wordcloud', methods=['POST', 'GET'])
def wordcloud():
    jsonToPost = json.dumps(request.form['wordcloud'])
    text = " "
    postedInfoMadeJson = json.loads(request.form['wordcloud'])
    jsonMadePyList = ast.literal_eval(postedInfoMadeJson) #idk if it works or nah
    wordArray = []
    for x in jsonMadePyList:
        text = text + x['respuesta'] + " "
        wordArray.append(x['respuesta'])
    wordcloud = WordCloud(width=480, height=480, margin=20,
                          background_color="white").generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=10, y=10)
    shortName = randomString()
    path = "C:/Users/juanz/Documents/CAETI/api_pad/static/img/img_wc/" + shortName + ".png"
    wordcloud.to_file(path)
    shortpath = "img/img_wc/" + shortName + ".png"
    wordArray.sort()
    # shortpath = "C:/Users/juanz/Documents/CAETI/api_pad/static/" + shortpath
    return render_template("wordcloud.html", json=jsonToPost, img_path=shortpath, words = wordArray)











@app.route('/word-analysis', methods=['POST', 'GET'])
def wordanalysis():
    jsonToPost = json.dumps(request.form['wordanalysis'])
    postedInfoMadeJson = json.loads(request.form['wordanalysis'])
    jsonMadePyList = ast.literal_eval(postedInfoMadeJson)
    
    print("******Debugger manual*******")
    
    print("El json que viene")
    # print(jsonToPost)
    # print(type(jsonToPost))
    
    print("*************")
    print("*************")
    
    print("El diccionario que tenemos para trabajar")
    # print(jsonMadePyList)
    # print(type(jsonMadePyList))

    print("*************")
    
    smallestDate = datetime.datetime.strptime("9999-12-31", '%Y-%m-%d')
    biggestDate = datetime.datetime.strptime("1984-01-01", '%Y-%m-%d') # Dance like a robot from 1984 🎶
    smallestTime = datetime.datetime.strptime("00-00-00", '%H-%M-%S')
    biggestTime = datetime.datetime.strptime("23-59-59", '%H-%M-%S')
    for objeto in jsonMadePyList:
        
        fechaSinLasComillasEsasDeMierda = objeto['fecha'].replace("'","")
        fechaDelObjeto = datetime.datetime.strptime(fechaSinLasComillasEsasDeMierda, '%Y-%m-%d')
        
        horaSinLasComillasEsasDeMierda = objeto['hora']
        # .replace("'","")
        horaDelObjeto = datetime.datetime.strptime(horaSinLasComillasEsasDeMierda, '%H:%M:%S')
        
        print(objeto['fecha'])
        print(objeto['hora'])
        #Menor fecha/hora
        if (fechaDelObjeto < smallestDate):
            smallestDate = fechaDelObjeto
            smallestTime = horaDelObjeto
        else:
            continue
        
        #Mayor fecha/hora
        if (fechaDelObjeto > biggestDate):
            biggestDate = fechaDelObjeto
            biggestTime = horaDelObjeto
        else:
            continue
        msj = f"El primer mensaje fue el {smallestDate} a las {smallestTime} y el ultimo fue el {biggestDate} a las {biggestTime}"
        print(msj)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    return render_template('wordanalysis.html', primeraFecha=smallestDate, ultimaFecha = biggestDate, primeraHora = smallestTime, ultimaHora = biggestTime)












# endregion
# Función para generar string random y guardar el  wordcloud
def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class analizador2(Resource):
    def get(self, file_name):
        return render_template("pivote-output.html")


# region DATOS INNECESARIOS PARA JUAN - - - DATOS INNECESARIOS PARA JUAN - - - DATOS INNECESARIOS PARA JUAN - - - DATOS INNECESARIOS PARA JUAN - - - DATOS INNECESARIOS PARA JUAN - - -


def get(id, num):
    # devuelve el mensaje correspondiente al id y num

    url = "http://chatbot-gd-api-v2.baitsoftware.com/api/experiences"

    url2 = url + '/' + str(id) + "/messages/" + str(num)

    r = requests.get(url2)

    r2 = r.text.replace('null', '"nulo"')

    try:
        json = eval(r2)

        vcomando = json["data"]

        rr = vcomando['message']

        return rr, vcomando

    except Exception as e:

        return 'error', 'error'


def post(num, id, message, actor):
    url = "http://chatbot-gd-api-v2.baitsoftware.com/api/DialogMessages"

    vdata = {"numReceptor": num, "idProject": int(
        id), "message": message, "actor": actor}

    r = requests.post(url, json=vdata)
    print(r)


def delete(num, id):
    try:

        url = "http://chatbot-gd-api-v2.baitsoftware.com/api/DialogChat"

        url = url + '/' + str(id) + '/' + num

        # vdata = {"numReceptor": num,"idProject": int(id)}

        r = requests.delete(url)

    except Exception as e:
        print(" Exception: ", e)


def getConfig(vdato):  # configuracion.json
    try:
        arch_config = open("./Configuracion/configuracion.json", 'r')
        r = eval(arch_config.read())[vdato]
        return r
    except:
        return "none"


def getComando():
    #
    rr = ""

    try:
        url = URLAPI + "pad/cualquiercosa"
        rr = getApi(url)
    except:
        rr = "error"

    return rr


def buscar_idProyecto(id_experiencia):
    try:

        if len(id_experiencia) < 10:
            return id_experiencia
        else:

            url = URLAPI_TG + 'experiences/' + id_experiencia
            r = getApi(url)
            jr = json.loads(r)

            vidProyecto = jr['data']['projectId']

            return vidProyecto

    except:

        return -1


def comandosonda(key, value):
    if key == "starting":
        # todo: ir  a buscar el id
        vidProyecto = buscar_idProyecto(key)
        json_sonda['idProyecto'] = vidProyecto

    else:
        pass


class setsonda(Resource):

    def put(self, valorsonda):
        global json_sonda

        temp = valorsonda.split(':')

        key = temp[0]
        value = temp[1]

        comandosonda(key, value)

        json_sonda = load_persist('json_sonda')

        json_sonda[key] = value

        save_persist('json_sonda')

        return 201


class sonda(Resource):
    def get(self):
        global json_sonda

        return json_sonda


class dropContactos2(Resource):
    def get(self):
        global Contactos2
        Contactos2 = {}
        save_persist('Contactos2')

        return Contactos2


class initChat(Resource):
    def get(self):

        result = []

        global Contactos2
        Contactos2 = load_persist('Contactos2')

        for r in Contactos2:
            print(r)

            vtopic = Contactos2[r]['topic']

            if vtopic == 'Iniciar':
                Contactos2[r]['topic'] = 'iniciado'

                print('60 > ', r, ' cambiado: ', Contactos2[r])

                result.append(r)

        print("***", Contactos2)
        save_persist('Contactos2')

        return result


def save_persist(elem):
    try:
        vpath = "./persist/"
        vpath = ""
        varchivo = vpath + elem + ".bin"
        with open(varchivo, "bw") as archivo:
            pickle.dump(eval(elem), archivo)
    except Exception as e:
        print("Exp save_persist ", e)


def load_persist(elem):
    try:

        vpath = "./persist/"
        vpath = ""
        varchivo = vpath + elem + ".bin"
        print(varchivo)
        with open(varchivo, "br") as archivo:
            # print(pickle.load(archivo))
            return pickle.load(archivo)

    except Exception as e:
        print(e)


def getApi(url):
    print("Entrando a getApi ", url)
    req = requests.get(url)
    return req.text


def setApi(url):
    req = requests.put(url)
    return req.status_code


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()

# parser.add_argument('contact')
parser.add_argument('valor')
parser.add_argument('v2')
parser.add_argument('contact2')
parser.add_argument('vcomando')
parser.add_argument('vcomando2')
parser.add_argument('key_value')
parser.add_argument('valorsonda')
parser.add_argument('luis_value')
parser.add_argument('vexpnro')
parser.add_argument('setvexpnro')
parser.add_argument('vnueva_experiencia')
parser.add_argument('vid_exp')
parser.add_argument('vid_nueva_exp')
parser.add_argument('getsonda_value')
parser.add_argument('file_name')


# Todo
# shows a single todo item and lets you delete a todo item


class getContactos(Resource):
    def get(self, vnro):
        # abort_if_todo_doesnt_exist(vnro)
        vContactos2 = load_persist('Contactos2')
        return vContactos2[vnro]


class listContactos(Resource):
    def get(self):
        # abort_if_todo_doesnt_exist(nro)
        Contactos2 = load_persist('Contactos2')
        return Contactos2


def luis_api_metodo(luis_value):
    vdato = luis_value.split(':')

    vid = vdato[0]
    vpregunta = vdato[1]

    url1 = "https://raw.githubusercontent.com/Funpei/chatBot/master/IA/pr" + vid + ".json"
    r = getApi(url1)

    json_pr = eval(r)

    json_sonda = load_persist('json_sonda')

    url = eval(json_sonda['luis'])[vid]
    url += '=' + vpregunta

    result = getApi(url)

    jr = eval(result)

    jr1 = (jr['topScoringIntent'])

    vcategoria = jr1['intent']

    # vmax = jr1['score']

    vrespuesta = json_pr[vcategoria]

    print("log 219", vrespuesta)

    return vrespuesta


class luis_api(Resource):
    def get(self, luis_value):
        vdato = luis_value.split(':')

        vid = vdato[0]
        vpregunta = vdato[1]

        url1 = "https://raw.githubusercontent.com/Funpei/chatBot/master/IA/pr" + vid + ".json"
        r = getApi(url1)

        json_pr = eval(r)

        json_sonda = load_persist('json_sonda')

        url = eval(json_sonda['luis'])[vid]
        url += '=' + vpregunta

        result = getApi(url)

        jr = eval(result)

        jr1 = (jr['topScoringIntent'])

        vcategoria = jr1['intent']

        # vmax = jr1['score']

        vrespuesta = json_pr[vcategoria]

        print("log 219", vrespuesta)

        return vrespuesta


class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        # task = {'valor': args['valor']}
        task = {'valor': todo_id}
        print(task, todo_id)
        TODOS[todo_id] = task
        print(TODOS)
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'valor': args['valor']}
        return TODOS[todo_id], 201


class AddContact(Resource):
    def post(self, contact):
        print(" ** pasa por addcontact")
        args = parser.parse_args()
        vcontact = args['contact']
        contactosToAdd[vcontact] = datetime.datetime.now()
        return 201

    def put(self, contact):
        print(" ** pasa por addcontact")
        args = parser.parse_args()
        vcontact = args['contact']
        contactosToAdd[vcontact] = datetime.datetime.now()
        return 201

    def get(self):
        return contactosToAdd


class ContactAdd(Resource):

    def get(self):
        print("** pasando por get")
        return contactosToAdd

    def post(self, contact):
        print(" ** pasa por addcontact")
        args = parser.parse_args()
        vcontact = args['contact']
        contactosToAdd[vcontact] = datetime.datetime.now()
        print(" _____________ ", vcontact, "  ", contactosToAdd[vcontact])
        return 201

    def put(self, contact):
        print(" ** pasa por addcontact")
        args = parser.parse_args()

        vvalor = args['valor']

        votro = args['v2']

        print(" _____________ ", contact, ' ', vvalor, ' ', votro)
        contactosToAdd[contact] = vvalor

        print(" _____________ ", contact, "  ", contactosToAdd[contact])

        return 201


# -----------------------------------------------

class command(Resource):

    def get(self, vcomando):
        print("**")
        return comando[0].strip()

    def put(self, vcomando):
        args = parser.parse_args()

        comando[0] = vcomando

        save_persist('comando')

        return 201


class command2(Resource):

    def put(self, vcomando2):
        temp = vcomando2.split(':')

        t1 = temp[0]
        t2 = temp[1]

        return 201


def getdb_contact(vidProyecto):
    db_pad2 = load_persist('db_pad2')

    key = 'exp_' + vidProyecto

    j1 = []

    j1 = db_pad2[key]

    arr_contacts = j1['contact']

    return arr_contacts


db_expriencias = {}


class nueva_experiencia(Resource):  # devuelven los contactos que hay en la db_pad2

    def put(self, vid_nueva_exp):
        try:
            try:
                db_pad2 = load_persist('vid_nueva_exp')
            except:
                pass

            key = vid_nueva_exp.split(',')[0]
            value = vid_nueva_exp.split(',')[1]

            db_expriencias[key] = value

            save_persist('db_expriencias')

        except:
            pass


class viewexp(Resource):  # devuelven los contactos que hay en la db_pad2
    def get(self, vid_exp):
        try:

            url1 = 'http://chatbot-v2-api.baitsoftware.com/api/experiences/' + vid_exp

            r = getApi(url1)

            jr = json.loads(r)

            c = jr['data']['conversation']['dialogUnits']

            ll = ""
            arr = []
            i = 0
            j = {}

            for cc in c:

                for ccc in cc['dialogMessages']:
                    i += 1
                    l = '{:<30}'.format(ccc['category']) + " - " + '{:<60}'.format(
                        ccc['message']) + " - " + '{:<30}'.format(ccc['nextDialog'])
                    j[i] = l
                    ll += l
                    arr.append(l)

            j = {'1': '11', '2': '21', '3': '31', '4': '41'}
            j = 'hola'
            print(j)

            return render_template("vexp.html", result=j)

        except Exception as e:
            print("Excepción en viewconversa")
            return 'none'


@app.route('/pad/viewexp2/', methods=['GET'])
def viewexp2():  # devuelven los contactos que hay en la db_pad2
    if request.method == 'GET':
        try:
            vid_exp = request.args.get('id')

            url1 = 'http://chatbot-v2-api.baitsoftware.com/api/experiences/' + vid_exp

            r = getApi(url1)

            jr = json.loads(r)

            c = jr['data']['conversation']['dialogUnits']

            ll = ""
            arr = []
            i = 0
            ii = 0
            j = {}
            jj = {}
            jjj = {}

            for cc in c:
                ii += 1
                i = 0
                j = {}

                ud = cc['alias']

                for ccc in cc['dialogMessages']:
                    i += 1
                    jj = {}
                    jj['alias'] = ud
                    jj['cat'] = ccc['category']
                    jj['men'] = ccc['message']
                    jj['proximo'] = ccc['nextDialog']

                    j[str(i)] = jj

                jjj[str(ii)] = j

            print(jjj)

            # jjj='none'

            return render_template("vexp.html", result=jjj)

        except Exception as e:
            print("Excepción en viewconversa   ", e)
            return 'none'


# devuelven los contactos que hay en la db_pad2
class getdb_contact_sonda(Resource):
    def get(self, vexpnro):
        try:
            db_pad2 = load_persist('db_pad2')

            key = 'exp_' + vexpnro

            j1 = []

            j1 = db_pad2[key]

            # arr_contacts = j1['contact']

            return j1

        except:
            return 'none'

    def put(self, vexpnro):
        try:
            db_pad2 = load_persist('db_pad2')

            if type(getsonda_value) == dict:
                for key in getsonda_value:
                    k = key
                    v = getsonda_value[k]
            else:
                temp = getsonda_value.split(':')

                k = temp[0]
                v = eval(temp[1])

            db_pad2[k] = v

            save_persist('db_pad2')

        except:
            return 'none'


class getsonda(Resource):
    def get(self, getsonda_value):
        try:
            json_sonda = load_persist('json_sonda')
            return json_sonda[getsonda_value]
        except:
            return 'none'


class store(Resource):

    def get(self, key_value):

        try:
            return pad_store[key_value]
        except:
            return "error"

    def put(self, key_value):

        dato = key_value

        dato1 = dato.split(':')

        if dato1[0] == 'qr':
            arreglo_qr[0] = dato1[1]
        else:
            pad_store[dato1[0]] = dato1[1]

        arreglo_qr[0] = dato1[1]

        save_persist('pad_store')

        return 201


# api 1 -
class apiContactos(Resource):

    def get(self):
        print("** pasando por get")
        return contactosToAdd

    def post(self, contact2):
        print(" **  post IniciarChat")
        args = parser.parse_args()
        vcontact = args['contact2']

        global Contactos2
        Contactos2[vcontact['nro']] = eval(contact2)

        return 201

    def put(self, contact2):
        print(" **  put IniciarChat")
        args = parser.parse_args()

        vjson = eval(contact2)

        # vcontact = args['contact2']

        global Contactos2

        Contactos2 = load_persist('Contactos2')

        Contactos2[vjson['nro']] = vjson

        save_persist('Contactos2')

        return 201


# api 2 -
class ContactGet(Resource):

    def get(self):
        print("** pasando por get")
        return contactosToAdd


##
# Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/pad')  # curl http://localhost:5000/todos
api.add_resource(Todo, '/pad/<todo_id>')  # cu0/todos/todo3

# api.add_resource(Contactos, '/pad/getContacto/<vnro>') # Contactos2

# api.add_resource(contactosAiniciar,'/pad/contactosAiniciar/') # Contactos2

# api.add_resource(Contactos, '/pad/setContacto/<vnro>') # Contactos2

# api.add_resource(ContactosTodos, '/pad/getContactos/') #  Contactos2

api.add_resource(ContactAdd, '/addcontact2/<contact>')  # cu0/todos/todo3

api.add_resource(ContactGet, '/addcontact/')  # cu0/todos/todo3

## api para pad2 ###################################################
api.add_resource(apiContactos,
                 '/pad/apiContactos/<contact2>')  # put, post para agregar contentido a Contactos2. Ej: {'nro':'1111,'name':'Ale','topic':'Iniciar'}
# Muestra el valor que tiene Contactos[vnro]
api.add_resource(getContactos, '/pad/getContacto/<vnro>')
api.add_resource(listContactos,
                 '/pad/listContactos/')  # Devuelve Contactos2. Es listado completo de todos los contactos
# devuelve los nros de contacto que deben ser iniciados
api.add_resource(initChat, '/pad/initChat/')
api.add_resource(dropContactos2, '/pad/dropContactos2/')
api.add_resource(command, '/pad/command/<vcomando>')
api.add_resource(command2, '/pad/command2/<vcomando2>')
api.add_resource(sonda, '/pad/sonda/')
api.add_resource(setsonda, '/pad/setsonda/<valorsonda>')
api.add_resource(getsonda, '/pad/getsonda/<getsonda_value>')
api.add_resource(store, '/pad/store/<key_value>')
api.add_resource(luis_api, '/pad/luis_api/<luis_value>')
api.add_resource(getdb_contact_sonda, '/pad/getdb_contact_sonda/<vexpnro>')
api.add_resource(viewexp, '/pad/viewexp/<vid_exp>')
api.add_resource(nueva_experiencia, '/pad/nueva_experiencia/<vid_nueva_exp>')
api.add_resource(analizador2, '/pad/analizador2/<file_name>')

#####################################################################


"""
Documentación
https://flask-restful.readthedocs.io/en/0.3.5/quickstart.html

curl http://localhost:5000/todos -d "task=something new" -X POST -v

http://asartorio.pythonanywhere.com/contactlist/    ----> lista todos los contactos


***
curl http://127.0.0.1:5000/addcontact2/777777 -d "valor=time 1" -X PUT

curl http://127.0.0.1:5000/addcontact/ -X GET -v
***


"""


@app.route("/hello1")
def hello1():
    return "Hello World para /hello1!"


@app.route("/scrapear")
def scrapear():
    options = webdriver.ChromeOptions()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome('./chromedriver')
    driver.get('http://www.google.com')
    vres = driver.title
    print(vres)  # this should print "Google"
    return vres


@app.route("/luis_init")
def luis_init():
    return render_template("luis.html", result=["", 0])


@app.route("/pad/chatprove2/", methods=['POST', 'GET'])
def chatprove2():
    tel = 1010

    if request.method == 'GET':

        vid_exp = request.args.get('id')
        texto = request.args.get('texto')

        idProject = buscar_idProyecto(vid_exp)

        if texto == None or texto == "" or texto.replace('""', '') == '':
            delete(str(tel), idProject)

            r = get(idProject, tel)
            rta = r[0]

            global arr_chat
            arr_chat = []
            arr_chat = ["*" + rta]
            env['rta'] = rta
            return render_template("chatprove.html", result=arr_chat, id_exp=vid_exp)

    if request.method == 'POST':

        result = request.form

        vid_exp = result['id_exp']
        vtexto = result['texto']

        idProject = buscar_idProyecto(vid_exp)

        if vtexto == "reiniciar":
            delete(str(tel), idProject)

            r = get(idProject, tel)
            rta = r[0]

            arr_chat = []
            arr_chat = ["*" + rta]

            env['rta'] = rta

            return render_template("chatprove.html", result=arr_chat, id_exp=vid_exp)

    # hacer post

    # post1  - todo: mando ultima pregunta

    arr_chat.append("................ " + vtexto)
    # arr_chat.append("*"+  rta)

    rta = env['rta']
    post(tel, idProject, rta, "s")

    # post2 - todo: mando respuesta del contacto

    respuesta_contacto = vtexto
    post(tel, idProject, respuesta_contacto, "c")

    # get - todo: obtengo respuesta del DG
    r = get(idProject, tel)
    rta = r[0]

    r1 = rta

    arr_chat.append("**" + rta)

    # mando al GD el mensaje de la regla
    post(tel, idProject, rta, "s")

    # Obtengo del GD el mensaje de la regla siguiente
    r = get(idProject, tel)
    rta = r[0]

    if rta != r1:
        arr_chat.append("*" + rta)
        arr_chat.append(".")

    env['rta'] = rta

    return render_template("chatprove.html", result=arr_chat, id_exp=vid_exp)


@app.route("/pad/chatprove/", methods=['POST', 'GET'])
def chatprove_public():
    if request.method == 'GET':

        vid_exp = request.args.get('id')
        texto = request.args.get('texto')
        vnro = request.args.get('nro')

        if vnro == None:
            tiempo = str(time.time())[-4:]
            tel = int(tiempo)
        else:
            tel = int(vnro)

        idProject = buscar_idProyecto(vid_exp)

        if texto == None or texto == "" or texto.replace('""', '') == '':
            delete(str(tel), idProject)

            r = get(idProject, tel)
            rta = r[0]

            global arr_chat
            arr_chat = []
            arr_chat = ["*" + rta]

            env['rta'] = rta

            return render_template("chatprove_public.html", result=arr_chat, id_exp=vid_exp, nro=tel)

    if request.method == 'POST':

        result = request.form

        vid_exp = result['id_exp']
        vtexto = result['texto']
        tel = int(result['nro'])

        idProject = buscar_idProyecto(vid_exp)

        if vtexto == "reiniciar":
            delete(str(tel), idProject)

            r = get(idProject, tel)
            rta = r[0]

            arr_chat = []
            arr_chat = ["*" + rta]

            env['rta'] = rta

            return render_template("chatprove_public.html", result=arr_chat, id_exp=vid_exp, nro=tel)

        # hacer post

        # post1  - todo: mando ultima pregunta

        if len(vtexto.split()) > 1:
            temp = intention(vtexto)

            if temp != vtexto:
                vtexto = '[' + temp + ']'
            else:
                vtexto = temp

        arr_chat.append(vtexto)
        # arr_chat.append("*"+  rta)

        rta = env['rta']
        post(tel, idProject, rta, "s")

        # post2 - todo: mando respuesta del contacto

        respuesta_contacto = vtexto
        post(tel, idProject, respuesta_contacto, "c")

        # get - todo: obtengo respuesta del DG
        r = get(idProject, tel)
        rta = r[0]

        r1 = rta

        arr_chat.append("**" + rta.ljust(30, ' '))

        # mando al GD el mensaje de la regla
        post(tel, idProject, rta, "s")

        # Obtengo del GD el mensaje de la regla siguiente
        r = get(idProject, tel)
        rta = r[0]

        if rta != r1:
            arr_chat.append("*" + rta.ljust(30, ' '))
            # arr_chat.append(".")

        env['rta'] = rta

        return render_template("chatprove_public.html", result=arr_chat, id_exp=vid_exp, nro=tel)


@app.route("/luis2", methods=['POST', 'GET'])
def luis2():
    if request.method == 'POST' or request.method == 'GET':

        try:

            url = URL_API + "pad/luis_api/"

            result = request.form

            vidp10 = result['nroexperiencia']
            vpregunta = result['vdato']

            url += vidp10 + ":" + vpregunta

            print("en luis2 getApi() : ", url)

            print(" luis_metodo ", luis_api_metodo(vidp10 + ":" + vpregunta))

            vrespuesta = luis_api_metodo(vidp10 + ":" + vpregunta)

            # vrespuesta = getApi(url).strip().replace('"','')

            rr = [vrespuesta, 0]
        except:
            rr = ["No hay respuesta", 0]

    return render_template("luis.html", result=rr)


# primer index
@app.route("/abmsonda1/")
def abmsonda():
    global json_sonda
    json_sonda = load_persist('json_sonda')
    return render_template("sonda.html", result=json_sonda)


# student
@app.route('/student/')
def student():
    return render_template('student.html')


# resultado2 es llamado dede la página anterior: student.html
@app.route('/result2', methods=['POST', 'GET'])
def result2():
    if request.method == 'POST':
        result = request.form
        return render_template("result.html", result=result)


# resultado2 es llamado dede la página anterior: student.html
@app.route('/List_nroEstados', methods=['POST', 'GET'])
def List_nroEstados():
    url = 'http://localhost:5000' + '/pad/contactosAiniciar/'

    # result1 = getApi(url)

    global Contactos2
    Contactos2 = load_persist('Contactos2')

    return render_template("List_nroEstados.html", result=Contactos2)


def pad_store(valor):
    try:
        if valor == 'qr':
            return arreglo_qr[0]
        else:

            return pad_store[valor]
    except:
        return "error"


@app.route('/getqr_api', methods=['POST', 'GET'])
def getqr_api():
    if request.method == 'GET':
        qr = pad_store('qr').replace(
            '--', ':').replace('*', '/').replace('"', '')

        # print(" 613 ",qr)

        return qr


@app.route('/getqr', methods=['POST', 'GET'])
def getqr():
    if request.method == 'GET':

        if json_sonda['vinit_mode'] == 'getqr_experience':

            url = URLAPI + "pad/store/qr"

            # url = url.replace('--',':')
            # qr = getApi(url).replace('--',':').replace('*','/').replace('"','')

            qr = pad_store('qr').replace(
                '--', ':').replace('*', '/').replace('"', '')

            if qr == 'none':
                qr = 'https://cdn.shopify.com/growth-tools-assets/qr-code/shopify-faae7065b7b351d28495b345ed76096c03de28bac346deb1e85db632862fd0e4.png'

            # print(" 613 ",qr)
        else:

            qr = 'https://store-images.s-microsoft.com/image/apps.15933.14374624288247235.7037ab92-5a5a-4529-b5af-025b76357642.493a34ee-eb48-40a5-b536-c3f141dce92a?mode=scale&q=90&h=300&w=300'

        return render_template("qr2.html", result=qr)


@app.route('/putsonda11', methods=['POST', 'GET', 'PUT'])
def putsonda11():
    if request.method == 'POST':
        result = request.form

        key = result['key']
        valor = result['valor']

        global json_sonda

        json_sonda = load_persist('json_sonda')

        json_sonda[key] = valor

        save_persist('json_sonda')

        print(json_sonda)

        return render_template("sonda.html", result=json_sonda)

    if request.method == 'PUT':
        result = str(request.data).replace(
            "b'", '').replace('\\\\', '')[:-1].split(':')

        key = result[0]
        valor = result[1]

        json_sonda = load_persist('json_sonda')

        json_sonda[key] = valor

        save_persist('json_sonda')

        return ""


@app.route('/lanzamiento_init', methods=['POST', 'GET'])
def lanzamiento_init():
    if request.method == 'POST':
        result = request.form

        nombre_contacto = result['nombre_contacto']
        idProyecto = result['idProyecto']
        categorias = result['categorias']
        accion = result['accion']
        nombre_prueba = result['nombre_prueba']

        # global json_sonda

        json_sonda['idProyecto'] = idProyecto
        json_sonda['vinit_mode'] = accion
        json_sonda['varchivo_nro_cat'] = nombre_contacto
        json_sonda['nombrePrueba'] = nombre_prueba
        json_sonda['categoria_contactos'] = categorias

        setApi(URL_API + "pad/command/" + accion)

        save_persist('json_sonda')

        print(json_sonda)

        return render_template("index.html")


@app.route('/wa_iniciar', methods=['POST', 'GET'])
def wa_iniciar():
    if request.method == 'POST':
        result = request.form
        print("Result: ", result['nro'])

        vnro = result['nro']
        vtema = result['tema']
        vnombre = result['nombre']
        vcomentario = result['comentario']

        vinit = {'nro': vnro, 'name': vnombre,
                 'topic': vtema, 'comment': vcomentario}

        global Contactos2
        Contactos2 = load_persist('Contactos2')

        Contactos2[vnro] = vinit

        save_persist('Contactos2')

        print(Contactos2)

        vurl = "https://wa.me/5492473466788?text=" + vinit['nro']

        print(vurl)

        return render_template("waIniciado.html")


@app.route('/cargarcontactos2', methods=['PUT', 'POST', 'GET'])
def cargar_contactos2():
    if request.method == 'POST':
        result = request.form

        vidProyecto = result['vidProyecto']
        vexp_contactos = result['expcontactos']

        global db_pad2
        db_pad2 = load_persist('db_pad2')

        # if es_formato correcto

        db_pad2["exp_" + vidProyecto] = eval(vexp_contactos)

        save_persist('db_pad2')

        return render_template("lanzamiento.html")

    # and request.headers['Content-Type'] == 'application/json':
    if request.method == 'PUT':

        temp = str(request.data).replace("b'", "").replace('\\\\', '')[:-1]
        j = eval(temp)

        # ----------------------------
        for i in j.keys():
            k = i
        key = k
        value = j[k]
        # -----------------------------

        try:

            # global db_pad2
            db_pad2 = load_persist('db_pad2')

            db_pad2["exp_" + key] = value

            save_persist('db_pad2')

            return "200"

        except:

            return "500 DB read-only"


@app.route('/admincontactos/')
def lanzamiento():
    # show the user profile for that user
    # todo - acá tengo que que persistir para que desde pad2 lo capte
    return render_template("lanzamiento.html")


@app.route('/putsonda1/')
def putsonda1():
    # show the user profile for that user

    # todo - acá tengo que que persistir para que desde pad2 lo capte

    return render_template("sonda.html")


@app.route('/wa/')
def wa():
    # show the user profile for that user

    # todo - acá tengo que que persistir para que desde pad2 lo capte

    return render_template("wa.html")


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    p = post_id + 100
    return 'Post %d' % p


# holaestoesuncomentarioparaprobarcopiarcosasdewindowsalinux

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/result')
def result():
    dict = {'phy': 50, 'che': 60, 'maths': 70}
    return render_template('result.html', result=dict)


@app.route('/index3')
def inde3():
    return render_template('index2.html')


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['nm']

    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie('userID', user)

    return resp


# endregion

if __name__ == '__main__':
    print(URLAPI[7:-6])
    #app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)

# region Otros datos innecesarios (Comentarios)
"""

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')



if __name__ == '__main__':
    app.run()

# -----------------------------------------------------------------

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run()

"""
# endregion
