"""Porción de código que se puede usar para generar token manualmente y poderlo usar en una herramienta como postman."""

import base64
config = 'micorreo123@email.com' + ":" + '1b1f1d93e566c8c86425'
BASICTOKEN = base64.b64encode(config.encode('ascii')).decode('ascii')
headersApi = {
        "Authorization" : "Basic " + BASICTOKEN
        }

print(headersApi['Authorization'])