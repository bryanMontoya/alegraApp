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

def validar_tax(tax):
    """Valida el id a enviar de acuerdo al iva en el excel."""
    if (tax == 0.19 or tax == 19):
        return 3
    elif (tax == 0.05 or tax == 5):
        return 2
    return 1