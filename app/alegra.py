import json
import requests

class Api:
    """Clase para Api."""

    def __init__(self):
        self._headers = None
        self._url_api = ""

    def get_headers(self):
        return self._headers

    def get_url(self):
        return self._url_api

    def set_headers(self, headers):
         self._headers = headers

    def set_url_api(self, url_api):
         self._url_api = url_api

    def enviar_factura(self, payload):
        """Método encargado de enviar a la API de Alegra una factura.
        Params: dict payload: Factura a enviar."""
        respuesta = requests.post(url = self._url_api + "invoices/",
                    headers = self._headers, data = json.dumps(payload))
        return respuesta

    def enviar_remision(self, payload):
        """Método encargado de enviar a la API de Alegra una remisión.
        Params: dict payload: Remisión a enviar."""
        respuesta = requests.post(url = self._url_api + "remissions/",
                    headers = self._headers, data = json.dumps(payload))
        return respuesta

    def get_client_by_id(self, identification):
        """Método encargado de consultar un cliente por su identificación.
        Params: int identificacion: Identificación del cliente.
        Retorna id del cliente."""
        params = {
            "identification" : int(identification),
            "order_field" : "id",
            "limit"  : 1
        }
        response = requests.get(url = self._url_api + "contacts/",
                headers = self._headers, params = params)
        return json.loads(response.text)[0]['id']

    def get_product_by_id(self, referencia):
        """Método encargado de consultar el id de un producto dado su referencia.
        Params: str referenciaProd: Referencia.
        Retorna id del producto."""        
        params = {
            "reference" : int(referencia),
            "order_field" : "id",
            "limit"  : 1
        }
        response = requests.get(url = self._url_api + "items/",
                headers = self._headers, params = params)
        return json.loads(response.text)[0]['id']
