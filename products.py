from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=schemas.ProductOut)
def create_product(p: schemas.ProductBase, db: Session = Depends(get_db)):
    m = models.Product(**p.dict())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.get("/", response_model=list[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()