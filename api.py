import ast
import codecs
import datetime
import json
import random
import string
from collections import Counter

import googletrans
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pymysql
import pymysql.cursors
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_restful import Api
from googletrans import Translator
from nltk import word_tokenize
from textblob import TextBlob
from wordcloud import WordCloud

app = Flask(__name__)
CORS(app)
api = Api(app)

# region Diccionarios
diccionarioClasificador_ENG = {
    "CC": "coordinating conjunction",
    "CD": "cardinal digit",
    "DT": "determiner",
    "EX": "existential",
    "FW": "foreign word",
    "IN": "preposition/subordinating conjunction",
    "JJ": "adjective	'big'",
    "JJR": "adjective, comparative	'bigger'",
    "JJS": "adjective, superlative	'biggest'",
    "LS": "list marker	1)",
    "MD": "modal	could, will",
    "NN": "noun, singular 'desk'",
    "NNS": "noun plural	'desks'",
    "NNP": "proper noun, singular	'Harrison'",
    "NNPS": "proper noun, plural	'Americans'",
    "PDT": "predeterminer	'all the kids'",
    "POS": "possessive ending",
    "PRP": "personal pronoun",
    "PRP$": "possessive pronoun",
    "RB": "adverb	very, silently,",
    "RBR": "adverb, comparative	better",
    "RBS": "adverb, superlative	best",
    "RP": "particle	give up",
    "TO": "to	go 'to' the store.",
    "UH": "interjection	errrrrrrrm",
    "VB": "verb, base form	take",
    "VBD": "verb, past tense	took",
    "VBG": "verb, gerund/present participle	taking",
    "VBN": "verb, past participle	taken",
    "VBP": "verb, sing. present, non-3d	take",
    "VBZ": "verb, 3rd person sing. present	takes",
    "WDT": "wh-determiner	which",
    "WP": "wh-pronoun	who, what",
    "WP$": "possessive wh-pronoun	whose",
    "WRB": "wh-abverb	where, when",
}

diccionarioClasificador_ESP = {
    "CC": "Conjuncion de coordinacion",
    "CD": "Digito cardinal",
    "DT": "Determinante",
    "EX": "Existencial",
    "FW": "Palabra extranjera",
    "IN": "Preposicion / Conjuncion subordinante",
    "JJ": "Adjetivo",
    "JJR": "Adjetivo comparativo",
    "JJS": "Adjetivo superlativo",
    "LS": "Marcador de lista",
    "MD": "Modal",
    "NN": "Sustantivo singular",
    "NNS": "Sustantivo plural",
    "NNP": "Nombre propio singular",
    "NNPS": "Nombre propio plural",
    "PDT": "Predeterminante",
    "POS": "Final posesivo",
    "PRP": "Pronombre personal",
    "PRP$": "Pronombre posesivo",
    "RB": "Adverbio",
    "RBR": "Adverbio comparativo",
    "RBS": "Advervbio superlativo",
    "RP": "Particula",
    "TO": "A-Hacia-Para",
    "UH": "Interjeccion",
    "VB": "Verbo base",
    "VBD": "Verbo pasado",
    "VBG": "Verbo gerundio / presente participio",
    "VBN": "Verbo pasado participio",
    "VBP": "Verbo singular presente",
    "VBZ": "Verbo tercera persona singular presente",
    "WDT": "Determinante WH",
    "WP": "Pronombre WH",
    "WP$": "Pronombre posesivo WH",
    "WRB": "Adverbio WH",
}

