from sqlalchemy.orm import Session
from database import make_engine
from main import read_customer
from models import Customer


def demonstrate_rollback(engine, customer_id=1):
    before = read_customer(engine, customer_id)
    if before is None:
        raise LookupError("Kunden saknas")
    print("Före:", before["name"])
    with Session(engine) as session:
        customer = session.get(Customer, customer_id)
        customer.rename("Tillfälligt ORM-namn")
        session.flush()
        print("Efter flush:", customer.name)
        session.rollback()
    after = read_customer(engine, customer_id)
    print("Ny session efter rollback:", after["name"])
    return before, after


if __name__ == "__main__":
    engine = make_engine(echo=True)
    try:
        demonstrate_rollback(engine)
    finally:
        engine.dispose()
