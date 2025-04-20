from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class DeviceMessage(Base):
    __tablename__ = "device_messages"

    id = Column(Integer, primary_key=True)
    device_id = Column(String, nullable=True)
    topic = Column(String, nullable=True)
    payload = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
