"Main module application"
from requests import Response
from typing import List

from alegra.alegra import AlegraService
from dtos.record import Estado, PurchaseRecordDto, ProductDto, Tipo
from excel.excel import Excel
from mappers.excel import map_purchases
from utils.helpers import read_config, read_txt, validate_tax

api = AlegraService()
excel = Excel()

def process_purchase(purchase: PurchaseRecordDto):
    "Process estimate/ invoce/ remission depending on the purchase type"
    if purchase.estado != Estado.PENDIENTE:        
        return
    try:
        payload = generate_payload(purchase)
        if purchase.tipo == Tipo.COTIZACION:
            print(f"Cargando cotizacion para cliente con id {purchase.cliente_id}")
            response = process_estimate(purchase, payload)
        elif purchase.tipo == Tipo.FACTURA:
            print(f"Cargando factura para cliente con id {purchase.cliente_id}")
            response = process_invoice(purchase, payload)
        elif purchase.tipo == Tipo.REMISION:
            print(f"Cargando remision para cliente con id {purchase.cliente_id}")
            response = process_remission(purchase, payload)
        else:
            print(f"No se reconoce entre factura/remision/cotizacion ID {purchase.cliente_id}")
            return
        change_state(purchase = purchase, api_response = response)
    except Exception:
        print(f"Error al procesar registro para cliente con id {purchase.cliente_id}")
        print(f"Error: {Exception}")
        return

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
    return response

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
    return response

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
    return response

def change_state(purchase: PurchaseRecordDto, api_response: Response) -> PurchaseRecordDto:
    "Change the state of the purchase"
    if api_response.status_code == 201:
        purchase.estado = Estado.CARGADO
        excel.change_status_column(purchase.row_id)
    return purchase

def main():
    print("AlegraApp esta despegando")

    purchases: List[PurchaseRecordDto] = map_purchases(excel)
    for purchase in purchases:
        process_purchase(purchase)

    print("AlegraApp ha aterrizado")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
