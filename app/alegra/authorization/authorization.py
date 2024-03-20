import base64
import utils

class Authorization:
    def __init__(self):
        self.headers = self._generate_token()

    def _generate_token(self):
        variables = []
        with open(utils.leer_config()['rutas']['credenciales'], 'r') as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                variables.append(linea.strip('\n'))
        EMAIL = variables[0]
        TOKEN = variables[1]

        config = EMAIL + ":" + TOKEN
        BASICTOKEN = base64.b64encode(config.encode('ascii')).decode('ascii')
        headers = {"Authorization" : "Basic " + BASICTOKEN}
        return headers
