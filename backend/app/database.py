import os
import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:   
    raise RuntimeError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class Base(DeclarativeBase):
    pass