diccionario_freeling = {
    "A": {
        "Categoria": "Adjetivo",
        "Tipo": {
            "Q": "Calificativo",
            "O": "Ordinal",
            "0": "-"
        },
        "Grado": {
            "0": "-",
            "A": "Aumentativo",
            "C": "Diminutivo",
            "S": "Superlativo"
        }

    },
    "R": {
        "Categoria": "Adverbio",
        "Tipo": {
            "G": "General",
            "N": "Negativo"
        }
    },
    "D": {
        "Categoria": "Determinante",
        "Tipo": {
            "D": "Demostrativo",
            "P": "Posesivo",
            "T": "Interrogativo",
            "E": "Exclamativo",
            "I": "Indefinido",
            "A": "Articulo",
        },
        "Persona": {
            "1": "Primera",
            "2": "Segunda",
            "3": "Tercera"
        }

    },
    "N": {
        "Categoria": "Nombre",
        "Tipo": {
            "C": "Comun",
            "P": "Propio"
        },
        "Genero": {
            "M": "Masculino",
            "F": "Femenino",
            "C": "Comun"
        },
        "Numero": {
            "S": "Singular",
            "P": "Plural",
            "N": "Invariable"
        },
        "Clasificacion_semantica": {
            "SP": "Persona",
            "G0": "Lugar",
            "O0": "Organizacion",
            "V0": "Otros"
        }

    },
    "V": {
        "Categoria": "Verbo",
        "Tipo": {
            "M": "Principal",
            "A": "Auxiliar",
            "S": "Semiauxiliar"
        },
        "Modo": {
            "I": "Indicativo",
            "S": "Subjuntivo",
            "M": "Imperativo",
            "N": "Infinitivo",
            "G": "Gerundio",
            "P": "Participio"
        }
    },
    "P": {
        "Categoria": "Pronombre",
        "Tipo": {
            "P": "Personal",
            "D": "Demostrativo",
            "X": "Posesivo",
            "I": "Indefinido",
            "T": "Interrogativo",
            "R": "Relativo",
            "E": "Exclamativo"
        },
        "Persona": {
            "1": "Primera",
            "2": "Segunda",
            "3": "Tercera"
        }
    },
    "C": {
        "Categoria": "Conjuncion",
        "Tipo": {
            "C": "Coordinada",
            "S": "Subordinada"
        }
    },
    "I": {
        "Categoria": "Interjeccion"
    },
    "S": {
        "Categoria": "Adposicion",
        "Tipo": {
            "P": "Preposicion"
        },
        "Forma": {
            "S": "Simple",
            "C": "Contraida"
        }
    },
    "F": {
        "Categoria": "Puntuacion"
    },
    "Z": {
        "Categoria": "Cifra"
    },
}


# endregion

# region Filtros


def ArmarJSON(reqEMPRESA, reqEXPERIENCIA, reqNUMTELEFONO, reqPREGUNTA, reqRESPUESTA, reqFECHA_DESDE,
              reqFECHA_HASTA, reqHORA_DESDE, reqHORA_HASTA):
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

    if contenidoFechadesde and not (contenidoFechahasta) and contenidoHorahasta and contenidoHoradesde:
        subQuery = "(pad2.datos.fecha >= " + contenidoFechadesde + " AND pad2.datos.hora >= " + \
                   contenidoHoradesde + \
                   ") AND (pad2.datos.hora <= " + contenidoHorahasta + ");"

    if contenidoFechadesde and not (contenidoFechahasta) and not (contenidoHorahasta) and not (contenidoHoradesde):
        subQuery = "(pad2.datos.fecha >= " + contenidoFechadesde + ");"

    if contenidoFechadesde and not (contenidoFechahasta) and not (contenidoHorahasta) and contenidoHoradesde:
        subQuery = "(pad2.datos.fecha >= " + contenidoFechadesde + \
                   " AND pad2.datos.hora >= " + contenidoHoradesde + ");"

    if contenidoFechadesde and not (contenidoFechahasta) and contenidoHorahasta and not (contenidoHoradesde):
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

    if not (contenidoFechadesde) and contenidoFechahasta and contenidoHorahasta and contenidoHoradesde:
        subQuery = "(pad2.datos.hora >= " + contenidoHoradesde + ") AND ( pad2.datos.fecha <= " + \
                   contenidoFechahasta + " AND pad2.datos.hora <= " + contenidoHorahasta + ");"

    return subQuery


# endregion

# region Rutas

@app.route('/pad/analizador222/', methods=['POST', 'GET'])
def analizador222():
    jsonToPost = ArmarJSON(request.args.get('empresa'), request.args.get('experiencia'),
                           request.args.get('num-telefono'), request.args.get(
            'pregunta'), request.args.get('respuesta'), request.args.get('fechadesde'), request.args.get('fechahasta'),
                           request.args.get('horadesde'), request.args.get('horahasta'))
    modo = 1
    return render_template("pivote-output.html", json=jsonToPost, modo=modo)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pivotemain")
def pivotemain():
    return render_template("pivote-filters.html")


@app.route('/analizador', methods=['POST', 'GET'])
def analizador():
    return render_template("pivote-filters.html")


