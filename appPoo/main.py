"""Alegra App."""

#Sección de importación de librerías.
import pandas as pd
from classes import excelFile, invoice

def main():
    """
    main(): Método principal.

    Return is None
    """
    anInvoice = {}
    path = 'data - copia.xlsx'
    excel = excelFile.ExcelFile(invoice = anInvoice, path = path)
    invoices = excel.readExcel()

    df = pd.read_excel(path, index_col = None, sheet_name = 'Pendientes')
    for indexInvoice, anInvoice in enumerate(invoices):

        date =  str(anInvoice['fecha'].date())
        dueDate = str(anInvoice['fecha'].date())
        client =  1
        itemId =  anInvoice['referencia']
        itemPrice =  anInvoice['precio']
        itemQuantity = anInvoice['cantidad']

        invoiceObject = invoice.Invoice(date, dueDate, client, itemId, itemPrice, itemQuantity)
        response = invoiceObject.sendInvoice()

        if response.status_code == 201:
            excel.saveInvoice(invoice = anInvoice)
            df = df.drop([indexInvoice])  
    
    with pd.ExcelWriter('data - copia.xlsx', engine = 'openpyxl', mode ='a', if_sheet_exists = 'replace') as writer:
        df.to_excel(writer, 'Pendientes', index = False)                  

if __name__ == '__main__':
    main()
