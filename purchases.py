from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/purchases", tags=["purchases"])

@router.post("/invoice", response_model=schemas.PurchaseInvoiceOut)
def create_purchase(payload: schemas.PurchaseInvoiceIn, db: Session = Depends(get_db)):
    supp = db.query(models.Supplier).get(payload.supplier_id)
    if not supp:
        raise HTTPException(status_code=400, detail="Invalid supplier")

    subtotal = 0.0
    tax_total = 0.0
    for it in payload.items:
        line = it.qty * it.rate
        tax = line * (it.tax_percent/100.0)
        subtotal += line
        tax_total += tax
    grand = round(subtotal + tax_total, 2)

    inv = models.PurchaseInvoice(
        supplier_id=payload.supplier_id,
        supplier_invoice_no=payload.supplier_invoice_no,
        subtotal=round(subtotal,2),
        tax_total=round(tax_total,2),
        grand_total=grand,
    )
    db.add(inv)
    db.flush()

    for it in payload.items:
        db.add(models.PurchaseItem(
            purchase_id=inv.id,
            product_id=it.product_id,
            qty=it.qty,
            rate=it.rate,
            tax_percent=it.tax_percent,
            line_total=round(it.qty*it.rate*(1+it.tax_percent/100.0),2),
        ))
        # increment stock
        prod = db.query(models.Product).get(it.product_id)
        if prod:
            prod.stock_qty = (prod.stock_qty or 0) + it.qty
            db.add(prod)

    db.commit()
    db.refresh(inv)
    return inv

@router.get("/invoices")
def list_purchases(db: Session = Depends(get_db)):
    return db.query(models.PurchaseInvoice).order_by(models.PurchaseInvoice.id.desc()).all()