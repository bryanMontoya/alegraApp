"""Modelo"""

import pandas as pd

class archivoExcel:
    """Clase para archivo de excel."""

    def __init__(self, pathExcel):
        self.path = pathExcel
        self.__registrosPendientes = None

    def leerRegistrosPendientes(self):
        """
        leer(): Método encargado de leer el documento de excel, y retornar los registros en
        como lista de diccionarios.
        Retorna Lista.
        """
        #Leer excel como dataframe, extraer columnas y registros.
        df = pd.read_excel(self.path, index_col = None, sheet_name = "Pendientes")
        columnas = [key.lower() for key in df.columns]
        registros = df.values.tolist()

        #Convertir dataframe a una lista de diccionarios.
        self.__registrosPendientes = [{colum:factura[columnas.index(colum)] for colum in columnas} for factura in registros]
        return self.__registrosPendientes

    def guardarFacturados(self, registro):
        """
        guardar(): Método encargado de apilar factura enviada en nueva hoja de excel de
        nombre 'Facturados'.
        Params:
        dict registro: Registros a guardar.
        """
        df = pd.read_excel(self.path, index_col = None, sheet_name = 'Facturados')
        df.loc[len(df.values) + 1] = registro.values()
        with pd.ExcelWriter(self.path, engine = 'openpyxl', mode ='a', if_sheet_exists = 'replace') as writer:
            df.to_excel(writer, 'Facturados', index = False)

    def borrarPendientes(self, registros):
        """
        borrar(): Método encargado de eliminar registros enviados de hoja de nombre
        nombre 'Pendientes'.
        Params:
        list registros: Registros a borrar.
        """
        df = pd.read_excel(self.path, index_col = None, sheet_name = 'Pendientes')

        for registro in registros:
            df = df.drop([registro])

        with pd.ExcelWriter(self.path, engine = 'openpyxl', mode = 'a', if_sheet_exists = 'replace') as writer:
            df.to_excel(writer, 'Pendientes', index = False)