@app.route('/analisis-conversaciones', methods=['POST', 'GET'])
def analisisconversaciones():
    jsonToPost = json.dumps(request.form['json'])
    postedInfoMadeJson = json.loads(
        request.form['json'])  # No sirve de una garcha
    try:
        jsonMadePyObjectsLists = ast.literal_eval(
            request.form['json'])  # QUE ESTO QUEDE ASI CARAJO
    except:
        jsonMadePyObjectsLists = []
    if len(jsonMadePyObjectsLists) != 0:
        return render_template("pivote-analysis.html", json=jsonToPost)
    # Hasta aca
    else:
        return render_template("noresults.html")


@app.route('/wordcloud', methods=['POST', 'GET'])
def wordcloud():
    jsonToPost = json.dumps(request.form['wordcloud'])
    text = " "
    postedInfoMadeJson = json.loads(request.form['wordcloud'])
    jsonMadePyObjectsLists = ast.literal_eval(
        postedInfoMadeJson)  # idk if it works or nah
    wordArray = []
    for x in jsonMadePyObjectsLists:
        text = text + x['respuesta'] + " "
        wordArray.append(x['respuesta'])
    nube = WordCloud(width=480, height=480, margin=20,
                     background_color="white").generate(text)
    plt.imshow(nube, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=10, y=10)
    shortName = randomString()
    path = "/home/pad/pad2/sonda/api_pad/static/img/img_wc/" + shortName + ".png"
    nube.to_file(path)
    shortpath = "img/img_wc/" + shortName + ".png"
    wordArray.sort()
    # shortpath = "/home/pad/pad2/sonda/api_pad/static/" + shortpath
    return render_template("wordcloud.html", json=jsonToPost, img_path=shortpath, words=wordArray)


