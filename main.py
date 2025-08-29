from fastapi import FastAPI
from .db import Base, engine, SessionLocal
from . import models
from .auth import router as auth_router, get_password_hash
from .routers import users, locations, customers, suppliers, products, sales, purchases, payments, expenses, reports, stock, gst

app = FastAPI(title="GST Billing Backend", version="0.1.0")

# Create tables
Base.metadata.create_all(bind=engine)

# Seed default locations (A,B,C,D) and admin user if not exists
def seed():
    db = SessionLocal()
    try:
        # Locations
        loc_codes = ["A","B","C","D"]
        for c in loc_codes:
            exists = db.query(models.Location).filter(models.Location.code == c).first()
            if not exists:
                db.add(models.Location(code=c, name=f"Location {c}", address=f"Address {c}", gstin=f"00AAAAA0000A1Z{loc_codes.index(c)}"))
        # Admin user
        if not db.query(models.User).filter(models.User.username=="admin").first():
            admin = models.User(username="admin", password_hash=get_password_hash("admin123"), role=models.RoleEnum.admin)
            db.add(admin)
        db.commit()
    finally:
        db.close()

seed()

# Routers
app.include_router(auth_router)
app.include_router(users.router)
app.include_router(locations.router)
app.include_router(customers.router)
app.include_router(suppliers.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(purchases.router)
app.include_router(payments.router)
app.include_router(expenses.router)
app.include_router(reports.router)
app.include_router(stock.router)
app.include_router(gst.router)

@app.get("/health")
def health():
    return {"status":"ok"}