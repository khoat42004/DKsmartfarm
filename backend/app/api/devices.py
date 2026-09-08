from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.database.database import get_db
from backend.app.models.models import Device

router = APIRouter(prefix="/api/devices", tags=["Devices"])

class DeviceCreate(BaseModel):
    zone_id: int
    device_code: str
    device_type: str  # Ví dụ: DHT22, PIR, Relay

@router.post("/register")
def register_device(data: DeviceCreate, db: Session = Depends(get_db)):
    # Kiểm tra xem mã thiết bị đã tồn tại chưa
    existing_device = db.query(Device).filter(Device.device_code == data.device_code).first()
    if existing_device:
        raise HTTPException(status_code=400, detail="Mã thiết bị này đã tồn tại trong hệ thống!")

    new_device = Device(
        zone_id=data.zone_id,
        device_code=data.device_code,
        device_type=data.device_type,
        status="online"
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return {
        "status": "success",
        "message": "Đăng ký thiết bị thành công!",
        "device_id": new_device.id,
        "device_code": new_device.device_code
    }