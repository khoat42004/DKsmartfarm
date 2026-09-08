import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from backend.app.api import sensors, devices

app = FastAPI(
    title="Smart Farm AIoT API",
    description="Hệ thống Backend quản lý nông trại thông minh (Chim cảnh Đức Khoa)",
    version="1.0.0"
)

# Đăng ký các router API
app.include_router(sensors.router, prefix="/api/sensors", tags=["Sensors"])
app.include_router(devices.router, prefix="/api/devices", tags=["Devices"])

# Đường dẫn tới thư mục frontend
frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend")

@app.get("/", include_in_schema=False)
def read_root():
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "status": "online",
        "message": "Smart Farm API is running",
        "docs_url": "/docs"
    }
