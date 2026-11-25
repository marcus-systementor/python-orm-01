import argparse
from sqlalchemy.orm import Session
from database import make_engine
from main import read_customer
from models import Customer, normalize_name


def rename_customer(engine, customer_id, new_name):
    # Task 2: begin a transaction, get the customer, handle missing ID,
    # call customer.rename(new_name), then let the block commit.
    raise NotImplementedError("Fyll i rename_customer enligt uppgift 2")


def create_customer(engine, customer_id, name):
    # Task 3: use your own free test ID, normalize the name, reject an
    # existing ID and add one Customer inside a transaction.
    raise NotImplementedError("Fyll i create_customer enligt uppgift 3")


def delete_test_customer(engine, customer_id):
    # Task 3: this guard limits deletion to the lab's test-ID range.
    if customer_id < 9000:
        raise ValueError("Använd bara din egen testpost med ID 9000 eller högre")
    # Get the object, handle missing ID and delete inside a transaction.
    raise NotImplementedError("Fyll i delete_test_customer enligt uppgift 3")


def main():
    parser = argparse.ArgumentParser(description="Dina ORM-uppgifter")
    parser.add_argument("action", choices=["rename", "create", "delete"])
    parser.add_argument("customer_id", type=int)
    parser.add_argument("name", nargs="?")
    parser.add_argument("--sql", action="store_true")
    args = parser.parse_args()
    if args.action != "delete" and args.name is None:
        parser.error("Ange namnet inom citattecken")
    engine = make_engine(echo=args.sql)
    try:
        if args.action == "rename":
            rename_customer(engine, args.customer_id, args.name)
        elif args.action == "create":
            create_customer(engine, args.customer_id, args.name)
        else:
            delete_test_customer(engine, args.customer_id)
        print("Ny läsning:", read_customer(engine, args.customer_id))
    except (NotImplementedError, ValueError, LookupError) as error:
        print(error)
        raise SystemExit(2)
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
