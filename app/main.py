#Sección de importación de librerías.
import pandas as pd

def readExcel() -> list:
    """
    readExcel(): Método encargado de leer el documento de excel, y convertir los registros en 
    una lista de diccionarios.
    """
    #Leer excel como dataframe.
    df = pd.read_excel('dataCopy.xlsx', index_col = None)
    #Extraer columnas.
    columns = [key.lower() for key in df.columns]
    #Extraer registros de factura.
    listaFacturas = df.values.tolist()
    #Convertir dataframe a una lista de diccionarios.
    facturas = [{colum:factura[columns.index(colum)] for colum in columns} for factura in listaFacturas]
    return facturas

def validateState(facturas: list) -> list:
    """
    validateState(): Método encargado de validar el estado de cada registro de la lista de facturas.
    """
    facturasEnviar = [factura for factura in facturas if factura['estado'].lower() != 'enviado']
    return facturasEnviar

def sendInvoice():
    """
    sendInvoice(): Método encargado de enviar a la API de Alegra las facturas.
    """    

def changeState():
    """
    changeState(): Método encargado de cambiar el estado de cada registro de factura a Enviado.
    """


def main():
    """
    main(): Método principal.
    """
    facturas = readExcel()
    facturasEnviar = validateState(facturas = facturas)

if __name__ == '__main__':
    main()
