"""Alegra App."""

#Sección de importación de librerías.
from atexit import register
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

    df = pd.read_excel(path, index_col = None, sheet_name = 'Pendientes')

    for indexRecord, record in enumerate(records):

        apiObject = api.Api(headers = headers)
        if record['fact/remis'].lower() == 'facturado':
            response = apiObject.sendInvoice(invoice = record)
        elif record['fact/remis'].lower() == 'remisionado':
            response = apiObject.sendRemission(remission = record)        

        if response.status_code == 201:
            excel.saveRecord(record = record)
            df = df.drop([indexRecord])

    with pd.ExcelWriter(path, engine = 'openpyxl', mode = 'a', if_sheet_exists = 'replace') as writer:
        df.to_excel(writer, 'Pendientes', index = False)

if __name__ == '__main__':
    main()
