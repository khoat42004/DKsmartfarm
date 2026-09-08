from fastapi import FastAPI
from backend.app.api import sensors, devices

app = FastAPI(
    title="Smart Farm AIoT API",
    description="Hệ thống Backend quản lý nông trại thông minh (Chim cảnh Đức Khoa)",
    version="1.0.0"
)

# Đăng ký các router API
app.include_router(sensors.router)
app.include_router(devices.router)

@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "Chào mừng bạn đến với hệ thống Smart Farm Backend!",
        "docs_url": "/docs"
    }