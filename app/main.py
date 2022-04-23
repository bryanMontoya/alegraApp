"""Alegra App."""

#Sección de importación de librerías.
from classes import excelFile, api

path = 'data - copia.xlsx'
headers = {
        "Authorization" :
        "Basic eWNhcnJvOUBnbWFpbC5jb206ZGIyNjEzNTc4OWY2NGU5ZjY0ZWI="
        }

def main():
    """
    main(): Método principal.

    Return is None
    """
    excel = excelFile.ExcelFile(path = path)
    records = excel.readExcel()
    recordsToDelete = []

    for indexRecord, record in enumerate(records):

        apiObject = api.Api(headers = headers)
        if record['fact/remis'].lower() == 'facturado':
            response = apiObject.sendInvoice(invoice = record)
        elif record['fact/remis'].lower() == 'remisionado':
            response = apiObject.sendRemission(remission = record)

        if response.status_code == 201:
            excel.saveRecord(record = record)
            recordsToDelete.append(indexRecord)

    excel.deletePendientes(recordsToDelete = recordsToDelete)

if __name__ == '__main__':
    main()

#TODO Misma Hoja para remisionados y facturados?
#TODO Cliente, buscarlo por el número de identificación no por el nombre. Realizar funcionalidad.
#TODO Producto, buscar producto. Realizar funcionalidad.
#TODO Construir Json específico para Remision/Factura.
#TODO Confiar en información del excel o la Api, ej: Precio de producto.
#TODO Fecha de Vencimiento Factura.
#TODO Cual se refiere al producto en el excel? Referencia o artículo.
#TODO Ruta de alegra Api como parámetro de la clase. Concatenar endpoints.
#TODO Xml Facturas de compras.
#TODO Información api completa Factura/Remision.
