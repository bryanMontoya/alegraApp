"""Utiles"""

pathExcelFile = 'Libro1 - copia.xlsx'
pathConfig = "Configuracion.txt"
pathTermsCond = "TerminosCondiciones.txt"
urlApi = "https://api.alegra.com/api/v1/"

def terminosCondiciones():
    "Para leer txt de terminos y condiciones."
    variables = []
    with open(pathTermsCond, 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            variables.append(linea.strip('\n'))
    return variables[0]
