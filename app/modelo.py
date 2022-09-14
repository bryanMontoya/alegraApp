"""Modelo"""

import pandas as pd
import numpy as np
from collections import Counter

class archivoExcel:
    """Clase para archivo de excel."""

    def __init__(self, pathExcel):
        self.path = pathExcel
        self.__registrosPendientes = None
        self.__vacias = None

    def leerRegistrosPendientes(self):
        """
        leer(): Método encargado de leer el documento de excel.
        Retorna Lista de registros pendientes y lista con la posicion de registros vacios.
        """        
        df = pd.read_excel(self.path, index_col = None, sheet_name = "ENVIABLES")   #Leer excel como dataframe, extraer columnas y registros.
        df = df.replace(r'^\s*$', np.NaN, regex = True)             #Espacios en blanco como Nan.
        nulos = Counter(np.where(pd.isnull(df))[0]).most_common()   #Saber cuales filas son vacias.        
        self.__vacias = [x[0] for x in nulos if x[1] == 22]        

        #Conocer nombres columnas.
        columnas = [key.lower() for key in df.columns]
        registros = df.values.tolist()

        #Convertir dataframe a una lista de diccionarios.
        self.__registrosPendientes = [{colum:factura[columnas.index(colum)] for colum in columnas} for factura in registros]
        return self.__registrosPendientes, self.__vacias

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
