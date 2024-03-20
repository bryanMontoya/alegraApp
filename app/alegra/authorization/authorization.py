import base64
from helpers.helpers import load_env

class Authorization:
    def __init__(self):
        self.headers = self._generate_token()

    def _generate_token(self):
        variables = []
        with open(load_env['rutas']['credenciales'], 'r') as file:
            lines = file.readlines()
            for line in lines:
                variables.append(line.strip('\n'))
        EMAIL = variables[0]
        TOKEN = variables[1]

        config = f"{EMAIL}:{TOKEN}"
        BASICTOKEN = base64.b64encode(config.encode('ascii')).decode('ascii')
        headers = {"Authorization": f"Basic {BASICTOKEN}"}
        return headers
