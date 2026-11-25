from __future__ import annotations
import argparse
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from database import make_engine


class RelationBase(DeclarativeBase):
    pass


class Customer(RelationBase):
    __tablename__ = "customers"
    customer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(100))
    orders: Mapped[list[Order]] = relationship(back_populates="customer")


class Order(RelationBase):
    __tablename__ = "orders"
    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id"))
    description: Mapped[str] = mapped_column(String(100))
    customer: Mapped[Customer] = relationship(back_populates="orders")


def read_customer_orders(engine, customer_id):
    with Session(engine) as session:
        customer = session.get(Customer, customer_id)
        if customer is None:
            return None
        # Access the relationship before closing the session.
        return {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "orders": [
                {"order_id": order.order_id, "customer_id": order.customer_id,
                 "description": order.description}
                for order in sorted(customer.orders, key=lambda order: order.order_id)
            ],
        }


def main():
    parser = argparse.ArgumentParser(description="Läs en kund och kundens orders")
    parser.add_argument("customer_id", type=int, nargs="?", default=1)
    parser.add_argument("--sql", action="store_true")
    args = parser.parse_args()
    engine = make_engine(database="orm_relations_lab", echo=args.sql)
    try:
        result = read_customer_orders(engine, args.customer_id)
        if result is None:
            print("Kunden saknas")
        else:
            print(f"Kund {result['customer_id']}: {result['name']}")
            if not result["orders"]:
                print("Inga orders")
            for order in result["orders"]:
                print(f"Order {order['order_id']}: {order['description']}")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
