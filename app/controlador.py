"""Controlador"""

import AlegraApi
import modelo
import utils
import utilsGenHeaders

def procesarEnviables(conjuntoRegistros):
        """
        procesarEnviables(): Método encargado de procesar enviable sea remision o factura.
        Params: 
        Retorna payload con enviable construido.
        """
        api = AlegraApi.Api()        
        api.setHeaders(utilsGenHeaders.genBasicToken())
        api.setUrlApi(utils.urlApi)

        registroPrincipal = conjuntoRegistros[0]        
                
        idCliente = api.getClientById(identification = registroPrincipal['clienteid'])        
        payload = {
            'date': str(registroPrincipal['fecha'].date()),
            'dueDate': str(registroPrincipal['fechavencimiento'].date()),
            'client': idCliente,            
            'termsConditions' : utils.terminosCondiciones()
        }

        items = []
        for registro in conjuntoRegistros:
            idProducto = api.getProductById(referenciaProd = registro['referencia'])        
            item = {
                'id': idProducto,
                'price': registro['precio'],
                'quantity': registro['cantidad'],   
                'reference': registro['referencia']
            }            
            items.append(item)                              
        payload['items'] = items                

        #Para campos que no se comparten.
        if registroPrincipal['fact / remis'].lower() == 'facturado':
            payload['anotation'] = """Favor consignar en la cta de ahorros Bancolombia #412 
                    00 00 0219 o en cta ahorros Davivienda #39 4000 054 707 a nombre de Samuel Rendon SAS.""", #TODO Anotaciones en txt
            respuesta = api.enviarFactura(payload)
        elif registroPrincipal['fact / remis'].lower() == 'remisionado':
            payload['anotation'] = str(registroPrincipal['transportadora']) + ' ' + str(registroPrincipal['guia']) + '*' + str(registroPrincipal['numeropaquetes'])
            respuesta = api.enviarRemision(payload)

        print(respuesta)                    
    
    #TODO status code respuesta api.
'''if response.status_code == 201:                        
        excel = modelo.archivoExcel(pathExcel = utils.pathExcelFile)
        excel.guardarFacturados(registro = registro)
        return regIndx     '''

def procesarConjuntos(registrosPendientes, registrosVaciosIndex):
    """procesarConjuntos: Identificar productos que pertenecen a un mismo cliente.
    Debido a la estructura del archivo de excel, donde para un cliente se apilan los diferentes productos.
    """
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

def main():
    
    excelEnviables = modelo.archivoExcel(pathExcel = utils.pathExcelFile)
    registrosPendientes, registrosVacios = excelEnviables.leerRegistrosPendientes()    
    procesarConjuntos(registrosPendientes, registrosVacios)         

if __name__ == '__main__':
    main()    

#TODO Generar token solo al inicio del programa.
#TODO Resiliente a caidas de red.
#TODO tax == IVA? Objeto
#TODO Tolerar que los llamados no funcionen.