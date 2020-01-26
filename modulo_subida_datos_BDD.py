import pymysql
import pymysql.cursors


# * Dependencias requeridas para el módulo.


class ObjetoJSONParaSubir:
    def __init__(self, empresa, experiencia, telefono, pregunta, respuesta, hora, fecha):
        # ? Esta clase fue creada para modelizar la rececpión de datos desde el CHATBOT.
        self.empresa = empresa
        self.experiencia = experiencia
        self.telefono = telefono
        self.pregunta = pregunta
        self.respuesta = respuesta
        self.fecha = fecha
        self.hora = hora


def db2string(vsql):
    dbServer = 'localhost'  # ip del servidor
    dbUser = 'pad'  # usurio autorizado para leer la base de datos
    dbPass = 'dalas'  # clave de la base de datos
    dbBase = 'pad2'  # nombre de la base de datos
    resultado = ""
    db = pymysql.connect(host=dbServer, user=dbUser, passwd=dbPass, db=dbBase, cursorclass=pymysql.cursors.DictCursor,
                         database="mysql")
    cursor = db.cursor()
    cursor.execute(vsql)
    resultado = cursor.fetchall()
    return resultado


def subir_esta_informacion_a_BDD(objeto_recibido_de_chatbot):
    # * objeto_recibido_de_chatbot representa la información brindada por el CHATBOT

    empresa = objeto_recibido_de_chatbot["empresa"]
    experiencia = objeto_recibido_de_chatbot["experiencia"]
    numtelefono = objeto_recibido_de_chatbot["numtelefono"]
    pregunta = objeto_recibido_de_chatbot["respuesta"]
    respuesta = objeto_recibido_de_chatbot["pregunta"]
    hora = objeto_recibido_de_chatbot["hora"]
    fecha = objeto_recibido_de_chatbot["fecha"]
    Objeto_para_consulta = ObjetoJSONParaSubir(
        # ! Instanciación de la clase previamente declarada "ObjetoJSONParaSubir"
        empresa, experiencia, numtelefono, pregunta, respuesta, hora, fecha)

    var_empresa = '"' + str(Objeto_para_consulta.empresa) + '"'
    var_experiencia = '"' + str(Objeto_para_consulta.experiencia) + '"'
    var_telefono = '"' + str(Objeto_para_consulta.telefono) + '"'
    var_pregunta = '"' + str(Objeto_para_consulta.pregunta) + '"'
    var_respuesta = '"' + str(Objeto_para_consulta.respuesta) + '"'
    var_fecha = '"' + str(Objeto_para_consulta.fecha) + '"'
    var_hora = '"' + str(Objeto_para_consulta.hora) + '"'



    consulta = f"INSERT INTO pad2.datos( pad2.datos.id, pad2.datos.empresa, pad2.datos.experiencia, pad2.datos.numtelefono, pad2.datos.pregunta, pad2.datos.respuesta, pad2.datos.hora, pad2.datos.fecha ) VALUES( NULL, {var_empresa}, {var_experiencia}, {var_telefono}, {var_pregunta}, {var_respuesta}, {var_hora}, {var_fecha} )"
    # ! Se ejecuta la consulta
    db2string(consulta)
