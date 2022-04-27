"""Model"""

import pandas as pd
import utils

class ExcelFile:
    """Clase para archivo de excel."""

    def __init__(self):
        self.path = utils.pathExcelFile

    def read(self):
        """
        read(): Método encargado de leer el documento de excel, y retornar los registros en
        como lista de diccionarios.

        Params:
        None

        Return type is list.
        """
        #Leer excel como dataframe, extraer columnas y registros.
        df = pd.read_excel(self.path, index_col = None, sheet_name = "Pendientes")
        columns = [key.lower() for key in df.columns]
        listInvoices = df.values.tolist()

        #Convertir dataframe a una lista de diccionarios.
        invoices = [{colum:factura[columns.index(colum)] for colum in columns} for factura in listInvoices]

        return invoices

    def save(self, record):
        """
        save(): Método encargado de apilar factura enviada en nueva hoja de excel de
        nombre 'Facturados'.

        Params:
        dict invoice: Registros a guardar.

        Return is None.
        """
        df = pd.read_excel(self.path, index_col = None, sheet_name = 'Facturados')
        df.loc[len(df.values) + 1] = record.values()
        with pd.ExcelWriter(self.path, engine = 'openpyxl', mode ='a', if_sheet_exists = 'replace') as writer:
            df.to_excel(writer, 'Facturados', index = False)

    def delete(self, recordsToDelete):
        """
        delete(): Método encargado de eliminar registros enviados de hoja de nombre
        nombre 'Pendientes'.

        Params:
        list recordsToDelete: Registros a borrar.

        Return is None.
        """
        df = pd.read_excel(self.path, index_col = None, sheet_name = 'Pendientes')

        for indexRecord in recordsToDelete:
            df = df.drop([indexRecord])

        with pd.ExcelWriter(self.path, engine = 'openpyxl', mode = 'a', if_sheet_exists = 'replace') as writer:
            df.to_excel(writer, 'Pendientes', index = False)
