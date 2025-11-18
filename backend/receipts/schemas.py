from ninja import Schema
from datetime import datetime
from decimal import Decimal
from typing import List, Optional


class StoreDataSchema(Schema):
    """Dados da loja vindos do scraper"""
    name: str = ''
    cnpj: str = ''
    address: str = ''
    number: str = ''
    neighborhood: str = ''
    city: str = ''
    state: str = ''
    phone: str = ''


class ItemDataSchema(Schema):
    """Dados do item vindos do scraper"""
    name: str = ''
    code: str = ''
    quantity: Optional[float] = None
    unit: str = ''
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    estimated_taxes: Optional[float] = None


class TotalsDataSchema(Schema):
    """Dados dos totais"""
    total_products: Optional[float] = None
    discount: float = 0
    total: Optional[float] = None
    total_taxes: Optional[float] = None


class PaymentDataSchema(Schema):
    """Dados do pagamento"""
    method: str = ''
    value: Optional[float] = None


class ReceiptDataSchema(Schema):
    """Schema completo dos dados da nota (do scraper)"""
    store: StoreDataSchema
    receipt: dict = {}  # number, series
    items: List[ItemDataSchema] = []
    totals: TotalsDataSchema
    payment: PaymentDataSchema
    access_key: str = ''
    issued_at: Optional[str] = None


class ImportReceiptRequest(Schema):
    """Requisição para importar nota"""
    qrcode_url: str


class ImportReceiptResponse(Schema):
    """Resposta da importação"""
    status: str
    receipt_id: int
    store_created: bool
    items_count: int


class ReceiptItemOut(Schema):
    """Schema para retornar item"""
    id: int
    name: str
    code: str
    quantity: Optional[float] = None
    unit: str
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    estimated_taxes: Optional[float] = None


class ReceiptOut(Schema):
    """Schema para retornar nota completa"""
    id: int
    store_name: str
    store_cnpj: str
    number: str
    series: str
    issued_at: Optional[datetime] = None
    total: Optional[float] = None
    discount: float
    total_taxes: Optional[float] = None
    payment_method: str
    access_key: str
    items: List[ReceiptItemOut] = []


class ReceiptListOut(Schema):
    """Schema para listar notas (versão resumida)"""
    id: int
    store_name: str
    total: Optional[float] = None
    issued_at: Optional[datetime] = None
    items_count: int