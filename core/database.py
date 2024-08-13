
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from models.base import Base
from sqlalchemy import event

connection_url = URL.create(
    "mssql+aioodbc",
    # username="scott",
    # password="tiger",
    host="localhost",
    # port=1434,
    database="devdb",
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "TrustServerCertificate": "yes",
        "authentication": "ActiveDirectoryIntegrated",
    },
)

# Copied from the connection url above. Hard coded the URL to use it in alembic as well
SQLALCHEMY_DATABASE_URL = "mssql+aioodbc://localhost/devdb?TrustServerCertificate=yes&authentication=ActiveDirectoryIntegrated&driver=ODBC+Driver+17+for+SQL+Server"
# SQLALCHEMY_DATABASE_URL = "sqlite:///middleware.db"

async_engine = create_async_engine(
    connection_url, echo=False
)

# This is needed to Ensure the application of crud constraints
# @event.listens_for(engine, "connect")
# def enable_sqlite_fks(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()


AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine.sync_engine)


async def create_all():
    """
    creates all database tables
    todo to be replaced with async alembic later
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


def get_sync_db():
    with SyncSessionLocal() as db:
        yield db
