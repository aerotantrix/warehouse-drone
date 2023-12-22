from typing import List, Dict
from pydantic import BaseModel


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
