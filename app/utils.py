"""
import  pandas  as pd
from pandas import DataFrame
 
#Leer
data = pd.read_excel('dataCopy.xlsx')
 #Ver todos los valores
print(data.values)
 #Ver el valor de la primera fila
print(data.values[0])
 
#Ver todos los valores en una columna
print(data['Estado'].values)
 
#Añadir columna
print("-----------------------")
 #Añadir fila
data.loc[2,'Estado'] = 'Enviado'
data.loc[3,'Estado'] = 'Por enviar 2'
 
 #Salvar
DataFrame(data).to_excel('1.xlsx', sheet_name='Sheet1', index=False, header=True)


a = ['a' ,'b' ,'c' , 'd']

for numcol, col in enumerate(a):
    print(numcol, col)
    
import requests
import base64
import json

message = "bmontoyaosorios@gmail.com:93654ceb0656ef4ee8d6"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print(base64_message)
"""
import pandas as pd
df = pd.read_excel('data - copia.xlsx', index_col = None, sheet_name = "Pendientes")  