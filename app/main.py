"""Alegra App."""
#Sección de importación de librerías.
import json
import pandas as pd
import requests

def readExcel() -> list:
    """
    readExcel(): Método encargado de leer el documento de excel, y convertir los registros en
        una lista de diccionarios.

    Params:
    None

    Return type is list.

    """
    #Leer excel como dataframe, extraer columnas y registros.
    df = pd.read_excel('data - copia.xlsx', index_col = None, sheet_name = "Pendientes")
    columns = [key.lower() for key in df.columns]
    listInvoices = df.values.tolist()

    #Convertir dataframe a una lista de diccionarios.
    invoices = [{colum:factura[columns.index(colum)] for colum in columns} for factura in listInvoices]

    return invoices

def sendInvoice(pendingInvoices : list):
    """
    sendInvoice(): Método encargado de enviar a la API de Alegra las facturas.

    Params:
        list pendingInvoices: Facturas pendientes por enviar.
    
    Return is None
    
    """
    df = pd.read_excel('data - copia.xlsx', index_col = None, sheet_name = 'Pendientes')
    #TODO: Creación de cliente en alegra. Por defecto id:1.
    #TODO: Creación de producto/servicio en alegra. Por defecto id:1.

    headers = {
            "Authorization" :
            "Basic Ym1vbnRveWFvc29yaW9zQGdtYWlsLmNvbTo5MzY1NGNlYjA2NTZlZjRlZThkNg=="
            }

    for i in range(len(pendingInvoices)):
        invoice = pendingInvoices[i]

        payload = {                                 #Obligatorios.
            'date': str(invoice['fecha'].date()),   #Fecha de creación de la factura.
            'dueDate': str(invoice['fecha'].date()),#Fecha de vencimiento de la factura.
            'client': 1,                            #Id del cliente.
            'items' : [                             #Lista de prod/serv asociados a la factura.
                {
                    'id': invoice['referencia'],    #Identificador prod/serv.
                    'price': invoice['precio'],     #Precio venta del producto.
                    'quantity': invoice['cantidad'],#Cantidad vendida del prod/serv.
                }
            ],
            'termsConditions' : """Favor llamar antes de consignar al cel 3117667434 para asignación de cuenta. Favor hacer el pago por medio de un PAC de Bancolombia o corresponsal bancario.""",
            'status': 'open',
            'paymentForm': 'CREDIT'
        }

        request = requests.post(url = "https://api.alegra.com/api/v1/invoices",
                    headers = headers, data = json.dumps(payload))

        print(request.status_code)
        print(request.text)
        if request.status_code == 201:
            saveInvoice(invoice = invoice)   
            df = df.drop([i])    
            
    with pd.ExcelWriter('data - copia.xlsx', engine = 'openpyxl', mode ='a', if_sheet_exists = 'replace') as writer:
        df.to_excel(writer, 'Pendientes', index = False)

def saveInvoice(invoice : dict):
    """
    saveInvoice(): Método encargado de apilar factura enviada en nueva hoja de excel de
    nombre 'Facturados'.

    Params:
        dict invoice: Factura a guardar.

    Return is None.

    """
    df = pd.read_excel('data - copia.xlsx', index_col = None, sheet_name = 'Facturados')
    df.loc[len(df.values) + 1] = invoice.values()
    with pd.ExcelWriter('data - copia.xlsx', engine = 'openpyxl', mode ='a', if_sheet_exists = 'replace') as writer:
        df.to_excel(writer, 'Facturados', index = False)

def main():
    """
    main(): Método principal.

    Return is None
    """
    pendingInvoices = readExcel()
    sendInvoice(pendingInvoices = pendingInvoices)

if __name__ == '__main__':
    main()
