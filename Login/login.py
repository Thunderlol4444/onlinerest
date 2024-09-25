import random
from functools import wraps
from fastapi import Depends, HTTPException, status,  Response, APIRouter, Request
from dependencies.database import get_database_connection
from . import models
from .utils import *
from .auth_bearer import JWTBearer
from time import time
import os
import signal
from .emailXauth import send_email
from dependencies.limiting_algorithms import RateLimitExceeded
from dependencies.rate_limiter import RateLimitFactory
router: APIRouter = APIRouter()
ip_addresses = {}


def limited(request):
    client = request
    try:
        if client not in ip_addresses:
            ip_addresses[client] = RateLimitFactory.get_instance("SlidingWindow")
        if ip_addresses[client].allow_request():
            return "This is a limited use API"
    except RateLimitExceeded as e:
        raise e
    

def token_required(func):
    @wraps(func)
    async def wrapper(**kwargs):
        connection = get_database_connection()
        payload = jwt.decode(kwargs['dependencies'], JWT_SECRET_KEY, ALGORITHM)
        user_id = payload['sub']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM TokenTable WHERE user_id=%s AND access_token=%s AND status=%s",
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
    # GOOGLE_CLIENT_ID = '1022384984816-tt725bcu2u0bb3onjcmj4o0eedk1kjpn.apps.googleusercontent.com'
    # GOOGLE_CLIENT_SECRET = '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'
    # GOOGLE_REFRESH_TOKEN = \
    #     '1//0gcJzGIdMsbnXCgYIARAAGBASNwF-L9IrfDfaxU9IokrvDsb9jjMJviGcqznXDltHgfsMamC5uV90zZd0ZTbhrVadVcEbMMqhjMo'
    #
    OTP = random.randint(1000, 9999)
    # if GOOGLE_REFRESH_TOKEN is None:
    #     print('No refresh token found, obtaining one')
    #     refresh_token, access_token, expires_in = get_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    #     print('Set the following as your GOOGLE_REFRESH_TOKEN:', refresh_token)
    #     exit()
    #
    # # valid_receiver_email = email_verification(receiver_email)
    # send_mail('jasonsimsamsung+1@gmail.com', new_user.email,
    #           'Verification code',
    #           'Here is your OTP<br/>' +
    #           f'OTP: {OTP}')
    #
    # print("OTP has been sent to " + new_user.email)
    # return {"message": "Verification sent", "OTP": f"{OTP}"}
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


@router.post('/login', response_model=models.TokenSchema, )
def login(request: models.RequestDetails = Depends()):
    user = database.child("users").get({"email": "request.email"})
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user[3]
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    token = database.child("users").get({"user_id": "user[0]"})
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
                database.child("TokenTable").child({"user_id": user[0]}).update({"access_token": access, "status": 1})
                da
                cursor.execute("DELETE FROM TokenTable WHERE status=%s AND user_id=%s", (0, user[0]))
                connection.commit()
                return {
                    "access_token": access,
                    "refresh_token": refresh,
                }
    access = create_access_token(user[0])
    refresh = create_refresh_token(user[0])
    values = (user[0], access, refresh, True)
    query = "INSERT INTO TokenTable (user_id, access_token, refresh_token, status) VALUES (%s, %s, %s, %s)"
    cursor.execute("DELETE FROM TokenTable WHERE status=%s AND user_id=%s", (0, user[0]))
    cursor.execute(query, values)
    connection.commit()
    return {
        "access_token": access,
        "refresh_token": refresh,
    }


@router.get('/getusers')
@token_required
def get_users(request: Request, dependencies=Depends(JWTBearer()), tags=["Admin"]):
    limited(request)
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users2")
    users = cursor.fetchall()
    return users


@router.patch('/change-password')
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
    cursor.execute("SELECT * FROM TokenTable WHERE user_id=%s AND access_token=%s", (user_id, token))
    existing_token = cursor.fetchone()
    if existing_token:
        cursor.execute("UPDATE TokenTable SET status=%s WHERE user_id=%s", (0, user_id))
        connection.commit()
    connection.close()
    return {"message": "Logout Successfully"}
