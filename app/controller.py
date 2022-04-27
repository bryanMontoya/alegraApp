"""Controller"""

import view
import model
import utils
import json
import requests

class Api:
    """Clase para Api."""

    def __init__(self, headers):
        self.headers = headers
        self.urlApi = utils.urlApi

    def sendInvoice(self, invoice):
        """
        sendInvoice(): Método encargado de enviar a la API de Alegra una factura.

        Params:
        dict Invoice: Factura a enviar.

        Return is the http response
        """

        idClient = self.getClientById(identification = invoice['clientedni'])
        idProduct = self.getProductByName(nameProd = invoice['referencia'])
        
        payload = {                                     #Obligatorios.
            'date': str(invoice['fecha'].date()),       #Fecha de creación de la factura.
            'dueDate': str(invoice['fecha'].date()),    #Fecha de vencimiento de la factura.
            'client': idClient,                         #Id del cliente.
            'items' : [                                 #Lista de prod/serv asociados a la factura.
                {
                    'id': idProduct,                    #Identificador prod/serv.
                    'price': invoice['precio'],         #Precio venta del producto.
                    'quantity': invoice['cantidad']     #Cantidad vendida del prod/serv.
                }
            ],
            'termsConditions' : """Favor llamar antes de consignar al cel 3117667434 para asignación de cuenta. 
                            Favor hacer el pago por medio de un PAC de Bancolombia o corresponsal bancario."""
        }

        #Crear factura de venta.
        response = requests.post(url = self.urlApi + "invoices/",
                    headers = self.headers, data = json.dumps(payload))

        return response

    def sendRemission(self, remission):
        """
        sendRemission(): Método encargado de enviar a la API de Alegra una remisión.

        Params:
        dict remission: Remisión a enviar.

        Return is the http response
        """

        idClient = self.getClientById(identification = remission['clientedni'])
        idProduct = self.getProductByName(nameProd = remission['referencia'])

        payload = {                                       #Obligatorios.
            'date': str(remission['fecha'].date()),       #Fecha de creación de la factura.
            'dueDate': str(remission['fecha'].date()),    #Fecha de vencimiento de la factura.
            'client': idClient,                           #Id del cliente.
            'items' : [                                   #Lista de prod/serv asociados a la factura.
                {
                    'id': idProduct,                      #Identificador prod/serv.
                    'price': remission['precio'],         #Precio venta del producto.
                    'quantity': remission['cantidad']     #Cantidad vendida del prod/serv.
                }
            ],
            'termsConditions' : """Favor llamar antes de consignar al cel 3117667434 para asignación de cuenta. Favor hacer el pago por medio de un PAC de Bancolombia o corresponsal bancario."""
        }

        #Crear remision.
        response = requests.post(url = self.urlApi + "remissions/",
                    headers = self.headers, data = json.dumps(payload))

        return response
    
    def getClientById(self, identification):
        """
        getClientById(): Método encargado de consultar un cliente por su identificación.

        Params:
        int identification: Identificación del cliente.

        Return type is int, id del cliente.
        """
        params = {
            "identification" : identification,
            "order_field" : "identificacion",
            "limit"  : 1
        }

        #Obtener id del cliente a través de la identificación.
        response = requests.get(url = self.urlApi + "contacts/",
                headers = self.headers, params = params)

        return json.loads(response.text)[0]['id']

    def getProductByName(self, nameProd):
        """
        getProductByName(): Método encargado de consultar el id de un producto dado su nombre.

        Params:
        str nameProd: Nombre del producto.

        Return type is int, id del producto.
        """
        params = {
            "name" : nameProd,
            "order_field" : "name",
            "limit"  : 1
        }

        #Obtener id del producto a través del nombre.
        response = requests.get(url = self.urlApi + "items/",
                headers = self.headers, params = params)

        return json.loads(response.text)[0]['id']

def handleRecords(records, excel, api):
    """
    handleRecords(): Método encargado de manejar cada registro.

    Params:
    list records: registros.
    obj excel: objecto de tipo excel.
    obj api: objeto de tipo api.

    Return type is list, registros a borrar.
    """

    recordsToDelete = []
    for indexRecord, record in enumerate(records):
        
        if record['fact/remis'].lower() == 'facturado':
            response = api.sendInvoice(invoice = record)
        elif record['fact/remis'].lower() == 'remisionado':
            response = api.sendRemission(remission = record)

        if response.status_code == 201:
            excel.save(record = record)
            recordsToDelete.append(indexRecord)
    
    return recordsToDelete

def main():
    """
    main(): Método principal.

    Return is None
    """
    view.starView()

    excel = model.ExcelFile()
    records = excel.read()
    apiObject = Api(headers = utils.headersApi)
    recordsToDelete = handleRecords(records = records, excel = excel, api = apiObject)
    excel.delete(recordsToDelete = recordsToDelete)

    view.endView()

if __name__ == '__main__':
    main()

#TODO Headers, certifieds.
#TODO Utils info.Terms and conditions.
#TODO Construir Json específico para Remision/Factura.
#TODO Confiar en información del excel o la Api, ej: Precio de producto.
#TODO Fecha de Vencimiento Factura.
#TODO Cual se refiere al producto en el excel? Referencia o artículo.
#TODO Xml Facturas de compras.
#TODO Información api completa Factura/Remision.