@app.route('/word-analysis', methods=['POST', 'GET'])
def wordanalysis():
    global tagged
    jsonToPost = json.dumps(request.form['wordanalysis'])
    postedInfoMadeJson = json.loads(request.form['wordanalysis'])
    jsonMadePyObjectsLists = ast.literal_eval(postedInfoMadeJson)

    # region Fechas iniciales y finales
    listOfDates = []
    listOfTimes = []
    for objeto in jsonMadePyObjectsLists:
        fechaSinComillas = objeto['fecha'].replace("'", "")
        fechaDelObjeto = datetime.datetime.strptime(
            fechaSinComillas, '%Y-%m-%d').date()
        horaSinComillas = objeto['hora'].replace("'", "")
        horaDelObjeto = datetime.datetime.strptime(
            horaSinComillas, '%H:%M:%S').time()
        listOfDates.append(fechaDelObjeto)
        listOfTimes.append(horaDelObjeto)
    doubleBubbleSort(listOfDates, listOfTimes)
    bubbleSort(listOfTimes)
    smallestDate = str(reorderDate(listOfDates[0]))
    biggestDate = str(reorderDate(listOfDates[len(listOfDates) - 1]))
    smallestTime = str(listOfTimes[0]) + " hs"
    biggestTime = str(listOfTimes[len(listOfTimes) - 1]) + " hs"
    # endregion

    # region Día más activo
    listOfUniqueDates = []
    counter = []
    for a in listOfDates:
        for b in listOfDates:
            if (a == b) and a not in listOfUniqueDates:
                listOfUniqueDates.append(a)
    new = Counter(listOfDates)
    listitaDePares = list(new.items())
    arr = []
    for x in list(listitaDePares):
        arr.append(x[1])
    doubleBubbleSort(arr, listOfDates)
    diaQueMasMensajesSeEnviaron = reorderDate(
        listOfDates[len(listOfDates) - 1])
    cantidadDeMensajesDelDiaQueMasMensajesSeEnviaron = arr[len(
        arr) - 1]
    # endregion

    # region Totalizadores

    # region DiasDeMensajes
    cantDias = len(listOfUniqueDates)
    # endregion

    # region Cant de palabras en respuestas
    palabrasEnRespuestas_TEXTO = ""
    test = ""
    for obj in jsonMadePyObjectsLists:
        palabrasEnRespuestas_TEXTO += obj['respuesta']
        test += obj['respuesta'] + " "
    palabras_entexto = palabrasEnRespuestas_TEXTO.split(" ")
    cantpalabras = len(palabrasEnRespuestas_TEXTO.split(" "))
    # region Letras en rtas
    stringConTodasLasRespuestas = ""
    for h in palabras_entexto:
        stringConTodasLasRespuestas += h
    listaDeLetras = list(stringConTodasLasRespuestas)
    totalDeLetras = len(listaDeLetras)

    # endregion
    # endregion

    # endregion

    # region Promedios
    respuestas = []
    for e in jsonMadePyObjectsLists:
        respuestas.append(e['respuesta'])
    cantRespuestas = len(respuestas)

    promedioRespuestasPorDia = round(
        cantRespuestas / len(listOfUniqueDates), 2)
    promedioLetrasPorRespuesta = round(totalDeLetras / cantRespuestas, 2)
    promedioLetrasPorDia = round(totalDeLetras / len(listOfUniqueDates), 2)
    promedioPalabrasPorRta = round(cantpalabras / cantRespuestas, 2)
    # endregion

    # region Grafico de barras de mensajes por x momento
    objects = ('Madrugada', 'Mañana', 'Mediodía',
               'Tarde', 'Noche', "Medianoche")
    y_pos = np.arange(len(objects))
    performance = [0, 0, 0, 0, 0, 0]
    for t in listOfTimes:
        if whatMomentOfTheDayIsIt(t) == "Madrugada":
            performance[0] += 1
        if whatMomentOfTheDayIsIt(t) == "Mañana":
            performance[1] += 1
        if whatMomentOfTheDayIsIt(t) == "Mediodía":
            performance[2] += 1
        if whatMomentOfTheDayIsIt(t) == "Tarde":
            performance[3] += 1
        if whatMomentOfTheDayIsIt(t) == "Noche":
            performance[4] += 1
        if whatMomentOfTheDayIsIt(t) == "Medianoche":
            performance[5] += 1
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Cantidad de mensajes')
    plt.title('Cantidad de mensajes enviados por momento del día')
    filename = randomString()
    longpathBarChart = '/home/pad/pad2/sonda/api_pad/static/img/img_bc/' + \
                       filename + '.png'
    shortPath = 'img/img_bc/' + filename + ".png"
    plt.savefig(longpathBarChart)
    # endregion

    # region Clasificador de palabras

    respuestas_separadas_con_espacios = ""
    traductor = Translator()
    for q in respuestas:
        respuestas_separadas_con_espacios += q
        respuestas_separadas_con_espacios += " "
    try:  # Traducir las palabras
        rta = traductor.translate(
            str(respuestas_separadas_con_espacios), dest="en")
        respuestas_separadas_con_espacios = str(rta.text)
    except Exception as e:
        print("Excepción de traduccion")
        print(str(e))
    palabras = word_tokenize(respuestas_separadas_con_espacios)
    try:  # Etiquetar las palabras
        tagged = nltk.pos_tag(palabras)
    except Exception as e:
        print("Excepción de postag")
        print(str(e))
    listOfUniqueKeysInTagged = []
    for tuplita in tagged:
        if tuplita[1] not in listOfUniqueKeysInTagged and tuplita[1] in diccionarioClasificador_ESP.keys():
            listOfUniqueKeysInTagged.append(tuplita[1])
        else:
            pass
    cantidad_de_tipos_de_palabras = {}
    for key in listOfUniqueKeysInTagged:
        cantidad_de_tipos_de_palabras[key] = 0
    for tupla_de_palabra_tipo in tagged:
        for value in listOfUniqueKeysInTagged:

            if tupla_de_palabra_tipo[1] == value:
                cantidad_de_tipos_de_palabras[value] += 1
    diccionario_final_correcto = {}
    for n in cantidad_de_tipos_de_palabras:
        if n in diccionarioClasificador_ESP:
            diccionario_final_correcto[diccionarioClasificador_ESP[n]
            ] = cantidad_de_tipos_de_palabras[n]
    diccionario_final_correcto = {k: v for k, v in sorted(
        diccionario_final_correcto.items(), key=lambda item: item[1])}
    listita = []
    dicEnLista = list(diccionario_final_correcto)
    for i in range(len(diccionario_final_correcto) - 1):
        listita.append(
            [dicEnLista[len(dicEnLista) - i - 1], diccionario_final_correcto[dicEnLista[len(dicEnLista) - i - 1]]])
    finalDict = {}
    for l in listita:
        key = l[0]
        value = l[1]
        finalDict[key] = value
    try:
        listaparajson = []
        for key, value in finalDict.items():
            listaparajson.append({key: value})
        if len(listaparajson) > 5:
            listaparajson = listaparajson[:5]
        else:
            pass
    except Exception as e:
        print(str(e))

    finalDict = json.dumps(str(finalDict))
    string_de_finaldict_reemplazando_comillas = str(
        finalDict).replace("'", '"')
    b = [i for i in string_de_finaldict_reemplazando_comillas]
    b[len(b) - 1] = "'"
    b[0] = "'"
    string_de_finaldict_reemplazando_comillas = ""
    for x in b:
        string_de_finaldict_reemplazando_comillas += x

    return render_template('wordanalysis.html', json=jsonToPost, primeraFecha=smallestDate, ultimaFecha=biggestDate,
                           primeraHora=smallestTime, ultimaHora=biggestTime, masmensajes=diaQueMasMensajesSeEnviaron,
                           cantmasmensajes=cantidadDeMensajesDelDiaQueMasMensajesSeEnviaron, cantDiasRtas=cantDias,
                           cantPalabras=cantpalabras, cantLetras=totalDeLetras, promRtaPorDia=promedioRespuestasPorDia,
                           promLetrasRta=promedioLetrasPorRespuesta, promedioLetrasPorDia=promedioLetrasPorDia,
                           promedioPalabrasPorRta=promedioPalabrasPorRta, barchart=shortPath,
                           clasificacionPalabras=string_de_finaldict_reemplazando_comillas)
    # endregion


