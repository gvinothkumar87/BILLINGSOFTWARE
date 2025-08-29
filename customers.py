from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=schemas.CustomerOut)
def create_customer(c: schemas.CustomerBase, db: Session = Depends(get_db)):
    m = models.Customer(**c.dict())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.get("/", response_model=list[schemas.CustomerOut])
def list_customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).all()