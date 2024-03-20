import json
import requests

import utils
from alegra.authorization.authorization import Authorization

class AlegraService:

    def __init__(self):
        self._headers = Authorization()
        self._url = utils.leer_config()['rutas']['apiAlegra']

    def load_invoce(self, payload):
        """Carga a la API de Alegra una factura.
        Params: dict payload: Factura a enviar."""
        return requests.post(url = self._url + "invoices/",
                    headers = self._headers, data = json.dumps(payload))        

    def load_remission(self, payload):
        """Cargar a la API una remisión.
        Params: dict payload: Remision a enviar."""
        return requests.post(url = self._url_api + "remissions/",
                    headers = self._headers, data = json.dumps(payload))

    def load_estimate(self, payload):
        """Cargar a la API una cotizacion.
        Params: dict payload: Cotizacion a enviar."""
        return requests.post(url = self._url_api + "estimates/",
                    headers = self._headers, data = json.dumps(payload))        

    def get_client_by_id(self, id):
        """Consultar un cliente por su identificación.
        Params: int identificacion: Identificación del cliente.
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
        """Consultar el id de un producto dado su referencia.
        Params: str referenciaProd: Referencia.
        Retorna id del producto."""
        params = {
            "reference" : int(reference),
            "order_field" : "id",
            "limit"  : 1
        }
        response = requests.get(url = self._url + "items/",
                headers = self._headers, params = params)
        return json.loads(response.text)[0]['id']
