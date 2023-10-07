# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./socomec.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

from typing import Optional
from sqlalchemy import create_engine
from sqlmodel import Field, Session, SQLModel, create_engine

# Create a SQLAlchemy engine and connect to your database
DB_FILE = "test.db"
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)


# Define SQLModel classes for Addresses, Meters, and Readings tables
class Address(SQLModel, table=True):
    address_id: Optional[int] = Field(default=None, primary_key=True)
    address_text: str


class Meter(SQLModel, table=True):
    meter_id: Optional[int] = Field(default=None, primary_key=True)
    meter_name: str | None = None
    address_id: int


class Reading(SQLModel, table=True):
    reading_id: Optional[int] = Field(default=None, primary_key=True)
    meter_id: int
    reading_value: int
    reading_date: str  # Assuming you're using SQLite; adjust for other databases


# Create the tables in the database
# create_table(engine, Address)
# create_table(engine, Meter)
# create_table(engine, Reading)
def create_tables():
    SQLModel.metadata.create_all()


# # Optionally, create the unique index if it doesn't exist (SQLite specific)
# with Session(engine) as session:
#     session.execute(
#         "CREATE UNIQUE INDEX IF NOT EXISTS MeterReadingDate on Readings (MeterID, ReadingDate)"
#     )


if __name__ == "__main__":
    create_tables()
