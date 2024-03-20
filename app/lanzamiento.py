import excel

from helpers.helpers import load_env, validar_tax, leer_txt
from alegra.alegra import AlegraService

FACTREM = 'fact/remis'
EXCELPATH = load_env()['rutas']['excel']

def procesar_enviables(conjunto_registros, index, api):
    """Método encargado de procesar enviable sea remision o factura."""

    registro_principal = conjunto_registros[0]
    if registro_principal['estado'].lower() == 'pendiente':
        try:
            id_cliente = api.get_client_by_id(identification = registro_principal['clienteid'])
        except IndexError:
            print("Error consultando la informacion del cliente😢😢 Valide que la identificación número " + str(registro_principal['clienteid']) + " se encuentre asociada a un cliente registrado en Alegra 🥱🥱")
        else:
            fallo_producto, items = False, []
            for registro in conjunto_registros:
                try:
                    id_producto = api.get_product_by_id(referencia = registro['ref'])
                except IndexError:
                    print("Error consultando informacion del producto😢😢 Valide que la referencia " + str(registro['ref']) + " se encuentre asociada a un producto registrado en Alegra 🥱🥱")
                    fallo_producto = True
                    break
                except Exception:
                    break
                else:
                    item = {
                        'id': id_producto,
                        'price': registro['precio base'],
                        'quantity': registro['cantidad'],
                        'reference': registro['ref'],
                        'tax' : [ {
                                'id' : validar_tax(registro['iva'])
                            }]
                    }
                    items.append(item)
            
            if not(fallo_producto):
                response = generar_payload_send(id_cliente, registro_principal, items, api)
                cambiar_estado(response, registro = index[0])
            
def generar_payload_send(id_cliente, registro_principal, items, api):
    """Encargada de generar el json completoy enviar factura o remision a la api."""
    payload = {
        'client' : id_cliente,
        'date' : str(registro_principal['fecha'].date()),
        'dueDate' : str(registro_principal['fecha de vencimiento'].date()),
        'items' : items
        }

    if registro_principal[FACTREM].lower() == 'factura':
        payload['anotation'] = leer_txt(load_env()['rutas']['FacturaNotas']) + ' ' + str(registro_principal['transportadora']) + ' ' + str(registro_principal['guia']) + ' ' + str(registro_principal['# paquetes']) + ' ' + str(registro_principal['empacador'])
        payload['termsConditions'] = leer_txt(load_env()['rutas']['FacturaTyC'])

        response = api.enviar_factura(payload)
        print("!Factura cargada! 💰💰 ID: " + str(registro_principal['clienteid']) + "\n")

    elif registro_principal[FACTREM].lower() == 'remision':
        payload['anotation'] = str(registro_principal['transportadora']) + ' ' + str(registro_principal['guia']) + '*' + str(registro_principal['# paquetes']) + ' ' + str(registro_principal['empacador'])
        payload['comments'] = [leer_txt(load_env()['rutas']['RemisionTyC'])]

        response = api.enviar_remision(payload)
        print("!Remision cargada! ✅✅ ID: " + str(registro_principal['clienteid']) + "\n")

    else:
        response = None
        print("No se reconoce entre factura o remision 😢😢 ID: " + str(registro_principal['clienteid']) + "\n")
    return response

def cambiar_estado(response, registro):
    """Valida que la respuesta del envío sea exitosa."""
    if response != None and response.status_code == 201:
        excel_obj = excel.archivo_excel(path_excel = EXCELPATH)
        excel_obj.cambiar_estado(registro);

def procesar_conjuntos(registros, filas_vacias_index, api):
    """Identificar productos que pertenecen a un mismo cliente.
    Debido a la estructura del archivo de excel, donde para un cliente se apilan los diferentes productos."""    
    print("\n🧮🧮 Generando estructura para facturas y remisiones 🧮🧮 \n" )

    conjunto, index = [], []
    for i, j in enumerate(registros):
        if (i not in filas_vacias_index):
            #Juntar registros pertenecientes a mismo enviable.
            conjunto.append(j)
            index.append(i)
        else:
            if (len(conjunto) > 0):
                #Procesar conjunto de registros.
                procesar_enviables(conjunto, index, api)
                conjunto.clear()
                index.clear()
    if (len(conjunto) > 0):
        #Procesar conjunto de registros.
        procesar_enviables(conjunto, index, api)

def main():
    print("🚀!AlegraApp está despegandoooo!🚀")
    try:
        open(EXCELPATH, "r+")
    except FileNotFoundError:
        print("Excel no encontrado. Verifica que el archivo con nombre: " + EXCELPATH + " existe")
    except PermissionError:
        print("No se pudo abrir el archivo. Por favor cierra el Excel")
    except Exception:
        print("Ocurrió un error")
    else:
        alegraService = AlegraService()
        print(alegraService._headers)     
        enviables = excel.archivo_excel(path_excel = EXCELPATH)
        try:
            registros, filas_vacias_index = enviables.leer_registros()
        except ValueError:
            print("No se encontró la pagina de ENVIABLES dentro del archivo")
        else:
            procesar_conjuntos(registros, filas_vacias_index, alegraService)
    finally:
        input("Presiona Enter para salir")

if __name__ == '__main__':
    main()
