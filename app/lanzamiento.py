import alegra
import excel
import utils
import autorizacion
from openpyxl import load_workbook

FACTREM = 'fact/remis'
EXCELPATH = utils.leer_config()['rutas']['excel']

def procesar_enviables(conjunto_registros, index):
    """Método encargado de procesar enviable sea remision o factura.
    Params: lista Conjunto de registros a enviar."""
    api = alegra.Api()
    api.set_headers(autorizacion.gen_basic_token())
    api.set_url_api(utils.leer_config()['rutas']['apiAlegra'])

    registro_principal = conjunto_registros[0]
    if registro_principal['estado'].lower() == 'pendiente':
        try:
            id_cliente = api.get_client_by_id(identification = registro_principal['clienteid'])
        except IndexError:
            print("Error consultando la informacion del cliente. Valide que la identificación número " + str(registro_principal['clienteid']) + ", se encuentre asociada a un cliente registrado en Alegra =)")
        except Exception:
            pass
        else:
            fallo_producto, items = False, []
            for registro in conjunto_registros:
                try:
                    id_producto = api.get_product_by_id(referencia = registro['referencia'])
                except IndexError:
                    print("Error consultando informacion del producto. Valide que la referencia número " + str(registro['referencia']) + ", se encuentre asociada a un producto registrado en Alegra =)")
                    fallo_producto = True
                    break
                except Exception:
                    break
                else:
                    item = {
                        'id': id_producto,
                        'price': registro['precio'],
                        'quantity': registro['cantidad'],
                        'reference': registro['referencia'],
                        'tax' : [ {
                                'id' : validar_tax(registro['iva'])
                            }]
                    }
                    items.append(item)
            
            if not(fallo_producto):
                payload = generar_payload(id_cliente, registro_principal, items)
                if registro_principal[FACTREM].lower() == 'factura':
                    response = api.enviar_factura(payload)
                elif registro_principal[FACTREM].lower() == 'remision':
                    response = api.enviar_remision(payload)
                else:          
                    response = None          
                    print("No se reconoce entre factura o remision :P")
                cambiar_estado(response, registro = index[0])
                
def generar_payload(id_cliente, registro_principal, items):
    """Encargada de generar el json completo."""
    payload = {
        'client' : id_cliente,
        'date' : str(registro_principal['fecha'].date()),
        'dueDate' : str(registro_principal['fechavencimiento'].date()),
        'items' : items
        }
    if registro_principal[FACTREM].lower() == 'factura':
        payload['anotation'] = utils.leer_txt(utils.leer_config()['rutas']['FacturaNotas'])
        payload['termsConditions'] = utils.leer_txt(utils.leer_config()['rutas']['FacturaTyC'])
    elif registro_principal[FACTREM].lower() == 'remision':
        payload['observations'] = str(registro_principal['transportadora']) + ' ' + str(registro_principal['guia']) + '*' + str(registro_principal['numeropaquetes'])
        payload['anotation'] = utils.leer_txt(utils.leer_config()['rutas']['RemisionTyC'])
    return payload

def cambiar_estado(response, registro):
    """Cambiar estado."""
    print(response.status_code)
    if response.status_code == 201:
        workbook = load_workbook(filename = EXCELPATH)
        sheet = workbook.active
        space = "X" + str(registro + 2)
        sheet[space] = "Cargado"
        workbook.save(filename = EXCELPATH)

def procesar_conjuntos(registros, filas_vacias_index):
    """procesarConjuntos: Identificar productos que pertenecen a un mismo cliente.
    Debido a la estructura del archivo de excel, donde para un cliente se apilan los diferentes productos.
    """
    print("Loading!!! Generando estructura para facturas y remisiones 🚀🚀")
    conjunto, index = [], []
    for i, j in enumerate(registros):
        if (i not in filas_vacias_index):
            #Juntar registros pertenecientes a mismo enviable.
            conjunto.append(j)
            index.append(i)
        else:
            if (len(conjunto) > 0):
                #Procesar conjunto de registros.
                procesar_enviables(conjunto, index)
                conjunto.clear()
                index.clear()
    if (len(conjunto) > 0):
        #Procesar conjunto de registros.
        procesar_enviables(conjunto, index)

def validar_tax(tax):
    """Valida el id a enviar de acuerdo al iva en el excel."""
    if (tax == 0.19 or tax == 19):
        return 3
    elif (tax == 0.05 or tax == 5):
        return 2
    return 1

def main():
    try:
        open(EXCELPATH, "r+")
    except FileNotFoundError:
        print("Archivo no encontrado :-( Verifica que el archivo " + EXCELPATH + " existe :-)")
    except PermissionError:
        print("No se pudo abrir el archivo! Por favor cierra el Excel :)")
    else:
        enviables = excel.archivo_excel(path_excel = EXCELPATH)
        registros, filas_vacias_index = enviables.leer_registros()
        print("Genial Leyendo registros del archivo Excel!")
        procesar_conjuntos(registros, filas_vacias_index)
    finally:
        input("Presiona cualquier tecla para salir ^_^")


if __name__ == '__main__':
    main()
