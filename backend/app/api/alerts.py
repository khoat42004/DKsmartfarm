from datetime import datetime
from typing import Optional
from backend.app.database.database import get_db
from backend.app.models.models import AIAlert
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/alerts", tags=["AI Alerts"])


# Khung dữ liệu Pydantic nhận từ Laptop Camera
class AlertCreate(BaseModel):
  target_type: str  # 'ran', 'chuot', 'stranger', 'known'
  confidence: float
  image_base64: Optional[str] = None


@router.post("")
def receive_alert(data: AlertCreate, db: Session = Depends(get_db)):
  """API nhận dữ liệu và hình ảnh cảnh báo từ camera gửi lên."""
  try:
    new_alert = AIAlert(
        target_type=data.target_type,
        confidence=data.confidence,
        image_base64=data.image_base64,
        created_at=datetime.utcnow(),
    )
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return {
      "status": "success",
      "message": "Đã lưu bản ghi cảnh báo thành công!",
      "alert_id": new_alert.id,
      "target_type": new_alert.target_type,
    }
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f"Lỗi lưu cảnh báo: {str(e)}")


@router.get("")
def get_alerts(limit: int = 20, db: Session = Depends(get_db)):
  """API cho giao diện Web (Frontend) lấy danh sách 20 cảnh báo mới nhất."""
  alerts = (
      db.query(AIAlert).order_by(AIAlert.created_at.desc()).limit(limit).all()
  )

  results = []
  for a in alerts:
    results.append({
        "id": a.id,
        "target_type": a.target_type,
        "confidence": a.confidence,
        "image_base64": a.image_base64,
        "created_at": a.created_at.strftime("%Y-%m-%d %H:%M:%S")
        if a.created_at
        else None,
    })

  return {"status": "success", "total": len(results), "data": results}