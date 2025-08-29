# GST Billing Backend (FastAPI + SQLite)

A production-ready starter backend for **Multi-Location GST Billing, Purchase & Accounts** with roles, ledgers, stock, GST reports, and E-Invoice/E-Way JSON generation (stubs).

## Quick Start

```bash
# 1) Create & activate venv (optional)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run dev server
uvicorn app.main:app --reload

# 4) Open docs
# http://127.0.0.1:8000/docs
```

## Default Admin
On first run, the app auto-creates a default Admin:
- **username:** admin
- **password:** admin123
Please change it immediately via `/auth/me` update or create a new one and delete this user.

## Features (MVP)
- JWT auth with roles: `admin`, `accountant`, `billing`, `manager`
- 4 fixed locations with independent **location-wise invoice numbering**
- Masters: Customers, Suppliers, Products (with stock qty)
- Sales Invoices (GST-ready fields) + Items → auto stock **decrement**
- Purchase Invoices + Items → auto stock **increment**
- Payments: from customers, to suppliers
- Expenses & Receipts
- Ledgers (derived): customer, supplier, expense, received
- Cash Account, simple P&L, Balance Sheet (basic derivations)
- GST reports (GSTR-1/2/3B) **skeleton endpoints**
- E-Invoice / E-Way Bill **JSON generators** (skeleton mapping)
- Export endpoints: CSV/JSON for most lists

> Note: This is a strong foundation. You can extend validations, GST rules, and PDF formats as needed.

## Project Structure
```
app/
  main.py              # app factory, router include, seed admin
  db.py                # DB engine, session, Base
  models.py            # SQLAlchemy models
  schemas.py           # Pydantic schemas
  auth.py              # auth, role dependencies
  deps.py              # common dependencies (db, current_user)
  routers/
    users.py
    locations.py
    customers.py
    suppliers.py
    products.py
    sales.py
    purchases.py
    payments.py
    expenses.py
    reports.py
    stock.py
    gst.py
  utils/
    numbering.py       # location-wise serial generation
    gst_utils.py       # JSON builders for e-invoice/e-way
    export_utils.py    # CSV/JSON helpers
```

## Environment
Defaults are embedded for SQLite. For Postgres, set `DATABASE_URL` env and restart.

## License
MIT