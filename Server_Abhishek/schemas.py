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


