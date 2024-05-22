from typing import List
from alegra.alegra import AlegraService
from dtos.record import Estado, PurchaseRecordDto, Tipo
from excel.excel import Excel
from utils.helpers import read_config,leer_txt,validar_tax

from mappers.excelMapper import map_purchases

FACTREM = 'fact/remis'
EXCELPATH = read_config()['rutas']['excel']

def procesar_enviables(conjunto_registros, index, api: AlegraService):
    """Método encargado de procesar enviable sea remision o factura."""

    registro_principal = conjunto_registros[0]
    if registro_principal['estado'].lower() == 'pendiente':
        try:
            id_cliente = api.get_client_by_id(id = registro_principal['clienteid'])
        except:
            print("Error consultando la informacion del cliente Valide que la identificación número " + str(registro_principal['clienteid']) + " se encuentre asociada a un cliente registrado en Alegra 🥱🥱")
        else:
            fallo_producto, items = False, []
            for registro in conjunto_registros:
                try:
                    id_producto = api.get_product_by_id(reference = registro['ref'])
                except:
                    print("Error consultando informacion del producto😢😢 Valide que la referencia " + str(registro['ref']) + " se encuentre asociada a un producto registrado en Alegra 🥱🥱")
                    fallo_producto = True
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
                #cambiar_estado(response, registro = index[0])
            
def generar_payload_send(id_cliente, registro_principal, items, api):
    """Encargada de generar el json completoy enviar factura o remision a la api."""
    payload = {
        'client' : id_cliente,
        'date' : str(registro_principal['fecha'].date()),
        'dueDate' : str(registro_principal['fecha de vencimiento'].date()),
        'items' : items
        }

    if registro_principal[FACTREM].lower() == 'factura':
        payload['anotation'] = leer_txt(read_config()['rutas']['FacturaNotas']) + ' ' + str(registro_principal['transportadora']) + ' ' + str(registro_principal['guia']) + ' ' + str(registro_principal['# paquetes']) + ' ' + str(registro_principal['empacador'])
        payload['termsConditions'] = leer_txt(read_config()['rutas']['FacturaTyC'])

        response = api.load_invoce(payload)
        print("!Factura cargada! 💰💰 ID: " + str(registro_principal['clienteid']) + "\n")

    elif registro_principal[FACTREM].lower() == 'remision':
        payload['anotation'] = str(registro_principal['transportadora']) + ' ' + str(registro_principal['guia']) + '*' + str(registro_principal['# paquetes']) + ' ' + str(registro_principal['empacador'])
        payload['comments'] = [leer_txt(read_config()['rutas']['RemisionTyC'])]

        response = api.load_remission(payload)
        print("!Remision cargada! ✅✅ ID: " + str(registro_principal['clienteid']) + "\n")

    else:
        response = None
        print("No se reconoce entre factura o remision 😢😢 ID: " + str(registro_principal['clienteid']) + "\n")
    return response

# def cambiar_estado(response, registro):
#     """Valida que la respuesta del envío sea exitosa."""
#     if response != None and response.status_code == 201:
#         excel_obj = excel.archivo_excel(path_excel = EXCELPATH)
#         excel_obj.cambiar_estado(registro);
def process_estimate(estimate: PurchaseRecordDto):
    client_id = api.get_client_by_id(id = estimate.cliente_id)

def process_remission(remission: PurchaseRecordDto):
    pass

def process_invoice(invoice: PurchaseRecordDto):
    pass

def generate_items():
    pass

def process_purchase(purchase: PurchaseRecordDto):
    if (purchase.estado != Estado.PENDIENTE):
        return

    if (purchase.tipo == Tipo.COTIZACION):
        process_estimate(purchase)
    elif (purchase.tipo == Tipo.FACTURA):
        process_invoice(purchase)
    elif (purchase.tipo == Tipo.REMISION):
        process_remission(purchase)
    else: 
        print("No se reconoce entre factura o remision ID: " + str(purchase.cliente_id) + "\n")
    

def main():
    print("🚀🚀🚀!AlegraApp está despegandoooo!🚀🚀🚀")
    try:
        open(EXCELPATH, "r+")
    except FileNotFoundError:
        print("Excel no encontrado. Verifica que el archivo con nombre: " + EXCELPATH + " exista")
    except PermissionError:
        print("No se pudo abrir el archivo. Por favor cierra el Excel.")
    except Exception:
        print("Ocurrió un error 😢😢")
    else:
        #Singleton con alegraService
        api = AlegraService()
        purchases: List[PurchaseRecordDto] = map_purchases()
        try:
            for purchase in purchases:                
                process_purchase(purchase)

            #registros, filas_vacias_index = enviables.map_purchases()
        except ValueError:
            print("No se encontró la pagina de ENVIABLES dentro del archivo.")
        else:
            procesar_conjuntos(registros, filas_vacias_index, api)
    finally:
        input("Presiona Enter para salir")

def main2():
    purchases: List[PurchaseRecordDto] = map_purchases()
    for purchase in purchases:                
        process_purchase(purchase)

if __name__ == '__main__':
    #main()
    main2()

