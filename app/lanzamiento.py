import alegraApi
import excel
import utils
import autorizacion

#TODO Method Refactor
def procesar_enviables(conjunto_registros):
    """Método encargado de procesar enviable sea remision o factura.
    Params: lista Conjunto de registros a enviar."""    
    api = alegraApi.Api()
    api.set_headers(autorizacion.gen_basic_token())
    api.set_url_api(utils.leer_config()['rutas']['apiAlegra'])

    registro_principal = conjunto_registros[0]
    if registro_principal['estado'].lower() == 'pendiente':
        try:
            id_cliente = api.get_client_by_id(identification = registro_principal['clienteid'])
        except:
            print("Error consultando la informacion del cliente. Valide que la identificación número " + str(registro_principal['clienteid'])
                    + ", se encuentre asociada a un cliente registrado en Alegra.")
        else:            
            fallo_producto = False
            items = []
            for registro in conjunto_registros:
                try:
                    id_producto = api.get_product_by_id(referencia = registro['referencia'])
                except:
                    print("Error consultando informacion del producto. Valide que la referencia número " + str(registro['referencia'])
                            + ", se encuentre asociada a un producto registrado en Alegra.")
                    fallo_producto = True
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
            
            payload = {
                'date': str(registro_principal['fecha'].date()),
                'dueDate': str(registro_principal['fechavencimiento'].date()),
                'client': id_cliente,
            }
            if not(fallo_producto):
                payload['items'] = items
                if registro_principal['fact/remis'].lower() == 'factura':
                    payload['anotation'] = utils.leer_txt(utils.leer_config()['rutas']['FacturaNotas'])
                    payload['termsConditions'] : utils.leer_txt(utils.leer_config()['rutas']['FacturaTyC'])  # type: ignore
                    respuesta_envio = api.enviar_factura(payload)
                elif registro_principal['fact/remis'].lower() == 'remision':
                    payload['observations'] = str(registro_principal['transportadora']) + ' ' + str(registro_principal['guia']) + '*' + str(registro_principal['numeropaquetes'])
                    payload['anotation'] = utils.leer_txt(utils.leer_config()['rutas']['RemisionTyC'])
                    respuesta_envio = api.enviar_remision(payload)

def cambiar_estado(response):
    """Cambiar estado."""
    if response.status_code == 201:
        print("Cambiar estado")

def procesar_conjuntos(registros, filas_vacias_index):
    """procesarConjuntos: Identificar productos que pertenecen a un mismo cliente.
    Debido a la estructura del archivo de excel, donde para un cliente se apilan los diferentes productos.
    """
    print("Generando estructura para facturas y remisiones.")
    conjunto = []
    for i, j in enumerate(registros):
        if (i not in filas_vacias_index):
            #Juntar registros pertenecientes a mismo enviable.
            conjunto.append(j)
        else:
            if (len(conjunto) > 0):
                #Procesar conjunto de registros.
                procesar_enviables(conjunto)                
                conjunto.clear()    
    if (len(conjunto) > 0):
        #Procesar conjunto de registros.        
        procesar_enviables(conjunto)

def validar_tax(tax):
    """Valida el id a enviar de acuerdo al iva en el excel.""" 
    if (tax == 0.19 or tax == 19):
        return 3
    elif (tax == 0.05 or tax == 5):
        return 2
    return 1

def main():
    enviables = excel.archivo_excel(path_excel = utils.leer_config()['rutas']['excel'])
    print("Leyendo registros del archivo Excel.")
    registros, filas_vacias_index = enviables.leer_registros()    
    procesar_conjuntos(registros, filas_vacias_index)

if __name__ == '__main__':
    main()

#TODO Leer txt como una sola linea aunque sean varias.
#TODO referencia de productos numeros enteros problemas con decimal.
#TODO Registros en estado diferente de enviado.