"""Alegra App."""

#Sección de importación de librerías.
import pandas as pd
from classes import excelFile, invoice

path = 'data - copia.xlsx'

def main():
    """
    main(): Método principal.

    Return is None
    """       
    excel = excelFile.ExcelFile(path = path)
    invoices = excel.readExcel()

    df = pd.read_excel(path, index_col = None, sheet_name = 'Pendientes')
    for indexInvoice, anInvoice in enumerate(invoices):        

        invoiceObject = invoice.Invoice(anInvoice)
        response = invoiceObject.sendInvoice()

        if response.status_code == 201:
            excel.saveInvoice(invoice = anInvoice)
            df = df.drop([indexInvoice])  
    
    with pd.ExcelWriter(path, engine = 'openpyxl', mode = 'a', if_sheet_exists = 'replace') as writer:
        df.to_excel(writer, 'Pendientes', index = False)                  

if __name__ == '__main__':
    main()
