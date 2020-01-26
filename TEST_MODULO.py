from modulo_subida_datos_BDD import subir_esta_informacion_a_BDD
objetoPrueba = {
    "empresa": "empresaTEST",
    "experiencia": "experienciaTEST",
    "fecha": "2020-01-25",
    "hora": "20:13:00",
    "numtelefono": "5493416419689",
    "pregunta": "¿Todo bien?",
    "respuesta": "si"
}
subir_esta_informacion_a_BDD(objetoPrueba)
