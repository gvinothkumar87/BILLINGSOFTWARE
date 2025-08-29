from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    accountant = "accountant"
    billing = "billing"
    manager = "manager"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.billing, nullable=False)
    assigned_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)  # e.g., A, B, C, D
    name = Column(String, nullable=False)
    address = Column(Text, nullable=True)
    gstin = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    last_invoice_number = Column(Integer, default=0)  # numeric counter per location
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    gstin = Column(String, nullable=True)
    email = Column(String, nullable=True)
    credit_limit = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    gstin = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    unit = Column(String, nullable=True)      # e.g., kg, bag, nos
    price = Column(Float, default=0.0)
    hsn = Column(String, nullable=True)
    tax_percent = Column(Float, default=0.0)  # GST %
    stock_qty = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SalesInvoice(Base):
    __tablename__ = "sales_invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_no = Column(String, unique=True, index=True) # e.g., A-0001
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    payment_type = Column(String, default="Cash")  # Cash/Credit
    place_of_supply = Column(String, nullable=True)
    subtotal = Column(Float, default=0.0)
    tax_total = Column(Float, default=0.0)
    discount_total = Column(Float, default=0.0)
    round_off = Column(Float, default=0.0)
    grand_total = Column(Float, default=0.0)

class SalesItem(Base):
    __tablename__ = "sales_items"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("sales_invoices.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    qty = Column(Float, default=0.0)
    rate = Column(Float, default=0.0)
    tax_percent = Column(Float, default=0.0)
    line_total = Column(Float, default=0.0)

class PurchaseInvoice(Base):
    __tablename__ = "purchase_invoices"
    id = Column(Integer, primary_key=True, index=True)
    supplier_invoice_no = Column(String, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    subtotal = Column(Float, default=0.0)
    tax_total = Column(Float, default=0.0)
    grand_total = Column(Float, default=0.0)

class PurchaseItem(Base):
    __tablename__ = "purchase_items"
    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchase_invoices.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    qty = Column(Float, default=0.0)
    rate = Column(Float, default=0.0)
    tax_percent = Column(Float, default=0.0)
    line_total = Column(Float, default=0.0)

class PaymentCustomer(Base):
    __tablename__ = "payment_customer"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    amount = Column(Float, default=0.0)
    mode = Column(String, default="Cash")
    notes = Column(Text, nullable=True)

class PaymentSupplier(Base):
    __tablename__ = "payment_supplier"
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    amount = Column(Float, default=0.0)
    mode = Column(String, default="Cash")
    notes = Column(Text, nullable=True)

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    category = Column(String, nullable=False)
    amount = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)

class Receipt(Base):
    __tablename__ = "receipts"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    source = Column(String, nullable=False)
    amount = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)