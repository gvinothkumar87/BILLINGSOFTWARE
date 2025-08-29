from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/from-customer")
def receive_from_customer(p: schemas.PaymentCustomerIn, db: Session = Depends(get_db)):
    m = models.PaymentCustomer(**p.dict())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.post("/to-supplier")
def pay_to_supplier(p: schemas.PaymentSupplierIn, db: Session = Depends(get_db)):
    m = models.PaymentSupplier(**p.dict())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m