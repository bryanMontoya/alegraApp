a = [{"a": "b"}, {"c": "g"}, {"j": "ñ"}]

x = list(enumerate(a))

print(x)


def myfuncion(valor):
    valor['hola'] = 'amigos'
    return valor
    
z = map(myfuncion, a)

print(list(z))
'''


def addition(n):
    return n + n
  
# We double all numbers using map()
numbers = (1, 2, 3, 4)
result = map(addition, numbers)
print(list(result))'''