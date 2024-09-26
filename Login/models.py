from pydantic import BaseModel
import datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class RequestDetails(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class ChangePassword(BaseModel):
    email: str
    # old_password: str
    new_password: str


class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime.datetime


class EmailVerification(BaseModel):
    email: str
    name: str


class UserToken(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
    status: int
    created_date: datetime.datetime


class UserData(BaseModel):
    id: int
    username: str
    email: str
    password: str


class AisTypeA(BaseModel):
    id: int
    MessageType: str
    RepeatIndicator: int
    MMSI: int
    NavigationalStatus: int
    RateOfTurn: float
    SOG: int
    PositionAccuracy: int
    Longitude: float
    Latitude: float
    COG: float
    TrueHeading: float
    TimeStamp: int
    ManoeuverIndicator: int
    Spare: int
    RAIMFlag: int
    RadioStatus: int
