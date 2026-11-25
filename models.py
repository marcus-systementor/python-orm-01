from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def normalize_name(name):
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("Namn måste anges")
    if len(clean_name) > 100:
        raise ValueError("Namnet får ha högst 100 tecken")
    return clean_name


class Customer(Base):
    __tablename__ = "customers"
    customer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(100))

    def rename(self, name):
        self.name = normalize_name(name)
