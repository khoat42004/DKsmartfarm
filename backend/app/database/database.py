import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Lấy DATABASE_URL từ biến môi trường của Render
DATABASE_URL = os.getenv("DATABASE_URL")

# Chuẩn hóa tiền tố cho SQLAlchemy + psycopg (Render thường cấp postgres:// hoặc postgresql://)
if DATABASE_URL:
  if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://", "postgresql+psycopg://", 1
    )
  elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )
else:
  # Dự phòng nếu chạy local không có biến môi trường
  DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Tự động kết nối lại nếu bị đứt kết nối
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
