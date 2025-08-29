from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..auth import get_password_hash
from ..deps import require_roles

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserOut, dependencies=[Depends(require_roles(models.RoleEnum.admin))])
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = models.User(
        username=payload.username,
        password_hash=get_password_hash(payload.password),
        role=payload.role,
        assigned_location_id=payload.assigned_location_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/", dependencies=[Depends(require_roles(models.RoleEnum.admin))])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()