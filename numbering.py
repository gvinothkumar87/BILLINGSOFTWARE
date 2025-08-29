from sqlalchemy.orm import Session
from ..models import Location

def next_invoice_number(db: Session, location_id: int) -> str:
    loc = db.query(Location).get(location_id)
    if not loc:
        raise ValueError("Invalid location")
    loc.last_invoice_number = (loc.last_invoice_number or 0) + 1
    db.add(loc)
    db.flush()
    return f"{loc.code}-{loc.last_invoice_number:04d}"