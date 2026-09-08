import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load biến môi trường từ file .env ở thư mục gốc
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/smartfarm")

# Khởi tạo SQLAlchemy Engine
engine = create_engine(DATABASE_URL)

# Tạo SessionLocal để thao tác với database (CRUD)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho các model kế thừa
Base = declarative_base()

# Dependency để lấy DB session cho các API FastAPI sau này
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()