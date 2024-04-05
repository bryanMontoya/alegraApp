from collections import Counter
from openpyxl import load_workbook

import pandas as pd
import numpy as np

class ExcelFile:
    """Clase para archivo de excel."""
    SHEET_NAME = "ENVIABLES"
    LOADED_STATE = "Cargado"
    PATH_EXCEL = "Registros.xlsx"

    def __init__(self):
        self.path = self.PATH_EXCEL
        self.__registros = None
        self.__vacias = None

    def read(self):
        """Retorna lista de registros pendientes y lista con la posicion de registros vacios."""        
        df = pd.read_excel(
            self.path,
            index_col = None,
            sheet_name = self.SHEET_NAME,
            usecols = "A:Z"
            )
        #Espacios en blanco como Nan.
        df = df.replace(r'^\s*$', np.NaN, regex = True)
        #Saber cuales filas son vacias.
        nulos = Counter(np.where(pd.isnull(df))[0]).most_common()
        self.__vacias = [x[0] for x in nulos if x[1] == len(df.columns)]
        #Conocer nombres columnas.
        columnas = [key.lower() for key in df.columns]
        registros = df.values.tolist()
        #Convertir dataframe a una lista de diccionarios.
        self.__registros = [{colum:factura[columnas.index(colum)] for colum in columnas} for factura in registros]
        return self.__registros, self.__vacias

    def map_to_registry():
        """Mapear registros a objeto."""
        pass
    
    def cambiar_estado(self, registro):
        """Cambiar estado de columna Pendiente a Cargado."""
        workbook = load_workbook(filename = self.path)
        sheet = workbook.active
        space = "Z" + str(registro + 2)
        sheet[space] = self.LOADED_STATE
        workbook.save(filename = self.path)
