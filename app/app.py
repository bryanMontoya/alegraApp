from typing import List

from alegra.alegra import AlegraService
from dtos.record import Estado, PurchaseRecordDto, ProductDto, Tipo
from mappers.excelMapper import map_purchases
from utils.helpers import read_config, read_txt, validate_tax

api = AlegraService()

def process_purchase(purchase: PurchaseRecordDto):
    if (purchase.estado != Estado.PENDIENTE):
        return
    
    payload = generate_payload(purchase)
    try:
        if (purchase.tipo == Tipo.COTIZACION):
            response = process_estimate(purchase, payload)
        elif (purchase.tipo == Tipo.FACTURA):
            response = process_invoice(purchase, payload)
        elif (purchase.tipo == Tipo.REMISION):
            response = process_remission(purchase, payload)
        else: 
            print("No se reconoce entre factura/remision/cotizacion ID" + str(purchase.cliente_id) + "\n")
        print(response)
    except Exception as e:
        print(f"Error al procesar registro {purchase.cliente_id}. {e}")

def generate_payload(purchase: PurchaseRecordDto):
    payload = {
        'client' : api.get_client_by_id(id = purchase.cliente_id),
        'date' : str(purchase.fecha),
        'dueDate' : str(purchase.fecha_vencimiento),
        'items' : generate_items(purchase.productos)
    }
    return payload

def generate_items(products: List[ProductDto]):
    items = []
    for product in products:
        items.append({
            'id': api.get_product_by_id(reference = product.referencia),
            'price': product.precio_base,
            'quantity': product.cantidad,
            'reference': product.referencia,
            'tax' : [{
                    'id' : validate_tax(product.iva)
                }]
        })
    return items

def process_estimate(estimate: PurchaseRecordDto, payload: dict):
    return api.load_estimate(payload)

def process_invoice(invoice: PurchaseRecordDto, payload: dict):
    config = read_config()
    payload['anotation'] = f"{read_txt(config['rutas']['FacturaNotas'])} {invoice.transportadora} {invoice.guia} {invoice.paq_tot} {invoice.empacador}"
    payload['termsConditions'] = read_txt(config['rutas']['FacturaTyC'])

    return api.load_invoce(payload)

def process_remission(remission: PurchaseRecordDto, payload: dict):
    config = read_config()
    payload['anotation'] = f"{remission.transportadora} {remission.guia}*{remission.paq_tot} {remission.empacador}"    
    payload['comments'] = [read_txt(config['rutas']['RemisionTyC'])]

    return api.load_remission(payload)

def main():
    purchases: List[PurchaseRecordDto] = map_purchases()
    for purchase in purchases:                
        process_purchase(purchase)

if __name__ == '__main__':    
    main()
