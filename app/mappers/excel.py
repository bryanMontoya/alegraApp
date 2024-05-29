"Map from excel records to Dtos"
from typing import List

from excel.excel import Excel
from dtos.record import Estado, ProductDto, PurchaseRecordDto, Tipo

def map_purchases(excel: Excel) -> List[PurchaseRecordDto]:
    """Mapear registros a objeto."""
    print("Generando estructura de items de venta")
    excel.read_file()
    records = excel.records
    empty_records_index = excel.empty_records_index
    purchases: List[PurchaseRecordDto] = []
    purchase_list, rows_id = [], []

    for record_index, record in enumerate(records):
        if record_index not in empty_records_index:
            purchase_list.append(record)
            rows_id.append(record_index)
        else:
            if len(purchase_list) > 0:
                purchases.append(purchase_list_to_purchase_dto(purchase_list, rows_id))
                purchase_list.clear()
                rows_id.clear()
    if len(purchase_list) > 0:
        purchases.append(purchase_list_to_purchase_dto(purchase_list, rows_id))

    return purchases

def purchase_list_to_purchase_dto(purchase_list: List, rows_id: List) -> PurchaseRecordDto:
    """Convertir lista de registros a objeto."""
    products = [record_to_product_dto(record) for record in purchase_list]
    purchase = record_to_purchase_dto(purchase_list[0], products, rows_id[0])
    return purchase

def record_to_product_dto(record: dict) -> ProductDto:
    "Convert record to product dto."
    return ProductDto(
        iva = record['iva'],
        referencia = record['ref'],
        articulo = record['articulo'],
        cantidad = record['cantidad'],
        precio_iva_incluido = record['precios iva inc'],
        total = record['total'],
        peso = record['peso (kg)'],
        num_paq = record['# paquetes'],
        precio_base = record['precio base'],
        subtotal = record['subtotal']
    )

def record_to_purchase_dto(record: dict, products: List[ProductDto], index: int) -> PurchaseRecordDto:
    "Convert record to purchase dto."
    return PurchaseRecordDto(
        row_id = index + 2, #To match the row number in the excel file(because of the header row)
        fecha = record['fecha'],
        plazo_dias = record['plazo dias'],
        fecha_vencimiento = record['fecha de vencimiento'],
        tipo = Tipo(record['fact/remis'].lower()),
        dcto_financiero = record['dcto fnciero'],
        cliente_nombre = record['clientenombre'],
        cliente_id = record['clienteid'],
        poblacion = record['poblacion'],
        codigo = record['fac/rem'],
        transportadora = record['transportadora'],
        guia = record['guia'],
        paq_tot = record['pac tot'],
        empacador = record['empacador'],
        notas = record['notas'],
        faltante = record['faltante'],
        estado = Estado(record['estado'].lower()),
        productos = products
    )
