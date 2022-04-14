"""Class Invoice."""

#Sección de importación de librerías.
import json
import requests

class Invoice:
    """Clase para factura."""

    def __init__(self, date, dueDate, client, itemId, itemPrice, itemQuantity):
        self.date = date
        self.dueDate = dueDate
        self.client = client
        self.itemId = itemId
        self.itemPrice = itemPrice
        self.itemQuantity = itemQuantity

    def sendInvoice(self):
        """
        sendInvoice(): Método encargado de enviar a la API de Alegra las facturas.

        Params:
        None

        Return is None
        """
        headers = {
            "Authorization" :
            "Basic Ym1vbnRveWFvc29yaW9zQGdtYWlsLmNvbTo5MzY1NGNlYjA2NTZlZjRlZThkNg=="
            }

        payload = {                                 #Obligatorios.
            'date': self.date,                      #Fecha de creación de la factura.
            'dueDate': self.date,                   #Fecha de vencimiento de la factura.
            'client': self.client,                  #Id del cliente.
            'items' : [                             #Lista de prod/serv asociados a la factura.
                {
                    'id': self.itemId,              #Identificador prod/serv.
                    'price': self.itemPrice,        #Precio venta del producto.
                    'quantity': self.itemQuantity   #Cantidad vendida del prod/serv.
                }
            ],
            'termsConditions' : """Favor llamar antes de consignar al cel 3117667434 para asignación de cuenta. Favor hacer el pago por medio de un PAC de Bancolombia o corresponsal bancario."""
        }

        #Crear factura de venta.
        response = requests.post(url = "https://api.alegra.com/api/v1/invoices",
                    headers = headers, data = json.dumps(payload))

        return response
