import alegraApi
import excel
import utils
import autorizacion

def procesarEnviables(conjuntoRegistros):
    """Método encargado de procesar enviable sea remision o factura.
    Params: lista Conjunto de registros a enviar."""
    api = alegraApi.Api()
    api.setHeaders(autorizacion.genBasicToken())
    api.setUrlApi(utils.leerYaml()['rutas']['apiAlegra'])

    registroPrincipal = conjuntoRegistros[0]
    try:
        idCliente = api.getClientById(identification = registroPrincipal['clienteid'])
    except:
        print("Error consultando la informacion del cliente. Valide que la identificación número " + str(registroPrincipal['clienteid'])
                + ", se encuentre asociada a un cliente registrado en Alegra.")
    else:
        payload = {
            'date': str(registroPrincipal['fecha'].date()),
            'dueDate': str(registroPrincipal['fechavencimiento'].date()),
            'client': idCliente,
        }
        falloProducto = False
        items = []
        for registro in conjuntoRegistros:
            try:
                idProducto = api.getProductById(referenciaProd = registro['referencia'])
            except:
                print("Error consultando informacion del producto. Valide que la referencia número " + str(registro['referencia'])
                        + ", se encuentre asociada a un producto registrado en Alegra.")
                falloProducto = True
                break
            else:
                item = {
                    'id': idProducto,
                    'price': registro['precio'],
                    'quantity': registro['cantidad'],
                    'reference': registro['referencia'],
                    'tax' : [ {
                            'id' : validarTax(registro['iva'])
                        }]
                }
                items.append(item)

        if not(falloProducto):
            payload['items'] = items
            if registroPrincipal['fact/remis'].lower() == 'factura':
                payload['anotation'] = utils.leerTxt(utils.leerYaml()['rutas']['FacturaNotas'])
                payload['termsConditions'] : utils.leerTxt(utils.leerYaml()['rutas']['FacturaTyC'])
                respuestaEnvio = api.enviarFactura(payload)
            elif registroPrincipal['fact/remis'].lower() == 'remision':
                payload['observations'] = str(registroPrincipal['transportadora']) + ' ' + str(registroPrincipal['guia']) + '*' + str(registroPrincipal['numeropaquetes'])
                payload['anotation'] = utils.leerTxt(utils.leerYaml()['rutas']['RemisionTyC'])
                respuestaEnvio = api.enviarRemision(payload)

            print(respuestaEnvio)

    #TODO status code respuesta api.
'''if response.status_code == 201:
        excel = modelo.archivoExcel(pathExcel = utils.pathExcelFile)
        excel.guardarFacturados(registro = registro)
        return regIndx     '''

def procesarConjuntos(registrosPendientes, registrosVaciosIndex):
    """procesarConjuntos: Identificar productos que pertenecen a un mismo cliente.
    Debido a la estructura del archivo de excel, donde para un cliente se apilan los diferentes productos.
    """
    print("Generando estructura para facturas y remisiones.")
    conjunto = []
    for i, j in enumerate(registrosPendientes):
        if (i not in registrosVaciosIndex):
            #Juntar registros pertenecientes a mismo enviable.
            conjunto.append(j)
        else:
            if (len(conjunto) > 0):
                #Procesar conjunto de registros.
                procesarEnviables(conjuntoRegistros = conjunto)
                conjunto.clear()
    else:
        if (len(conjunto) > 0):
            #Procesar conjunto de registros.
            procesarEnviables(conjuntoRegistros = conjunto)

def validarTax(tax):
    """Valida el id a enviar de acuerdo al iva en el excel.""" 
    if (tax == 0.19 or tax == 19):
        return 3
    elif (tax == 0.05 or tax == 5):
        return 2
    return 1

def main():
    excelEnviables = excel.archivoExcel(pathExcel = utils.leerYaml()['rutas']['excel'])
    print("Leyendo registros del archivo Excel.")
    registrosPendientes, registrosVacios = excelEnviables.leerRegistrosPendientes()
    procesarConjuntos(registrosPendientes, registrosVacios)

if __name__ == '__main__':
    main()

#TODO Leer txt como una sola linea aunque sean varias.
#TODO referencia de productos numeros enteros problemas con decimal.