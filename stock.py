from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models

router = APIRouter(prefix="/stock", tags=["stock"])

@router.get("/summary")
def stock_summary(db: Session = Depends(get_db)):
    prods = db.query(models.Product).all()
    return [{"id": p.id, "name": p.name, "stock_qty": p.stock_qty} for p in prods]