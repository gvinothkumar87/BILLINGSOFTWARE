from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models
from ..utils.export_utils import to_csv_stream

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/customer-ledger/{customer_id}")
def customer_ledger(customer_id: int, db: Session = Depends(get_db)):
    sales = db.query(models.SalesInvoice).filter(models.SalesInvoice.customer_id == customer_id).all()
    pays  = db.query(models.PaymentCustomer).filter(models.PaymentCustomer.customer_id == customer_id).all()
    entries = []
    balance = 0.0
    for s in sales:
        balance += s.grand_total
        entries.append({"type":"invoice","date":s.date,"ref":s.invoice_no,"debit":s.grand_total,"credit":0.0,"balance":balance})
    for p in pays:
        balance -= p.amount
        entries.append({"type":"receipt","date":p.date,"ref":p.id,"debit":0.0,"credit":p.amount,"balance":balance})
    entries.sort(key=lambda x: x["date"])
    return entries

@router.get("/supplier-ledger/{supplier_id}")
def supplier_ledger(supplier_id: int, db: Session = Depends(get_db)):
    purchases = db.query(models.PurchaseInvoice).filter(models.PurchaseInvoice.supplier_id == supplier_id).all()
    pays  = db.query(models.PaymentSupplier).filter(models.PaymentSupplier.supplier_id == supplier_id).all()
    entries = []
    balance = 0.0
    for s in purchases:
        balance += s.grand_total
        entries.append({"type":"purchase","date":s.date,"ref":s.supplier_invoice_no,"debit":s.grand_total,"credit":0.0,"balance":balance})
    for p in pays:
        balance -= p.amount
        entries.append({"type":"payment","date":p.date,"ref":p.id,"debit":0.0,"credit":p.amount,"balance":balance})
    entries.sort(key=lambda x: x["date"])
    return entries

@router.get("/cash-account")
def cash_account(db: Session = Depends(get_db)):
    outs = db.query(models.PaymentSupplier).all()
    ins  = db.query(models.PaymentCustomer).all()
    exps = db.query(models.Expense).all()
    recs = db.query(models.Receipt).all()
    total_in = sum(r.amount for r in ins) + sum(r.amount for r in recs)
    total_out = sum(r.amount for r in outs) + sum(r.amount for r in exps)
    return {"total_in": total_in, "total_out": total_out, "balance": total_in-total_out}

@router.get("/pl")
def profit_and_loss(db: Session = Depends(get_db)):
    sales = sum(s.grand_total for s in db.query(models.SalesInvoice).all())
    purchases = sum(p.grand_total for p in db.query(models.PurchaseInvoice).all())
    expenses = sum(e.amount for e in db.query(models.Expense).all())
    # Very simplified P&L (without COGS logic). Adjust as needed.
    return {"sales": sales, "purchases": purchases, "expenses": expenses, "profit": sales - purchases - expenses}

@router.get("/balance-sheet")
def balance_sheet(db: Session = Depends(get_db)):
    # Basic placeholders. Extend with receivables/payables, inventory valuation, capital, etc.
    stock_value = sum((p.stock_qty or 0)*(p.price or 0) for p in db.query(models.Product).all())
    cash = 0.0  # compute from cash ledger if maintained
    assets = {"stock": stock_value, "cash": cash}
    liabilities = {"payables": 0.0}
    equity = {"capital": 0.0, "retained": 0.0}
    return {"assets": assets, "liabilities": liabilities, "equity": equity}

@router.get("/export/customers.csv")
def export_customers(db: Session = Depends(get_db)):
    rows = [{"id": c.id, "name": c.name, "phone": c.phone, "gstin": c.gstin} for c in db.query(models.Customer).all()]
    return to_csv_stream("customers.csv", rows, headers=["id","name","phone","gstin"])