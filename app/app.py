"Main module application"
from requests import Response
from typing import List

from alegra.alegra import AlegraService
from dtos.record import Estado, PurchaseRecordDto, ProductDto, Tipo
from mappers.excel import map_purchases
from utils.helpers import read_config, read_txt, validate_tax

api = AlegraService()

def process_purchase(purchase: PurchaseRecordDto):
    "Process estimate/ invoce/ remission depending on the purchase type"
    if purchase.estado != Estado.PENDIENTE:
        return
    payload = generate_payload(purchase)
    try:
        if purchase.tipo == Tipo.COTIZACION:
            return process_estimate(purchase, payload)
        elif purchase.tipo == Tipo.FACTURA:
            return process_invoice(purchase, payload)
        elif purchase.tipo == Tipo.REMISION:
            return process_remission(purchase, payload)
        else:
            print("No se reconoce entre factura/remision/cotizacion ID" + str(purchase.cliente_id))
            return purchase
    except Exception as e:
        print(f"Error al procesar registro {purchase.cliente_id}. {e}")

def generate_payload(purchase: PurchaseRecordDto) -> dict:
    "Generates the payload for the api request"
    payload = {
        'client' : api.get_client_by_id(id = purchase.cliente_id),
        'date' : str(purchase.fecha),
        'dueDate' : str(purchase.fecha_vencimiento),
        'items' : generate_items(purchase.productos)
    }
    return payload

def generate_items(products: List[ProductDto]) -> List[dict]:
    "Generates list of items for the api request"
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
    "Process estimate - Call api load"
    response = api.load_estimate(payload)
    return change_state(estimate, response)

def process_invoice(invoice: PurchaseRecordDto, payload: dict):
    "Process invoice - Configure payload adds and Call api load"
    config = read_config()
    payload['anotation'] = (
        f"{read_txt(config['rutas']['FacturaNotas'])} "
        f"{invoice.transportadora} "
        f"{invoice.guia} "
        f"{invoice.paq_tot} "
        f"{invoice.empacador}"
    )
    payload['termsConditions'] = read_txt(config['rutas']['FacturaTyC'])

    response = api.load_invoce(payload)
    return change_state(invoice, response)

def process_remission(remission: PurchaseRecordDto, payload: dict) -> PurchaseRecordDto:
    "Process remission - Configure payload adds and Call api load"
    config = read_config()
    payload['anotation'] = (
        f"{remission.transportadora} "
        f"{remission.guia}*"
        f"{remission.paq_tot} "
        f"{remission.empacador}"
    )
    payload['comments'] = [read_txt(config['rutas']['RemisionTyC'])]

    response = api.load_remission(payload)
    return change_state(remission, response)

def change_state(purchase: PurchaseRecordDto, api_response: Response) -> PurchaseRecordDto:
    "Change the state of the purchase"
    if api_response.status_code == 201:
        purchase.estado = Estado.CARGADO
    return purchase

def main():
    "Main function"
    purchases: List[PurchaseRecordDto] = map_purchases()
    for purchase in purchases:
        print(process_purchase(purchase))

if __name__ == '__main__':
    main()
