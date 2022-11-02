import yaml

def leer_config():
    """Lee archivo de configuracion y lo devuelve como diccionario."""
    with open("application.yml", "r") as stream:
        return yaml.safe_load(stream)

def leer_txt(path):
    """Para leer txt de terminos y condiciones."""
    variables = []
    with open(path, 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            variables.append(linea.strip('\n'))
    return variables[0]
