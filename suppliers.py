from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

@router.post("/", response_model=schemas.SupplierOut)
def create_supplier(s: schemas.SupplierBase, db: Session = Depends(get_db)):
    m = models.Supplier(**s.dict())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.get("/", response_model=list[schemas.SupplierOut])
def list_suppliers(db: Session = Depends(get_db)):
    return db.query(models.Supplier).all()