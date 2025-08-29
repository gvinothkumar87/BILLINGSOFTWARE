from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/money", tags=["expenses/receipts"])

@router.post("/expense")
def add_expense(e: schemas.ExpenseIn, db: Session = Depends(get_db)):
    m = models.Expense(**e.dict())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.get("/expenses")
def list_expenses(db: Session = Depends(get_db)):
    return db.query(models.Expense).all()

@router.post("/receipt")
def add_receipt(r: schemas.ReceiptIn, db: Session = Depends(get_db)):
    m = models.Receipt(**r.dict())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.get("/receipts")
def list_receipts(db: Session = Depends(get_db)):
    return db.query(models.Receipt).all()