@app.route('/etiquetador-morfologico', methods=['POST', 'GET'])
def etiquetador():
    oracion = ""
    jsonToPost = json.dumps(request.form['etiquetador'])
    postedInfoMadeJson = json.loads(request.form['etiquetador'])
    jsonMadePyObjectsLists = ast.literal_eval(postedInfoMadeJson)
    for i in jsonMadePyObjectsLists:
        oracion += i["respuesta"]
        oracion += " "
    entrada = codecs.open("fragmento-wikicorpus-tagged-spa.txt", "r", encoding="utf-8")
    tagged_words = []
    tagged_sents = []
    for linea in entrada:
        linea = linea.rstrip()
        if linea.startswith("<") or len(linea) == 0:
            if len(tagged_words) > 0:
                tagged_sents.append(tagged_words)
                tagged_words = []
        else:
            camps = linea.split(" ")
            forma = camps[0]
            lema = camps[1]
            etiqueta = camps[2]
            tupla = (forma, etiqueta)
            tagged_words.append(tupla)

    unigram_tagger = nltk.UnigramTagger(tagged_sents)
    bigram_tagger = nltk.BigramTagger(tagged_sents, backoff=unigram_tagger)
    tokens = nltk.tokenize.word_tokenize(oracion)
    analisi = bigram_tagger.tag(tokens)
    analisis = []
    for n in analisi:
        if n in analisi and n not in analisis:
            analisis.append(n)
    palabras_etiquetadas = []
    listadeNN = []
    for palabra_analizada in analisis:
        palabra_analizada = list(palabra_analizada)
        if str(type(palabra_analizada[1])) != "<class 'NoneType'>":
            minilist = [palabra_analizada[0], etiquetado_morfologico(palabra_analizada[1])]
            palabras_etiquetadas.append(minilist)
        else:
            palabra_analizada[1] = "None"
            minilist = [palabra_analizada[0], etiquetado_morfologico(palabra_analizada[1])]
            listadeNN.append(minilist)

    n = len(palabras_etiquetadas)
    for i in range(n):
        for j in range(0, n - i - 1):
            if palabras_etiquetadas[j][1] > palabras_etiquetadas[j + 1][1]:
                palabras_etiquetadas[j], palabras_etiquetadas[j + 1] = palabras_etiquetadas[j + 1], \
                                                                       palabras_etiquetadas[j]
    return render_template('etiquetado_morfologico.html', lista_palabras_etiquetadas=palabras_etiquetadas,
                           lista_palabras_no_reconocidas=listadeNN)


@app.route('/posneg', methods=['POST', 'GET'])
def posneg():
    jsonToPost = json.dumps(request.form['posneg'])
    postedInfoMadeJson = json.loads(request.form['posneg'])
    jsonMadePyObjectsLists = ast.literal_eval(postedInfoMadeJson)
    texto = ""
    for element in jsonMadePyObjectsLists:
        texto += f'{element["respuesta"]} '
    objetoAnalizador = TextBlob(texto)
    objetoAnalizador_Traducido = objetoAnalizador.translate(to="en")
    try:
        sentiments = []
        # [x.sentiment.polarity for x in word_tokenize(objetoAnalizador_Traducido)]
        for palabra in word_tokenize(str(objetoAnalizador_Traducido)):
            elementotecsblob = TextBlob(palabra)
            sentiments.append(elementotecsblob.sentiment.polarity)
        total = len(word_tokenize(str(objetoAnalizador_Traducido)))
        positives = [pos for pos in sentiments if pos > 0]
        negatives = [neg for neg in sentiments if neg < 0]
        neutrals = [neutral for neutral in sentiments if neutral == 0]
        pptg = str(round((len(positives) / total) * 100, 2))
        nptg = str(round((len(negatives) / total) * 100, 2))
        neuptg = str(round((len(neutrals) / total) * 100, 2))
    except Exception as e:
        print(str(e))
    return render_template('posneg.html', pos=pptg, neg=nptg, neutral=neuptg)


