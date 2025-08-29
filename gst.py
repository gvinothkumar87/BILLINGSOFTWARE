from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models
from ..utils.gst_utils import einvoice_json, ewaybill_json

router = APIRouter(prefix="/gst", tags=["gst"])

@router.get("/gstr1")
def gstr1(db: Session = Depends(get_db)):
    # Very simplified — group sales by HSN/tax
    sales = db.query(models.SalesInvoice).all()
    return {"count": len(sales), "invoices": [s.invoice_no for s in sales]}

@router.get("/gstr2")
def gstr2(db: Session = Depends(get_db)):
    purchases = db.query(models.PurchaseInvoice).all()
    return {"count": len(purchases)}

@router.get("/gstr3b")
def gstr3b(db: Session = Depends(get_db)):
    # Simplified tax liability/ITC summary
    out_tax = sum(s.tax_total for s in db.query(models.SalesInvoice).all())
    in_tax = sum(p.tax_total for p in db.query(models.PurchaseInvoice).all())
    return {"output_tax": out_tax, "input_tax": in_tax, "net_tax_payable": max(out_tax - in_tax, 0.0)}

@router.get("/einvoice/{invoice_id}")
def einvoice(invoice_id: int, db: Session = Depends(get_db)):
    inv = db.query(models.SalesInvoice).get(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    items = db.query(models.SalesItem).filter(models.SalesItem.invoice_id == invoice_id).all()
    # Company (seller) from location
    loc = db.query(models.Location).get(inv.location_id)
    cust = db.query(models.Customer).get(inv.customer_id)
    item_payloads = []
    for it in items:
        prod = db.query(models.Product).get(it.product_id)
        item_payloads.append({"name": prod.name if prod else "Item", "hsn": prod.hsn if prod else None, "qty": it.qty, "rate": it.rate, "tax_percent": it.tax_percent, "unit": prod.unit if prod else "NOS"})
    payload = einvoice_json(inv, item_payloads, {"name": loc.name, "address": loc.address, "gstin": loc.gstin}, {"name": cust.name, "address": cust.address, "gstin": cust.gstin})
    return payload

@router.get("/ewaybill/{invoice_id}")
def ewaybill(invoice_id: int, db: Session = Depends(get_db)):
    inv = db.query(models.SalesInvoice).get(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    items = db.query(models.SalesItem).filter(models.SalesItem.invoice_id == invoice_id).all()
    loc = db.query(models.Location).get(inv.location_id)
    cust = db.query(models.Customer).get(inv.customer_id)
    item_payloads = []
    for it in items:
        prod = db.query(models.Product).get(it.product_id)
        item_payloads.append({"name": prod.name if prod else "Item", "hsn": prod.hsn if prod else None, "qty": it.qty, "rate": it.rate, "tax_percent": it.tax_percent, "unit": prod.unit if prod else "NOS"})
    payload = ewaybill_json(inv, item_payloads, {"name": loc.name, "address": loc.address, "gstin": loc.gstin}, {"name": cust.name, "address": cust.address, "gstin": cust.gstin})
    return payload