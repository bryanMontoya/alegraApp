"Excel class"
from collections import Counter
from openpyxl import load_workbook

import numpy as np
import pandas as pd

class Excel:
    """Clase para archivo de excel."""
    SHEET_NAME = "ENVIABLES"
    LOADED_STATE = "Cargado"
    PENDING_STATE = "Pendiente"
    PATH_EXCEL = "Registros.xlsx"

    def __init__(self):
        self.__records = []
        self.__empty_records_index = []

    @property
    def records(self):
        "Get records list"
        return self.__records

    @property
    def empty_records_index(self):
        "Get empty records index list."
        return self.__empty_records_index

    def read_file(self):
        """Retorna lista de registros pendientes y lista con la posicion de registros vacios."""
        try:
            open(self.PATH_EXCEL, "r+")
        except FileNotFoundError:
            print("Excel no encontrado. Verifica que el archivo: " + self.PATH_EXCEL + " exista")
        except PermissionError:
            print("Cierra el archivo de excel")
        else:
            df = pd.read_excel(
                self.PATH_EXCEL,
                index_col = None,
                sheet_name = self.SHEET_NAME,
                usecols = "A:Z"
                )
            #Espacios en blanco como Nan.
            df = df.replace(r'^\s*$', np.NaN, regex = True)
            #Saber cuales filas son vacias.
            nulos = Counter(np.where(pd.isnull(df))[0]).most_common()
            self.__empty_records_index = [x[0] for x in nulos if x[1] == len(df.columns)]
            #Conocer nombres columnas.
            columnas = [key.lower() for key in df.columns]
            registros = df.values.tolist()
            #Convertir dataframe a una lista de diccionarios.
            self.__records = [
                {colum:factura[columnas.index(colum)] for colum in columnas} for factura in registros
                ]
  
    def change_status_column(self, row: int):
        "Cambiar estado de columna Pendiente a Cargado"
        workbook = load_workbook(filename = self.PATH_EXCEL)
        sheet = workbook[self.SHEET_NAME]
        space = f"Z{row}"
        sheet[space] = self.LOADED_STATE
        workbook.save(filename = self.PATH_EXCEL)
