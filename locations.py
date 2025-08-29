from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..deps import require_roles

router = APIRouter(prefix="/locations", tags=["locations"])

@router.post("/", response_model=schemas.LocationOut, dependencies=[Depends(require_roles(models.RoleEnum.admin))])
def create_location(loc: schemas.LocationBase, db: Session = Depends(get_db)):
    if db.query(models.Location).filter(models.Location.code == loc.code).first():
        raise HTTPException(status_code=400, detail="Code already exists")
    m = models.Location(**loc.dict())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.get("/")
def list_locations(db: Session = Depends(get_db)):
    return db.query(models.Location).all()