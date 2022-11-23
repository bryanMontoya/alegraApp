"""Porción de código que se puede usar para generar token manualmente y poderlo usar en una herramienta como postman."""

import base64
config = 'correo3@gmail.com' + ":" + '27ab0f21365573156b0e'
BASICTOKEN = base64.b64encode(config.encode('ascii')).decode('ascii')
headersApi = {
        "Authorization" : "Basic " + BASICTOKEN
        }

print(headersApi['Authorization'])