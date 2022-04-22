"""import base64

message = "ycarro9@gmail.com:db26135789f64e9f64eb"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print(base64_message)"""


import requests
import json

headers = {
            "Authorization" :
            "Basic eWNhcnJvOUBnbWFpbC5jb206ZGIyNjEzNTc4OWY2NGU5ZjY0ZWI="
            }

#Nombre exacto del cliente. Si hay dos clientes?
params = {"identification" : 12345,
          "limit"  : 1,
          "order_field" : "identification"
        }

#Obtener id del cliente a través del nombre para crear factura de venta.
response = requests.get(url = "https://api.alegra.com/api/v1/contacts/",
                headers = headers, params = params)

print(json.loads(response.text)[0]['id'])

"""
#Nombre exacto del producto.
params = {"name" : "clavos"}
#Obtener id del producto a través del nombre para crear factura de venta.
response = requests.get(url = "https://api.alegra.com/api/v1/items/",
                headers = headers, params = params)

print(response.status_code)
print(response.text)
"""