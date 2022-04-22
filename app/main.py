"""Alegra App."""

#Sección de importación de librerías.
import pandas as pd
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
