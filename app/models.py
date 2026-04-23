from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    mac_address = Column(String(17), unique=True, nullable=False, index=True)
    name = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_seen_at = Column(DateTime, nullable=True)

    readings = relationship(
        "Reading",
        back_populates="module",
        cascade="all, delete-orphan",
    )


class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(
        Integer,
        ForeignKey("modules.id"),
        nullable=False,
        index=True,
    )
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    soil_moisture = Column(Integer, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    light_lux = Column(Float, nullable=True)
    light_red = Column(Integer, nullable=True)
    light_green = Column(Integer, nullable=True)
    light_blue = Column(Integer, nullable=True)
    battery_voltage = Column(Float, nullable=True)

    module = relationship("Module", back_populates="readings")
