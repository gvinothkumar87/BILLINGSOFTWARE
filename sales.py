from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..deps import require_roles, current_location_restricted, get_current_user
from ..utils.numbering import next_invoice_number

router = APIRouter(prefix="/sales", tags=["sales"])

@router.post("/invoice", response_model=schemas.SalesInvoiceOut, dependencies=[Depends(require_roles(models.RoleEnum.admin, models.RoleEnum.accountant, models.RoleEnum.billing))])
def create_invoice(payload: schemas.SalesInvoiceIn, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    # If billing staff, restrict location
    if user.role == models.RoleEnum.billing and user.assigned_location_id and payload.location_id != user.assigned_location_id:
        raise HTTPException(status_code=403, detail="Billing restricted to assigned location")

    # Validate foreign keys
    loc = db.query(models.Location).get(payload.location_id)
    cust = db.query(models.Customer).get(payload.customer_id)
    if not loc or not cust:
        raise HTTPException(status_code=400, detail="Invalid location or customer")

    invoice_no = next_invoice_number(db, payload.location_id)

    subtotal = 0.0
    tax_total = 0.0
    for it in payload.items:
        line = it.qty * it.rate
        tax = line * (it.tax_percent/100.0)
        subtotal += line
        tax_total += tax

    grand = round(subtotal + tax_total - payload.discount_total + payload.round_off, 2)

    inv = models.SalesInvoice(
        invoice_no=invoice_no,
        location_id=payload.location_id,
        customer_id=payload.customer_id,
        payment_type=payload.payment_type,
        place_of_supply=payload.place_of_supply,
        subtotal=round(subtotal,2),
        tax_total=round(tax_total,2),
        discount_total=round(payload.discount_total,2),
        round_off=round(payload.round_off,2),
        grand_total=grand,
    )
    db.add(inv)
    db.flush()  # get inv.id

    for it in payload.items:
        db.add(models.SalesItem(
            invoice_id=inv.id,
            product_id=it.product_id,
            qty=it.qty,
            rate=it.rate,
            tax_percent=it.tax_percent,
            line_total=round(it.qty*it.rate*(1+it.tax_percent/100.0),2),
        ))
        # decrement stock
        prod = db.query(models.Product).get(it.product_id)
        if prod:
            prod.stock_qty = (prod.stock_qty or 0) - it.qty
            db.add(prod)

    db.commit()
    db.refresh(inv)
    return inv

@router.get("/invoices")
def list_invoices(db: Session = Depends(get_db)):
    return db.query(models.SalesInvoice).order_by(models.SalesInvoice.id.desc()).all()