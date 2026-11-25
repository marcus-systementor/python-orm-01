import argparse
from sqlalchemy.orm import Session
from database import make_engine
from models import Customer


def read_customer(engine, customer_id):
    with Session(engine) as session:
        customer = session.get(Customer, customer_id)
        if customer is None:
            return None
        # Copy ordinary values while the session is open.
        return {"customer_id": customer.customer_id, "name": customer.name}


def main():
    parser = argparse.ArgumentParser(description="Läs en kund med ORM")
    parser.add_argument("customer_id", type=int, nargs="?", default=1)
    parser.add_argument("--sql", action="store_true", help="Visa SQL-loggen")
    args = parser.parse_args()
    engine = make_engine(echo=args.sql)
    try:
        customer = read_customer(engine, args.customer_id)
        print("Kunden saknas" if customer is None else customer)
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
