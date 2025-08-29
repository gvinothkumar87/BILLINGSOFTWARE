from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from .models import RoleEnum

class UserBase(BaseModel):
    username: str
    role: RoleEnum
    assigned_location_id: Optional[int] = None
    is_active: bool = True

class UserCreate(BaseModel):
    username: str
    password: str
    role: RoleEnum = RoleEnum.billing
    assigned_location_id: Optional[int] = None

class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LocationBase(BaseModel):
    code: str
    name: str
    address: Optional[str] = None
    gstin: Optional[str] = None
    contact: Optional[str] = None

class LocationOut(LocationBase):
    id: int
    last_invoice_number: int
    model_config = ConfigDict(from_attributes=True)

class CustomerBase(BaseModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    gstin: Optional[str] = None
    email: Optional[str] = None
    credit_limit: float = 0.0

class CustomerOut(CustomerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SupplierBase(BaseModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    gstin: Optional[str] = None
    email: Optional[str] = None

class SupplierOut(SupplierBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    unit: Optional[str] = None
    price: float = 0.0
    hsn: Optional[str] = None
    tax_percent: float = 0.0
    stock_qty: float = 0.0

class ProductOut(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SalesItemIn(BaseModel):
    product_id: int
    qty: float
    rate: float
    tax_percent: float

class SalesInvoiceIn(BaseModel):
    location_id: int
    customer_id: int
    payment_type: str = "Cash"
    place_of_supply: Optional[str] = None
    discount_total: float = 0.0
    round_off: float = 0.0
    items: List[SalesItemIn]

class SalesInvoiceOut(BaseModel):
    id: int
    invoice_no: str
    date: datetime
    location_id: int
    customer_id: int
    payment_type: str
    subtotal: float
    tax_total: float
    discount_total: float
    round_off: float
    grand_total: float
    model_config = ConfigDict(from_attributes=True)

class PurchaseItemIn(BaseModel):
    product_id: int
    qty: float
    rate: float
    tax_percent: float

class PurchaseInvoiceIn(BaseModel):
    supplier_id: int
    supplier_invoice_no: str
    items: List[PurchaseItemIn]

class PurchaseInvoiceOut(BaseModel):
    id: int
    date: datetime
    supplier_id: int
    supplier_invoice_no: str
    subtotal: float
    tax_total: float
    grand_total: float
    model_config = ConfigDict(from_attributes=True)

class PaymentCustomerIn(BaseModel):
    customer_id: int
    amount: float
    mode: str = "Cash"
    notes: Optional[str] = None

class PaymentSupplierIn(BaseModel):
    supplier_id: int
    amount: float
    mode: str = "Cash"
    notes: Optional[str] = None

class ExpenseIn(BaseModel):
    category: str
    amount: float
    notes: Optional[str] = None

class ReceiptIn(BaseModel):
    source: str
    amount: float
    notes: Optional[str] = None