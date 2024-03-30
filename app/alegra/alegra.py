import base64
import json
import requests

from utils.helpers import read_config

class AlegraService:

    def __init__(self):
        self._headers = Authorization().headers
        self._url = read_config()['rutas']['apiAlegra']

    def load_invoce(self, payload):
        "Carga una factura"
        return requests.post(url = self._url + "invoices/",
                    headers = self._headers, data = json.dumps(payload))        

    def load_remission(self, payload):
        "Cargar una remisión."        
        return requests.post(url = self._url + "remissions/",
                    headers = self._headers, data = json.dumps(payload))

    def load_estimate(self, payload):
        "Cargar una cotizacion."
        return requests.post(url = self._url + "estimates/",
                    headers = self._headers, data = json.dumps(payload))        

    def get_client_by_id(self, id):
        """Consultar cliente por su id
        Retorna id del cliente."""
        params = {
            "identification" : int(id),
            "order_field" : "id",
            "limit"  : 1
        }
        response = requests.get(url = self._url + "contacts/",
                headers = self._headers, params = params)
        return json.loads(response.text)[0]['id']

    def get_product_by_id(self, reference):
        """Consultar producto por su referencia.
        Retorna id del producto."""
        params = {
            "reference" : int(reference),
            "order_field" : "id",
            "limit"  : 1
        }
        response = requests.get(url = self._url + "items/",
                headers = self._headers, params = params)
        return json.loads(response.text)[0]['id']

class Authorization:
    def __init__(self):
        self.headers = self._generate_token()
    
    def _read_credentials(self):
        try:
            with open(read_config()['rutas']['credenciales'], 'r') as file:
                return [line.strip('\n') for line in file.readlines()]
        except FileNotFoundError:
            print("Credentials file not found.")
            return None

    def _generate_token(self):
        variables = self._read_credentials()
        EMAIL, TOKEN = variables[0], variables[1]
        config = f"{EMAIL}:{TOKEN}"
        BASICTOKEN = base64.b64encode(config.encode('ascii')).decode('ascii')
        headers = {"Authorization" : "Basic " + BASICTOKEN}
        return headers
