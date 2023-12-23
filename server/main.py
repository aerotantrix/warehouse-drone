import stat
from turtle import st
from cv2 import randShuffle
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
        .filter_by(station_name=station.station_name)
        .first()
    )
    if existing_station:
        raise HTTPException(status_code=400, detail="Station name already registered")

    new_station = models.RpiStation(
        station_name=station.station_name,
        password=utils.get_hashed_password(station.password),
        battery=station.battery,
    )

    session.add(new_station)
    session.commit()
    session.refresh(new_station)

    return {"message": f"Station {new_station.station_name} created successfully"}


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
        .filter(models.RpiStation.station_name == request.username)
        .first()
    )
    if station is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect station_name"
        )
    hashed_password = station.password
    if not utils.verify_password(request.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    access_token = utils.create_access_token(station.station_name)

    token_db = models.TokenTable(
        username=station.station_name, access_token=access_token, status=True
    )

    session.add(token_db)
    session.commit()
    session.refresh(token_db)

    return {"access_token": access_token}


@app.get("/user_details/{username}", response_model=schemas.UserDetails, tags=["Details"])
@token_required
async def user_details(
    username: str,
    session: Session = Depends(get_session),
    dependencies=Depends(auth_bearer.JWTBearer()),
):
    user: models.User = (
        session.query(models.User).filter(models.User.username == username).first()
    )
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username")
    return {"name": user.name, "email": user.email}


# login required for all below

# getting user details without password

# getting station details without password
# internal function that will ask the station for drone battery percent. (write to db)

# write update to database -- bin table

# write get call to get bin table


@app.get("/station/{station_name}", tags=["Details"])
@token_required
async def get_battery(
    station_name: str,
    session: Session = Depends(get_session),
    dependencies=Depends(auth_bearer.JWTBearer()),
    ) -> Dict:
    station: models.RpiStation = (
        session.query(models.RpiStation)
        .filter(models.RpiStation.station_name == station_name)
        .first()
    )
    if station is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect Station')
    return {"battery": station.battery }


@app.get("/bin/{station_name}")
@token_required
async def get_bin_details(
    station_name: str,
    session: Session = Depends(get_session),
    dependencies=Depends(auth_bearer.JWTBearer())
    ):
    try:
        db = Session()
        bin_details = (
            db.query(models.Bin)
            .filter(models.Bin.station_name == station_name)
            .first()
        )
        db.close()

        if bin_details is None:
            raise HTTPException(status_code=404, detail="bin details not found")

        return {
            "timestamp": bin_details.timestamp,
            "bin_id": bin_details.bin_id,
            "row": bin_details.row,
            "col": bin_details.col,
            "rack": bin_details.rack,
            "station_name": bin_details.station_name,
        }
    except Exception:
        raise HTTPException(status_code=404, detail="bin details not found")


@app.get("/check-schedule/{station_name}")
@token_required
async def check_schedule(
    station_name: str,
    session: Session = Depends(get_session),
    dependencies=Depends(auth_bearer.JWTBearer())):
    try:
        schedule_data = (
            session.query(models.DroneSchedule)
            .filter_by(station_name=station_name)
            .order_by(models.DroneSchedule.schedule_time)
            .first()
        )
        return {schedule_data.schedule_time} if schedule_data else {}
    except Exception:
        raise HTTPException(status_code=500, detail="schedule not found")


@app.post("/dashboard-insert/")
@token_required
async def bin_data_dashboard(
    bin_id: int,
    row: str,
    rack: str,
    shelf: str,
    status: str,
    station_name: str,
    session: Session = Depends(get_session)
):
    try:
        new_bin = models.Bin(
            bin_id=bin_id,
            row=row,
            rack=rack,
            shelf=shelf,
            status=status,
            station_name=station_name
        )
        session.add(new_bin)
        session.commit()
        session.refresh(new_bin)
        return {"message": "Bin data inserted successfully"}
    except Exception:
        raise HTTPException(status_code=500, detail="error inserting into DB")


@app.post("/station-insert/")
async def bin_data_station(
    bin_id: int,
    row: str,
    rack: str,
    shelf: str,
    status: str,
    session: Session = Depends(get_session)
):
    try:
        new_bin = models.Bin(
            bin_id=bin_id,
            row=row,
            rack=rack,
            shelf=shelf,
            status=status
        )
        session.add(new_bin)
        session.commit()
        session.refresh(new_bin)
        return {"message": "Bin data inserted successfully"}
    except Exception:
        raise HTTPException(status_code=500, detail="error inserting into DB")
    

@app.post("/remove-bin/")
async def remove_bin(
    row: int,
    rack: int,
    shelf: int,
    session: Session = Depends(get_session)
):
    try:
        bin_tuple = (
            session.query(models.Bin)
            .filter_by(row=row, rack=rack, shelf=shelf)
            .first()
        )

        if bin_tuple:
            session.delete(bin_tuple)
            session.commit()
            return {"message": "Tuple removed successfully"}
        else:
            return {"message": "Tuple not found"}
    except Exception:
        raise HTTPException(status_code=500, detail=f"Error: Requested tuple not found in DB")
