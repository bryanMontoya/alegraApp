from dataclasses import dataclass
from enum import Enum
from datetime import date
from typing import List

class Estado(Enum):
    CARGADO = "cargado"
    PENDIENTE = "pendiente"

@dataclass
class ProductDto:
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
    fecha: date
    plazo_dias: int
    fecha_vencimiento: date
    tipo: str
    dcto_financiero: str
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
