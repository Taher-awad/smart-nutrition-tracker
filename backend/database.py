from sqlmodel import SQLModel, create_engine, Session
import os

# Create engine
sqlite_url = os.getenv("DATABASE_URL", "sqlite:///database.db")

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
