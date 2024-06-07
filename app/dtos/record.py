"DTOs"
from dataclasses import dataclass
from enum import Enum
from datetime import date
from typing import List

class Estado(Enum):
    "Handles the state of the purchase record"
    CARGADO = "cargado"
    PENDIENTE = "pendiente"

class Tipo(Enum):
    "Handles the type of the purchase record"
    COTIZACION = "cotizacion"
    FACTURA = "factura"
    REMISION = "remision"

@dataclass
class ProductDto:
    "Product data transfer object."
    iva: str
    referencia: str
    articulo: str
    cantidad: int
    precio_iva_incluido: float
    total: float
    peso: float
    num_paq: float
    precio_base: float
    subtotal: float

@dataclass
class PurchaseRecordDto:
    "Purchase record data transfer object."
    row_id: int
    fecha: date
    plazo_dias: int
    fecha_vencimiento: date
    tipo: Tipo
    vendedor: str
    cliente_nombre: str
    cliente_id: str
    poblacion: str
    codigo: str
    transportadora: str
    guia: str
    paq_tot: int
    empacador: str
    notas: str
    faltante: str
    estado: Estado
    productos: List[ProductDto]
