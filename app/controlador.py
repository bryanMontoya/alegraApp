"""Controlador"""

import modelo
import vista
import json
import requests
import utils
import utilsGenHeaders

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
        respuesta = requests.post(url = self._urlApi + "invoices/",
                    headers = self._headers, data = json.dumps(payload))
        return respuesta

    def enviarRemision(self, payload):
        """
        enviarRemision(): Método encargado de enviar a la API de Alegra una remisión.
        Params: dict payload: Remisión a enviar.
        Retorna respuesta http.
        """        
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
        #TODO Tolerar que no se encuentre el cliente.

    def getProductById(self, referenciaProd):
        """
        getProductById(): Método encargado de consultar el id de un producto dado su referencia.
        Params: str referenciaProd: Referencia.
        Retorna int, id del producto.
        """
        params = {
            "reference" : int(referenciaProd),
            "order_field" : "id",
            "limit"  : 1
        }
        response = requests.get(url = self._urlApi + "items/",
                headers = self._headers, params = params)
        return json.loads(response.text)[0]['id']
        #TODO Tolerar que no se encuentre la referencia del producto.

def procesarEnviables(conjuntoRegistros):
        """
        procesarEnviables(): Método encargado de procesar enviable sea remision o factura.
        Params: 
        Retorna payload con enviable construido.
        """
        api = Api()        
        api.setHeaders(utilsGenHeaders.genBasicToken())
        api.setUrlApi(utils.urlApi)

        registroPrincipal = conjuntoRegistros[0]        
                
        idCliente = api.getClientById(identification = registroPrincipal['clienteid'])        
        payload = {
            'date': str(registroPrincipal['fecha'].date()),
            'dueDate': str(registroPrincipal['fechavencimiento'].date()),
            'client': idCliente,            
            'termsConditions' : terminosCondiciones()
        }

        items = []
        for registro in conjuntoRegistros:
            idProducto = api.getProductById(referenciaProd = registro['referencia'])        
            item = {
                'id': idProducto,
                'price': registro['precio'],
                'quantity': registro['cantidad'],   
                'reference': registro['referencia']
            }            
            items.append(item)                              
        payload['items'] = items                

        #Para campos que no se comparten.
        if registroPrincipal['fact / remis'].lower() == 'facturado':
            payload['anotation'] = """Favor consignar en la cta de ahorros Bancolombia #412 
                    00 00 0219 o en cta ahorros Davivienda #39 4000 054 707 a nombre de Samuel Rendon SAS.""", #TODO Anotaciones en txt
            respuesta = api.enviarFactura(payload)
        elif registroPrincipal['fact / remis'].lower() == 'remisionado':
            payload['anotation'] = str(registroPrincipal['transportadora']) + ' ' + str(registroPrincipal['guia']) + '*' + str(registroPrincipal['numeropaquetes'])
            respuesta = api.enviarRemision(payload)

        print(respuesta)                    
    
    #TODO status code respuesta api.
'''if response.status_code == 201:                        
        excel = modelo.archivoExcel(pathExcel = utils.pathExcelFile)
        excel.guardarFacturados(registro = registro)
        return regIndx     '''

def procesarConjuntos(registrosPendientes, registrosVaciosIndex):
    """procesarConjuntos: Identificar productos que pertenecen a un mismo cliente.
    Debido a la estructura del archivo de excel, donde para un cliente se apilan los diferentes productos.
    """
    conjunto = []
    for i, j in enumerate(registrosPendientes):
        if (i not in registrosVaciosIndex):
            #Juntar registros pertenecientes a mismo enviable.
            conjunto.append(j)
        else:
            if (len(conjunto) > 0):
                #Procesar conjunto de registros.
                procesarEnviables(conjuntoRegistros = conjunto)
                conjunto.clear()
    else:
        if (len(conjunto) > 0):
            #Procesar conjunto de registros.
            procesarEnviables(conjuntoRegistros = conjunto)

def main():

    #vista.starView()
    excelEnviables = modelo.archivoExcel(pathExcel = utils.pathExcelFile)
    registrosPendientes, registrosVacios = excelEnviables.leerRegistrosPendientes()    
    procesarConjuntos(registrosPendientes, registrosVacios)
    #registrosBorrar = map(procesarRegistro, list(enumerate(registros)))
    #excel.borrarPendientes(registros = registrosBorrar)
    #vista.endView()

def terminosCondiciones():
    "Para leer txt de terminos y condiciones."
    variables = []
    with open(utils.pathTermsCond, 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            variables.append(linea.strip('\n'))
    return variables[0]

if __name__ == '__main__':
    main()    

#TODO Generar token solo al inicio del programa.
#TODO Resiliente a caidas de red.
#TODO tax == IVA? Objeto
#TODO Tolerar que los llamados no funcionen.