"""Auth Token."""

import base64

def genAuthToken(pathConfig):
    """Genera token de autorizacion para la api."""

    email, token = __readUtiles(path = pathConfig)
    msg = email + ":" + token        
    authToken = base64.b64encode(msg.encode('ascii')).decode('ascii')
    return authToken    

def __readUtiles(path):
    """Lee archivo de configuracion config.txt"""

    params = []
    with open(path,'r') as file:
        lineas = file.readlines()
        for linea in lineas:
            params.append(linea.strip('\n'))    
    return params[0], params[1]
