#Sección de importación de librerías.
import pandas as pd
import json
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
    
    Return type is None    
    """
    payload = {
            "date": "2015-11-15",
            "dueDate": "2015-12-15",
            "client":  1,
            "items" : [
            {
                "id": 1,
                "price" : 120,
                "quantity" : 5    
            }
            ]
        }
    headers = {
            "Authorization" : 
            "Basic Ym1vbnRveWFvc29yaW9zQGdtYWlsLmNvbTo5MzY1NGNlYjA2NTZlZjRlZThkNg=="
            }      

    for invoice in pendingInvoices:                                                  
        try:
            #request = requests.post(url = "https://api.alegra.com/api/v1/invoices",
            #            headers = headers, data = json.dumps(payload))
            #if request.status_code == 200:
                saveInvoice(invoice = invoice)            
        except:
            ...

def saveInvoice(invoice : dict):
    """
    saveInvoice(): Método encargado de apilar factura enviada en nueva hoja de excel de 
    nombre 'Facturados'.

    Params:
        dict invoice: Factura a guardar.

    Return type is None.

    """
    df = pd.read_excel('data - copia.xlsx', index_col = None, sheet_name = 'Facturados')    
    df.loc[len(df.values) + 1] = invoice.values()
    with pd.ExcelWriter('data - copia.xlsx', engine = 'openpyxl', mode ='a', if_sheet_exists = 'replace') as writer:
        df.to_excel(writer, 'Facturados', index = False)

def main():
    """
    main(): Método principal.    
    """
    pendingInvoices = readExcel()        
    sendInvoice(pendingInvoices = pendingInvoices)

if __name__ == '__main__':
    main()

#TODO factura: list or dic.
#TODO: Creación de cliente en alegra.
#TODO: Creación de producto en alegra.
#TODO: Delete invoice from Pendientes when sending.