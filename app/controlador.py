"""Controlador"""

import modelo
import vista
import json
import requests
import utils
import utilsGenHeaders

class Api:
    """Clase para Api."""

    def __init__(self, headers):
        self.headers = headers
        self.urlApi = utils.urlApi

    def enviarFactura(self, factura):
        """
        enviarFactura(): Método encargado de enviar a la API de Alegra una factura.
        Params: dict factura: Factura a enviar.
        Retorna respuesta http
        """
        payload = Api.construirFactura(self = self, factura = factura)
        respuesta = requests.post(url = self.urlApi + "invoices/",
                    headers = self.headers, data = json.dumps(payload))
        return respuesta
    
    def construirFactura(self, factura):
        """
        construirFactura(): Método encargado de construir factura.
        Params: dict factura: Factura a enviar.
        Retorna payload con factura construida.
        """
        idCliente = Api.getClientById(self = self, identification = factura['clienteid'])
        idProducto = Api.getProductById(self = self, referenciaProd = factura['referencia'])

        payload = {                                         #Obligatorios.
            'date': str(factura['fecha'].date()),           #Fecha de creación de la factura.
            'dueDate': str(factura['fechavencimiento'].date()),        #Fecha de vencimiento des la factura.
            'anotation' : """Favor consignar en la cta de ahorros Bancolombia #412 
            00 00 0219 o en cta ahorros Davivienda #39 4000 054 707 a nombre de Samuel Rendon SAS.""", #TODO Anotaciones en txt
            'termsConditions' : terminosCondiciones(),            
            'paymentMethod' :str(factura['formapago']),
            'client': idCliente,                            #Id del cliente.
            'items' : [                                     #Lista de prod/serv asociados a la factura.
                {
                    'id': idProducto,                       #Identificador prod/serv.
                    'price': factura['precio'],             #Precio venta del producto.
                    'quantity': factura['cantidad'],        #Cantidad vendida del prod/serv.                    
                    'reference' : factura['referencia']
                }
            ]
        }
        return payload
    
    def enviarRemision(self, remision):
        """
        enviarRemision(): Método encargado de enviar a la API de Alegra una remisión.
        Params: dict remision: Remisión a enviar.
        Retorna respuesta http.
        """
        payload = Api.construirRemision(self = self, remision = remision)
        respuesta = requests.post(url = self.urlApi + "remissions/",
                    headers = self.headers, data = json.dumps(payload))
        return respuesta
    
    def construirRemision(self, remision):
        """
        construirRemision(): Método encargado de construir remision.
        Params: dict remision: Remision a enviar.
        Retorna payload con remision construida.
        """
        idCliente = Api.getClientById(self = self, identification = remision['clienteid'])
        idProducto = Api.getProductById(self = self, referenciaProd = remision['referencia'])
        payload = {                                      #Obligatorios.
            'date': str(remision['fecha'].date()),       #Fecha de creación de la factura.
            'dueDate': str(remision['fechavencimiento'].date()),    #Fecha de vencimiento de la factura.
            'client': idCliente,                         #Id del cliente.
            'anotation' : str(remision['transportadora']) + ' ' + str(remision['guia']) 
                        + '*' + str(remision['numeropaquetes']),
            'termsConditions' : terminosCondiciones(),
            'items' : [                                  #Lista de prod/serv asociados a la factura.
                {
                    'id': idProducto,                    #Identificador prod/serv.
                    'price': remision['precio'],         #Precio venta del producto.
                    'quantity': remision['cantidad'],    #Cantidad vendida del prod/serv. 
                    'reference': remision['referencia']
                }
            ]
        }
        return payload
    
    def getClientById(self, identification):
        """
        getClientById(): Método encargado de consultar un cliente por su identificación.
        Params: int identificacion: Identificación del cliente.
        Retorna int, id del cliente.
        """
        params = {
            "identification" : identification,
            "order_field" : "id",
            "limit"  : 1
        }
        response = requests.get(url = self.urlApi + "contacts/",
                headers = self.headers, params = params)
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
        response = requests.get(url = self.urlApi + "items/",
                headers = self.headers, params = params)
        return json.loads(response.text)[0]['id']

def terminosCondiciones():
    "Para leer txt de terminos y condiciones."
    variables = []
    with open(utils.pathTermsCond, 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            variables.append(linea.strip('\n'))
    return variables[0]

def procesarRegistro(registro):
    """
    handleRecords(): Método encargado de manejar cada registro.
    Params: list registro: registro.
    """ 
    headersApi = utilsGenHeaders.genBasicToken() #TODO Refactor
    api = Api(headers = headersApi)
    regIndx = registro[0]
    registro = registro[1]

    if registro['fact/remis'].lower() == 'facturado':
        response = api.enviarFactura(factura = registro)
    elif registro['fact/remis'].lower() == 'remisionado':
        response = api.enviarRemision(remision = registro)
    
    if response.status_code == 201:                        
        excel = modelo.archivoExcel(pathExcel = utils.pathExcelFile)
        excel.guardarFacturados(registro = registro)
        return regIndx            

def main():

    vista.starView()
    excel = modelo.archivoExcel(pathExcel = utils.pathExcelFile)
    registros = excel.leerRegistrosPendientes()
    registrosBorrar = map(procesarRegistro, list(enumerate(registros)))    
    excel.borrarPendientes(registros = registrosBorrar)
    vista.endView()

if __name__ == '__main__':
    main()

#TODO Generar token solo al inicio del programa.
#TODO Resiliente a caidas de red, a archivo abierto.
#TODO tax == IVA? Objeto
#TODO Tolerar que los llamados no funcionen.