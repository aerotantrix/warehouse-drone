from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    name: str
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str


class RequestDetails(BaseModel):
    username: str
    password: str


class StationCreate(BaseModel):
    station_name: str
    password: str
    battery: int


class UserDetails(BaseModel):
    name: str
    email: str


class StationDetails(BaseModel):
    station_name: str
    battery: int


class AddSchedule(BaseModel):
    station_name: str
    schedule_time: datetime


class InsertBin(BaseModel):
    bin_id: str
    row: int
    rack: int
    shelf: int
    status: bool
    station_name: str
