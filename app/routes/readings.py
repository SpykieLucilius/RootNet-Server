from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Module, Reading
from ..schemas import (
    ReadingCreate,
    ReadingCreateResponse,
    ReadingsListOut,
)

router = APIRouter(prefix="/readings", tags=["readings"])


@router.post("", response_model=ReadingCreateResponse, status_code=201)
def create_reading(payload: ReadingCreate, db: Session = Depends(get_db)):
    mac = payload.mac_address.upper()

    module = db.query(Module).filter(Module.mac_address == mac).first()
    if module is None:
        # auto-register unknown module
        short = mac.replace(":", "")[-4:].lower()
        module = Module(mac_address=mac, name=f"module-{short}")
        db.add(module)
        db.flush()  # gets us module.id without committing yet

    now = datetime.utcnow()
    reading = Reading(
        module_id=module.id,
        timestamp=now,
        soil_moisture=payload.soil_moisture,
        temperature=payload.temperature,
        humidity=payload.humidity,
        light_lux=payload.light_lux,
        light_red=payload.light_red,
        light_green=payload.light_green,
        light_blue=payload.light_blue,
        battery_voltage=payload.battery_voltage,
    )
    module.last_seen_at = now

    db.add(reading)
    db.commit()
    db.refresh(reading)

    return ReadingCreateResponse(status="ok", reading_id=reading.id)


@router.get("", response_model=ReadingsListOut)
def list_readings(
    module_id: Optional[int] = Query(None),
    since: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    q = db.query(Reading)
    if module_id is not None:
        q = q.filter(Reading.module_id == module_id)
    if since is not None:
        q = q.filter(Reading.timestamp >= since)

    q = q.order_by(Reading.timestamp.desc()).limit(limit)
    readings = q.all()
    return ReadingsListOut(count=len(readings), readings=readings)
