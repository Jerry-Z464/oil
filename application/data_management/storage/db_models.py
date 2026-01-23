from sqlalchemy import Column, String, Text, BIGINT, FLOAT, ForeignKey
from sqlalchemy.dialects.mssql import TINYINT
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Device(Base):
    __tablename__ = 'device'

    id = Column(String(50), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    last_update_time = Column(BIGINT, nullable=False)
    status = Column(TINYINT, nullable=False)

    data_records = relationship("DeviceData", back_populates="device")


class DeviceData(Base):
    __tablename__ = 'device_data'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    device_id = Column(String(50), ForeignKey('device.id'), index=True, nullable=False)
    cmt5_time = Column(BIGINT, nullable=False)
    dP = Column(FLOAT, nullable=False)
    gVF = Column(FLOAT, nullable=False)
    gasFlowRate = Column(FLOAT, nullable=False)
    liquidFlowRate = Column(FLOAT, nullable=False)
    oilFlowRate = Column(FLOAT, nullable=False)
    pressure = Column(FLOAT, nullable=False)
    temperature = Column(FLOAT, nullable=False)
    waterCut = Column(FLOAT, nullable=False)
    waterFlowRate = Column(FLOAT, nullable=False)

    device = relationship("Device", back_populates="data_records")


class Alert(Base):
    __tablename__ = "alert"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    device_id = Column(String(50), index=True, nullable=False)
    alert_type = Column(TINYINT, nullable=False)
    message = Column(String(200), nullable=False)
    created_at = Column(BIGINT, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    timestamp = Column(BIGINT, index=True, nullable=False)
    event_type = Column(String(50), index=True, nullable=False)
    device_id = Column(String(50), index=True, nullable=False)


class Setting(Base):
    __tablename__ = 'setting'

    key = Column(String(50), unique=True, nullable=False, primary_key=True)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
