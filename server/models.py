from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    username = Column(String(32), nullable=False, primary_key=True)
    name = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(256), unique=True, nullable=False)


class TokenTable(Base):
    __tablename__ = "tokens"
    username = Column(String(32))
    access_token = Column(String(512), primary_key=True)
    status = Column(Boolean)
    created_datetime = Column(DateTime, default=datetime.now)


class RpiStation(Base):
    __tablename__ = "rpistations"
    stationname = Column(String(32), primary_key=True)
    password = Column(String(256), unique=True, nullable=False)
    battery = Column(Integer, nullable=True)


class Bin(Base):
    __tablename__ = "bins"
    bin_id = Column(String(32), nullable=False, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.now)
    row = Column(Integer, nullable=False)
    col = Column(Integer, nullable=False)
    rack = Column(Integer, nullable=False)
    drone_name = Column(String(32), ForeignKey(RpiStation.stationname), nullable=False)
