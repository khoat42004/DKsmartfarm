from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.database.database import get_db
from backend.app.models.models import SensorReading, Device

router = APIRouter(prefix="/api/sensors", tags=["Sensors"])

# Khung dữ liệu Pydantic để validate dữ liệu ESP32 gửi lên
class SensorDataCreate(BaseModel):
    device_code: str
    temperature: float
    humidity: float

@router.post("/data")
def receive_sensor_data(data: SensorDataCreate, db: Session = Depends(get_db)):
    # Tìm thiết bị trong database dựa trên device_code
    device = db.query(Device).filter(Device.device_code == data.device_code).first()
    if not device:
        raise HTTPException(status_code=404, detail="Mã thiết bị không tồn tại trong hệ thống!")

    # Lưu bản ghi cảm biến vào bảng sensor_readings
    db_reading = SensorReading(
        device_id=device.id,
        temperature=data.temperature,
        humidity=data.humidity
    )
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)

    return {
        "status": "success",
        "message": "Đã lưu dữ liệu cảm biến thành công!",
        "data": {
            "device_code": data.device_code,
            "temperature": data.temperature,
            "humidity": data.humidity
        }
    }