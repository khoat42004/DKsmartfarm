import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.app.api import alerts, devices, sensors
from backend.app.database.database import Base, engine

app = FastAPI(
    title="Smart Farm AIoT API",
    description=(
        "Hệ thống Backend quản lý nông trại thông minh (Chim cảnh Đức Khoa)"
    ),
    version="1.0.0",
)


# Khởi tạo bảng dữ liệu khi khởi động
@app.on_event("startup")
def startup_db_client():
  try:
    Base.metadata.create_all(bind=engine)
    print("[DATABASE] Đã kết nối và kiểm tra bảng thành công!")
  except Exception as e:
    print(f"[DATABASE CẢNH BÁO]: Chưa thể tạo bảng tự động ({e})")


# Đăng ký các router API
app.include_router(sensors.router)
app.include_router(devices.router)
app.include_router(alerts.router)

# Xác định đường dẫn thư mục frontend
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Phục vụ các tài nguyên tĩnh (css, js, ảnh) nếu có trong thư mục frontend
if os.path.exists(FRONTEND_DIR):
  app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


# Khi người dùng vào trang chủ "/", trả về file giao diện index.html
@app.get("/")
def read_root():
  index_path = os.path.join(FRONTEND_DIR, "index.html")
  if os.path.exists(index_path):
    return FileResponse(index_path)
  return {
      "status": "success",
      "message": "Chào mừng bạn đến với hệ thống Smart Farm Backend!",
      "docs_url": "/docs",
  }
