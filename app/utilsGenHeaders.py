"Archivo para generar Autorization Token"

import base64
import utils

def genBasicToken():
    #Se lee archivo donde se guarda email y token entregado por alegra.
    variables = []
    with open(utils.pathConfig, 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            variables.append(linea.strip('\n'))
    EMAIL = variables[0]
    TOKEN = variables[1]

    config = EMAIL + ":" + TOKEN
    BASICTOKEN = base64.b64encode(config.encode('ascii')).decode('ascii')
    headersApi = {
            "Authorization" : "Basic " + BASICTOKEN
            }

    return headersApi
