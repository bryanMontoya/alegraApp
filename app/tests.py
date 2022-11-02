"""from openpyxl import load_workbook
 
#load excel file
workbook = load_workbook(filename = "Libro1 - copia.xlsx")
 
#open workbook
sheet = workbook.active
 
#modify the desired cell
sheet["X3"] = "Cargado"
 
#save the file
workbook.save(filename="Libro2 - copia.xlsx")"""

import autorizacion
import requests
import json
params = {
    "identifications" : int(2),
    "order_field" : "id",
    "limit"  : 1
}
try:
    response = requests.get(url = "https://api.alegra.com/api/v1/" + "contacts/",
        headers = autorizacion.gen_basic_token(), params = params)
    print(json.loads(response.text))
except Exception:
    print("Error de conexion")


