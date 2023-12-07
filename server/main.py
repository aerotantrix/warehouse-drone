import utils
import models
import asyncio
import schemas
import database
import auth_bearer
import numpy as np
import pandas as pd
import sqlalchemy

from functools import wraps
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Dict, List
from credentials import psql_credentials
from datetime import datetime
from celery.result import AsyncResult

# from celery_server import Tasks


database.Base.metadata.create_all(database.engine)


def get_session():
    session = database.local_session()
    try:
        yield session
    except:
        session.close()


app = FastAPI(
    title="Locus API",
    description="The Locus API provides the methods to automate your inventory management using drones.",
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def token_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        payload = auth_bearer.JWTBearer.decodeJWT(kwargs["dependencies"])
        username = payload["sub"]
        data = (
            kwargs["session"]
            .query(models.TokenTable)
            .filter_by(
                username=username, access_token=kwargs["dependencies"], status=True
            )
            .first()
        )
        if data:
            return await func(*args, **kwargs)

        else:
            return {"msg": "Token blocked"}

    return wrapper


@app.post("/register-user", tags=["Authentication"])
async def register_user(
    user: schemas.UserCreate, session: Session = Depends(get_session)
):
    existing_user: models.User | None = (
        session.query(models.User).filter_by(username=user.username).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = models.User(
        username=user.username,
        name=user.name,
        email=user.email,
        password=utils.get_hashed_password(user.password),
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": f"User {new_user.username} created successfully"}


@app.post("/register-station", tags=["Authentication"])
@token_required
async def register_station(
    station: schemas.StationCreate,
    session: Session = Depends(get_session),
    dependencies=Depends(auth_bearer.JWTBearer()),
):
    existing_station: models.RpiStation | None = (
        session.query(models.RpiStation)
        .filter_by(stationname=station.stationname)
        .first()
    )
    if existing_station:
        raise HTTPException(status_code=400, detail="Station name already registered")

    new_station = models.RpiStation(
        stationname=station.stationname,
        password=utils.get_hashed_password(station.password),
        battery=station.battery,
    )

    session.add(new_station)
    session.commit()
    session.refresh(new_station)

    return {"message": f"Station {new_station.stationname} created successfully"}


@app.post("/login-user", response_model=schemas.TokenSchema, tags=["Authentication"])
async def login_user(
    request: schemas.RequestDetails, session: Session = Depends(get_session)
) -> Dict:
    user: models.User = (
        session.query(models.User)
        .filter(models.User.username == request.username)
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username"
        )
    hashed_password = user.password
    if not utils.verify_password(request.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    access_token = utils.create_access_token(user.username)

    token_db = models.TokenTable(
        username=user.username, access_token=access_token, status=True
    )

    session.add(token_db)
    session.commit()
    session.refresh(token_db)

    return {"access_token": access_token}


@app.post("/login-station", response_model=schemas.TokenSchema, tags=["Authentication"])
async def login_station(
    request: schemas.RequestDetails,
    session: Session = Depends(get_session),
) -> Dict:
    station: models.RpiStation = (
        session.query(models.RpiStation)
        .filter(models.RpiStation.stationname == request.username)
        .first()
    )
    if station is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect stationname"
        )
    hashed_password = station.password
    if not utils.verify_password(request.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    access_token = utils.create_access_token(station.stationname)

    token_db = models.TokenTable(
        username=station.stationname, access_token=access_token, status=True
    )

    session.add(token_db)
    session.commit()
    session.refresh(token_db)

    return {"access_token": access_token}


@app.get("/user_details", response_model=schemas.UserDetails, tags=["Details"])
@token_required
async def user_details(
    session: Session = Depends(get_session),
    dependencies=Depends(auth_bearer.JWTBearer()),
):
    username: str | None = (
        session.query(models.TokenTable)
        .filter(models.TokenTable.access_token == dependencies)
        .first()
    ).username

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exist"
        )

    user: models.User = (
        session.query(models.User).filter(models.User.username == username).first()
    )
    return {"name": user.name, "email": user.email}


# login required for all below

# getting user details without password

# getting station details without password
# internal function that will ask the station for drone battery percent. (write to db)

# write update to database -- bin table

# write get call to get bin table


#