@app.route('/language', methods=['POST', 'GET'])
def language():
    global palabra_traducida
    translator_languages_dict = googletrans.LANGUAGES
    jsonToPost = json.dumps(request.form['language'])
    postedInfoMadeJson = json.loads(request.form['language'])
    jsonMadePyObjectsLists = ast.literal_eval(postedInfoMadeJson)
    respuestas = []
    idioma_respuestas = []
    textito = ""
    try:
        for i in jsonMadePyObjectsLists:
            palabra = i["respuesta"]
            respuestas.append(palabra)
            textito += palabra
        palabra_tra = TextBlob(textito)
        palabra_traducida = palabra_tra.detect_language()
    except Exception as e:
        print(str(e))
    translatorcito = Translator()
    QueIdiomaEs = translatorcito.translate(
        translator_languages_dict[palabra_traducida], "es", "en")
    imagen_bandera = "img/banderas/" + palabra_traducida + ".png"

    return render_template('language_identifier.html', json=jsonToPost, idioma=QueIdiomaEs.text,
                           bandera=imagen_bandera)


# endregion

# region Funciones útiles

def db2string(vsql):
    dbServer = 'localhost'  # ip del servidor
    dbUser = 'pad'  # usurio autorizado para leer la base de datos
    dbPass = 'dalas'  # clave de la base de datos
    dbBase = 'pad2'  # nombre de la base de datos

    # dbServer = 'localhost'  # ip del servidor
    # dbUser = 'root'  # usurio autorizado para leer la base de datos
    # dbPass = ''  # clave de la base de datos
    # dbBase = 'pad2'  # nombre de la base de datos

    result = ""

    db = pymysql.connect(host=dbServer, user=dbUser, passwd=dbPass, db=dbBase, cursorclass=pymysql.cursors.DictCursor,
                         database="mysql")

    cur = db.cursor()

    # vsql coantiene la query (ejemplo, select * from tabla where campo=valor)
    cur.execute(vsql)

    result = cur.fetchall()

    return result


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def whatMomentOfTheDayIsIt(dateParameter):
    if dateParameter >= datetime.datetime.strptime('01:00:00',
                                                   '%H:%M:%S').time() and dateParameter <= datetime.datetime.strptime(
        '05:00:00', '%H:%M:%S').time():
        return "Madrugada"
    # Madrugada
    if dateParameter > datetime.datetime.strptime('05:00:00',
                                                  '%H:%M:%S').time() and dateParameter <= datetime.datetime.strptime(
        '11:00:00', '%H:%M:%S').time():
        return "Mañana"
    # Mañana
    if dateParameter > datetime.datetime.strptime('11:00:00',
                                                  '%H:%M:%S').time() and dateParameter <= datetime.datetime.strptime(
        '14:00:00', '%H:%M:%S').time():
        return "Mediodía"
    # Mediodía
    if dateParameter > datetime.datetime.strptime('14:00:00',
                                                  '%H:%M:%S').time() and dateParameter <= datetime.datetime.strptime(
        '19:00:00', '%H:%M:%S').time():
        return "Tarde"
    # Tarde
    if dateParameter > datetime.datetime.strptime('19:00:00',
                                                  '%H:%M:%S').time() and dateParameter <= datetime.datetime.strptime(
        '23:00:00', '%H:%M:%S').time():
        return "Noche"
    # Noche
    if dateParameter >= datetime.datetime.strptime('01:00:00',
                                                   '%H:%M:%S').time() and dateParameter <= datetime.datetime.strptime(
        '05:00:00', '%H:%M:%S').time():
        return "Medianoche"
    # Medianoche


