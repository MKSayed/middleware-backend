from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import event

connection_url = URL.create(
    "mssql+pyodbc",
    # username="scott",
    # password="tiger",
    host="localhost",
    # port=1434,
    database="testdb",
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "TrustServerCertificate": "yes",
        "authentication": "ActiveDirectoryIntegrated",
    },
)

# SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://@localhost/testdb?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&authentication=ActiveDirectoryIntegrated"
# SQLALCHEMY_DATABASE_URL = "sqlite:///middleware.db"

engine = create_engine(
    connection_url, echo=True
)

# This is needed to Ensure the application of crud constraints
# @event.listens_for(engine, "connect")
# def enable_sqlite_fks(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    with Session(engine) as session:
        yield session
