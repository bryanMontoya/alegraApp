import base64
config = 'correo1@email.com' + ":" + 'cde5317c284098ec0ac2'
BASICTOKEN = base64.b64encode(config.encode('ascii')).decode('ascii')
headersApi = {
        "Authorization" : "Basic " + BASICTOKEN
        }

print(headersApi['Authorization'])