def doubleBubbleSort(nlist, nlist2):
    for passnum in range(len(nlist) - 1, 0, -1):
        for i in range(passnum):
            if nlist[i] > nlist[i + 1]:
                temp = nlist[i]
                temp2 = nlist2[i]
                nlist[i] = nlist[i + 1]
                nlist2[i] = nlist2[i + 1]
                nlist[i + 1] = temp
                nlist2[i + 1] = temp2


def bubbleSort(nlist):
    for passnum in range(len(nlist) - 1, 0, -1):
        for i in range(passnum):
            if nlist[i] == nlist[i + 1]:
                if nlist[i] > nlist[i + 1]:
                    temp = nlist[i]
                    nlist[i] = nlist[i + 1]
                    nlist[i + 1] = temp


def reorderDate(oldDate):
    # Ej: 2019-03-11 ==> ["2019", "03", "11"]
    arregloFechaVieja = str(oldDate).split('-')
    hora = arregloFechaVieja[0]
    mes = arregloFechaVieja[1]
    dia = arregloFechaVieja[2]
    nuevafecha = dia + "/" + mes + "/" + hora
    return nuevafecha


def etiquetado_morfologico(codigo):
    global primera_letra
    global segunda_letra
    global tercera_letra
    global quinsex_letra
    global cuarta_letra
    codigo = str(codigo).upper()
    if len(str(codigo)) == 1:
        primera_letra = str(codigo[0])
    elif len(str(codigo)) == 2:
        primera_letra = str(codigo[0])
        segunda_letra = str(codigo[1])
    elif len(str(codigo)) == 3:
        primera_letra = str(codigo[0])
        segunda_letra = str(codigo[1])
        tercera_letra = str(codigo[2])
    elif len(str(codigo)) == 4:
        primera_letra = str(codigo[0])
        segunda_letra = str(codigo[1])
        tercera_letra = str(codigo[2])
        cuarta_letra = str(codigo[3])
    elif len(str(codigo)) > 4:
        primera_letra = str(codigo[0])
        segunda_letra = str(codigo[1])
        tercera_letra = str(codigo[2])
        cuarta_letra = str(codigo[3])
        quinsex_letra = str(f"{codigo[4]}{codigo[5]}")
    resultado_del_etiquetado = ""
    if codigo == "NONE" or codigo == "none" or codigo == "None":
        resultado_del_etiquetado = "N/D"
        return resultado_del_etiquetado
    if primera_letra == "A":  # Adjetivo
        adj_cat = diccionario_freeling[primera_letra]["Categoria"]

        if segunda_letra in diccionario_freeling[primera_letra]["Tipo"]:
            adj_tipo = diccionario_freeling[primera_letra]["Tipo"][segunda_letra]
        else:
            adj_tipo = ""

        if tercera_letra in diccionario_freeling[primera_letra]["Grado"]:
            adj_grado = diccionario_freeling[primera_letra]["Grado"][tercera_letra]
        else:
            adj_grado = ""

        resultado_del_etiquetado += f"{adj_cat} "
        resultado_del_etiquetado += f"{adj_tipo} "
        resultado_del_etiquetado += f"{adj_grado} "
    elif primera_letra == "R":  # Adverbio

        adv_cat = diccionario_freeling[primera_letra]["Categoria"]
        if segunda_letra in diccionario_freeling[primera_letra]["Tipo"]:
            adv_tipo = diccionario_freeling[primera_letra]["Tipo"][segunda_letra]
        else:
            adv_tipo = ""

        resultado_del_etiquetado = f"{adv_cat} "
        resultado_del_etiquetado += f"{adv_tipo} "
    elif primera_letra == "D":  # Determinante
        det_cat = diccionario_freeling[primera_letra]["Categoria"]
        if segunda_letra in diccionario_freeling[primera_letra]["Tipo"]:
            det_tipo = diccionario_freeling[primera_letra]["Tipo"][segunda_letra]
        else:
            det_tipo = ""
        if tercera_letra in diccionario_freeling[primera_letra]["Persona"]:
            det_per = diccionario_freeling[primera_letra]["Persona"][tercera_letra]
        else:
            det_per = ""

        resultado_del_etiquetado = f"{det_cat} "
        resultado_del_etiquetado += f"{det_tipo} "
        resultado_del_etiquetado += f"{det_per} "
    elif primera_letra == "N" and codigo != "None":  # Nombre
        nom_cat = diccionario_freeling[primera_letra]["Categoria"]
        if segunda_letra in diccionario_freeling[primera_letra]["Tipo"]:
            nom_tipo = diccionario_freeling[primera_letra]["Tipo"][segunda_letra]
        else:
            nom_tipo = ""
        if tercera_letra in diccionario_freeling[primera_letra]["Genero"]:
            nom_gen = diccionario_freeling[primera_letra]["Genero"][tercera_letra]
        else:
            nom_gen = ""
        if cuarta_letra in diccionario_freeling[primera_letra]["Numero"]:
            nom_num = diccionario_freeling[primera_letra]["Numero"][cuarta_letra]
        else:
            nom_num = ""
        if quinsex_letra in diccionario_freeling[primera_letra]["Clasificacion_semantica"]:
            nom_clas = diccionario_freeling[primera_letra]["Clasificacion_semantica"][quinsex_letra]
        else:
            nom_clas = ""
        resultado_del_etiquetado = f"{nom_cat} "
        resultado_del_etiquetado += f"{nom_tipo} "
        resultado_del_etiquetado += f"{nom_gen} "
        resultado_del_etiquetado += f"{nom_num} "
        resultado_del_etiquetado += f"{nom_clas} "
    elif primera_letra == "V":  # Verbo
        verb_cat = diccionario_freeling[primera_letra]["Categoria"]

        if segunda_letra in diccionario_freeling[primera_letra]["Tipo"]:
            verb_tipo = diccionario_freeling[primera_letra]["Tipo"][segunda_letra]
        else:
            verb_tipo = ""

        if tercera_letra in diccionario_freeling[primera_letra]["Modo"]:
            verb_modo = diccionario_freeling[primera_letra]["Modo"][tercera_letra]
        else:
            verb_modo = ""
        resultado_del_etiquetado = f"{verb_cat} "
        resultado_del_etiquetado += f"{verb_tipo} "
        resultado_del_etiquetado += f"{verb_modo} "
    elif primera_letra == "P":  # Pronombre

        pron_cat = diccionario_freeling[primera_letra]["Categoria"]

        if segunda_letra in diccionario_freeling[primera_letra]["Tipo"]:
            pron_tipo = diccionario_freeling[primera_letra]["Tipo"][segunda_letra]
        else:
            pron_tipo = ""

        if tercera_letra in diccionario_freeling[primera_letra]["Persona"]:
            pron_pers = diccionario_freeling[primera_letra]["Persona"][tercera_letra]
        else:
            pron_pers = ""

        resultado_del_etiquetado = f"{pron_cat} "
        resultado_del_etiquetado += f"{pron_tipo} "
        resultado_del_etiquetado += f"{pron_pers} persona "
    elif primera_letra == "C":  # Conjuncion
        conj_cat = diccionario_freeling[primera_letra]["Categoria"]

        if segunda_letra in diccionario_freeling[primera_letra]["Tipo"]:
            conj_tipo = diccionario_freeling[primera_letra]["Tipo"][segunda_letra]
        else:
            conj_tipo = ""

        resultado_del_etiquetado = f"{conj_cat} "
        resultado_del_etiquetado += f"{conj_tipo} "
    elif primera_letra == "I":  # Interjeccion
        int_cat = diccionario_freeling[primera_letra]["Categoria"]
        resultado_del_etiquetado = f"{int_cat} "
    elif primera_letra == "S":  # Adposicion
        adp_cat = diccionario_freeling[primera_letra]["Categoria"]

        if segunda_letra in diccionario_freeling[primera_letra]["Tipo"]:
            adp_tipo = diccionario_freeling[primera_letra]["Tipo"][segunda_letra]
        else:
            adp_tipo = ""
        if tercera_letra in diccionario_freeling[primera_letra]["Forma"]:
            adp_forma = diccionario_freeling[primera_letra]["Forma"][tercera_letra]
        else:
            adp_forma = ""
        resultado_del_etiquetado = f"{adp_cat} "
        resultado_del_etiquetado += f"{adp_tipo} "
        resultado_del_etiquetado += f"{adp_forma} "
    elif primera_letra == "F":  # Puntuacion
        punct_cat = diccionario_freeling[primera_letra]["Categoria"]
        # patron = re.compile(r'F[a-z]]')
        # if patron.match(codigo):
        resultado_del_etiquetado = punct_cat
    elif primera_letra == "Z":  # Cifra
        cif_cat = diccionario_freeling[primera_letra]["Categoria"]
        resultado_del_etiquetado = cif_cat
    return resultado_del_etiquetado


# endregion


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug=True)
