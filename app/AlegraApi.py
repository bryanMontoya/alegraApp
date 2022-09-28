import json
import requests

class Api:
    """Clase para Api."""

    def __init__(self):
        self._headers = None
        self._urlApi = None

    def getHeaders(self):
        return self._headers

    def getUrl(self):
        return self._urlApi

    def setHeaders(self, headers):
         self._headers = headers

    def setUrlApi(self, urlApi):
         self._urlApi = urlApi

    def enviarFactura(self, payload):
        """
        enviarFactura(): Método encargado de enviar a la API de Alegra una factura.
        Params: dict payload: Factura a enviar.
        Retorna respuesta http
        """
        print("Enviando Factura a la Api de Alegra.")
        respuesta = requests.post(url = self._urlApi + "invoices/",
                    headers = self._headers, data = json.dumps(payload))
        return respuesta

    def enviarRemision(self, payload):
        """
        enviarRemision(): Método encargado de enviar a la API de Alegra una remisión.
        Params: dict payload: Remisión a enviar.
        Retorna respuesta http.
        """
        print("Enviando Remision a la Api de Alegra.")
        respuesta = requests.post(url = self._urlApi + "remissions/",
                    headers = self._headers, data = json.dumps(payload))
        return respuesta

    def getClientById(self, identification):
        """
        getClientById(): Método encargado de consultar un cliente por su identificación.
        Params: int identificacion: Identificación del cliente.
        Retorna int, id del cliente.
        """
        params = {
            "identification" : int(identification),
            "order_field" : "id",
            "limit"  : 1
        }
        response = requests.get(url = self._urlApi + "contacts/",
                headers = self._headers, params = params)
        return json.loads(response.text)[0]['id']

    def getProductById(self, referenciaProd):
        """
        getProductById(): Método encargado de consultar el id de un producto dado su referencia.
        Params: str referenciaProd: Referencia.
        Retorna int, id del producto.
        """
        params = {
            "reference" : referenciaProd,
            "order_field" : "id",
            "limit"  : 1
        }
        response = requests.get(url = self._urlApi + "items/",
                headers = self._headers, params = params)
        return json.loads(response.text)[0]['id']
