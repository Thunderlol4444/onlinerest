import random
from functools import wraps
from fastapi import Depends, HTTPException, status,  Response, APIRouter
from dependencies.database import get_database_connection
from . import models
from .utils import *
from .auth_bearer import JWTBearer
from time import time
import os
import signal
# from .emailverificatiion import *
from .emailXauth import send_email

router: APIRouter = APIRouter()


def token_required(func):
    @wraps(func)
    async def wrapper(**kwargs):
        connection = get_database_connection()
        payload = jwt.decode(kwargs['dependencies'], JWT_SECRET_KEY, ALGORITHM)
        user_id = payload['sub']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM TokenTable WHERE user_id=%s AND access_toke=%s AND status=%s",
                       (user_id, kwargs['dependencies'], True))
        data = cursor.fetchone()
        if data:
            return func(kwargs['dependencies'])

        else:
            return {'msg': "Token blocked"}

    return wrapper


@router.get("/shutdown")
def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content='Server shutting down...')


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.post("/register")
def register_user(user: models.UserCreate = Depends()):
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users2 WHERE email=%s", (user.email,))
    existing_user = cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    encrypted_password = get_hashed_password(user.password)
    values = (user.username, user.email, encrypted_password)
    query = "INSERT INTO users2 (username, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "user created successfully"}


@router.post("/register/email_verification")
def register_email_verification(new_user: models.EmailVerification = Depends()):
    OTP = random.randint(1000, 9999)
    host = "smtp.gmail.com"
    port = 587
    user = "jasonsimsamsung@gmail.com"
    recipient = new_user.email
    subject = "Verify your email"
    msg = f"OTP: {OTP}"
    sender = user
    recipients = [recipient]
    send_email(host, port, subject, msg, sender, recipients)
    return {"message": "Verification sent", "OTP": f"{OTP}"}


@router.post('/login', response_model=models.TokenSchema)
def login(request: models.RequestDetails = Depends()):
    connection = get_database_connection()
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM users2 WHERE email=%s", (request.email,))
    user = cursor.fetchone()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user[3]
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    cursor.execute("SELECT * FROM TokenTable WHERE user_id=%s", (user[0],),)
    token = cursor.fetchone()
    if token:
        if token[3] == 1:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user already signed in")
        else:
            refresh_token2 = refresh_token(token[2])
            print(refresh_token2)
            if time() - float(refresh_token2["exp"]) < REFRESH_TOKEN_EXPIRE_MINUTES:
                access = create_access_token(user[0])
                print(access)
                refresh = token[2]
                cursor.execute("UPDATE TokenTable SET access_toke=%s, status=%s WHERE user_id=%s", (access, 1, user[0]))
                cursor.execute("DELETE FROM TokenTable WHERE status=%s AND user_id=%s", (0, user[0]))
                connection.commit()
                return {
                    "access_token": access,
                    "refresh_token": refresh,
                }
    access = create_access_token(user[0])
    refresh = create_refresh_token(user[0])
    values = (user[0], access, refresh, True)
    query = "INSERT INTO TokenTable (user_id, access_toke, refresh_toke, status) VALUES (%s, %s, %s, %s)"
    cursor.execute("DELETE FROM TokenTable WHERE status=%s AND user_id=%s", (0, user[0]))
    cursor.execute(query, values)
    connection.commit()
    return {
        "access_token": access,
        "refresh_token": refresh,
    }


@router.get('/getusers')
@token_required
def get_users(dependencies=Depends(JWTBearer()), tags=["Admin"]):
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users2")
    users = cursor.fetchall()
    return users


@router.post('/change-password')
def change_password(request: models.ChangePassword = Depends()):
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users2 WHERE email=%s", (request.email,))
    user = cursor.fetchone()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    # if not verify_password(request.old_password, user[3]):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    encrypted_password = get_hashed_password(request.new_password)
    cursor.execute("UPDATE users2 SET password=%s WHERE email=%s", (encrypted_password, request.email))
    connection.commit()

    return {"message": "Password changed successfully"}


@router.post('/logout')
def logout(dependencies=Depends(JWTBearer())):
    connection = get_database_connection()
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload['sub']
    print(user_id)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM TokenTable")
    token_record = cursor.fetchall()
    info = []
    for record in token_record:
        print("record", record)
        if (datetime.utcnow() - record[4]).days > 1:
            info.append(record[0])
    print(tuple(info))
    if info:
        for i in range(len(info)):
            cursor.execute("DELETE FROM TokenTable WHERE user_id=%s", (info[i],))
            connection.commit()
    cursor.execute("SELECT * FROM TokenTable WHERE user_id=%s AND access_toke=%s", (user_id, token))
    existing_token = cursor.fetchone()
    if existing_token:
        cursor.execute("UPDATE TokenTable SET status=%s WHERE user_id=%s", (0, user_id))
        connection.commit()
    connection.close()
    return {"message": "Logout Successfully"}
