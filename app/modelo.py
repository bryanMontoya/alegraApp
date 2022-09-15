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

#TODO 22 cambiar por len(columnas)
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
