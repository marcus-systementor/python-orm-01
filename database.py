from getpass import getpass
import os
from sqlalchemy import URL, create_engine


def make_engine(database="course_storage", echo=False):
    user = os.getenv("DB_USER") or input("MySQL-användare: ").strip()
    password = os.getenv("DB_PASSWORD")
    if password is None:
        password = getpass("MySQL-lösenord: ")
    url = URL.create(
        "mysql+mysqlconnector", username=user, password=password,
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")), database=database,
    )
    return create_engine(url, echo=echo)
