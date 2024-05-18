from typing import List

from excel.excel import Excel
from dtos.record import Estado, ProductDto, PurchaseRecordDto

def map_purchases() -> List[PurchaseRecordDto]:
    """Mapear registros a objeto."""
    excel = Excel()
    excel.read_file()
    records = excel.records
    empty_records_index = excel.empty_records_index

    purchases: List[PurchaseRecordDto] = []
    purchaseList = []
    for record_index, record in enumerate(records):
        if (record_index not in empty_records_index):
            purchaseList.append(record)
        else:
            if (len(purchaseList) > 0):
                purchaseList_to_purchaseDto(purchaseList)
                purchaseList.clear()
    if (len(purchaseList) > 0):
    #Procesar conjunto de registros.
        pass

def purchaseList_to_purchaseDto(purchaseList: List) -> PurchaseRecordDto:
    for record in purchaseList:
        purchase = PurchaseRecordDto(
            fecha = record['fecha'],
            plazo_dias = record['plazo_dias'],
            fecha_vencimiento = record['fecha_vencimiento'],
            tipo = record['tipo'],
            dcto_financiero = record['dcto_financiero'],
            cliente_nombre = record['cliente_nombre'],
            cliente_id = record['cliente_id'],
            poblacion = record['poblacion'],
            codigo = record['codigo'],
            transportadora = record['transportadora'],
            guia = record['guia'],
            paq_tot = record['paq_tot'],
            empacador = record['empacador'],
            notas = record['notas'],
            faltante = record['faltante'],
            estado = Estado(record['estado']),
            products = []
        )
