import random
import os
import signal
import datetime as date
from functools import wraps
from fastapi import Depends, HTTPException, status,  Response, APIRouter, Request
from . import models
from .utils import *
from .auth_bearer import JWTBearer
from time import time
from firebase_admin import db
from .emailXauth import send_email
from dependencies.limiting_algorithms import RateLimitExceeded
from dependencies.rate_limiter import RateLimitFactory
from fastapi.responses import JSONResponse

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
        directory = db.reference("")
        payload = jwt.decode(kwargs['dependencies'], JWT_SECRET_KEY, ALGORITHM)
        user_id = payload['sub']
        user_data = directory.child("TokenTable").order_by_child("user_id").equal_to(user_id).get()
        access_token_list = [value["access_token"] for key, value in dict(user_data).items()]
        if access_token_list[0] == kwargs['dependencies']:
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
    directory = db.reference("/Users")
    user_data = directory.order_by_child("email").equal_to(user.email).get()
    email = None
    for key, value in dict(user_data).items():
        email = value["email"]
    if email is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    encrypted_password = get_hashed_password(user.password)
    user_list = directory.order_by_child("user_id").get()
    user_id = 1
    for key, value in dict(user_list).items():
        if user_id != value["user_id"]:
            break
        user_id += 1
    directory.child("user"+str(user_id)).set({"user_id": user_id, "username": user.username, "email": user.email,
                          "password": encrypted_password})
    return (JSONResponse(
            status_code=200,
            content={"message": "user created successfully", "user": {"email": email}},
            headers={
                "Access-Control-Allow-Origin": "https://refined-density-297301.web.app",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
            }))


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
    return (JSONResponse(
            status_code=200,
            content={"message": "Verification sent", "OTP": f"{OTP}"}))


@router.post('/login', response_model=models.TokenSchema, )
def login(request: models.RequestDetails = Depends()):
    directory = db.reference("")
    user_list = directory.child("Users").order_by_child("email").equal_to(request.email).get()
    email = None
    password = None
    user_id = None
    userkey = None
    for key, value in dict(user_list).items():
        userkey = key
        email = value["email"]
        password = value["password"]
        user_id = value["user_id"]
    if email is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password")
    token_list = directory.child("TokenTable").order_by_child("user_id").equal_to(user_id).get()
    access = None
    refresh = None
    logged_in = None
    token_name = None
    for key, value in dict(token_list).items():
        token_name = key
        access = value["access_token"]
        refresh = value["refresh_token"]
        logged_in = value["status"]
        print("access: ", access)
        print(dict(value))

    if access:
        if logged_in == 1:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user already signed in")
        else:
            refresh_token2 = refresh_token(refresh)
            print(refresh_token2)
            if time() - float(refresh_token2["exp"]) < REFRESH_TOKEN_EXPIRE_MINUTES:
                access = create_access_token(user_id)
                print(access)
                directory.child("TokenTable").child(token_name).update({"access_token": access, "status": 1})
                return (JSONResponse(
                        status_code=200,
                        content={"access_token": access, "refresh_token": refresh}))
            else:
                access = create_access_token(user_id)
                refresh = create_refresh_token(user_id)
                directory.child("TokenTable").child(token_name).update({"access_token": access,
                                                                        "refresh_token": refresh, "status": 1})
                return (JSONResponse(
                    status_code=200,
                    content={"access_token": access, "refresh_token": refresh,
                             "message": "New refresh token generated"}))
    access = create_access_token(user_id)
    refresh = create_refresh_token(user_id)
    now = date.datetime.now()
    directory.child("TokenTable").child(userkey).set({"user_id": user_id, "access_token": access,
                                                      "refresh_token": refresh, "status": 1, "created_date": str(now)})
    return (JSONResponse(
        status_code=200,
        content={"access_token": access, "refresh_token": refresh}))


@router.get('/getusers')
@token_required
def get_users(request: Request, dependencies=Depends(JWTBearer()), tags=["Admin"]):
    limited(request)
    directory = db.reference("/Users")
    user_list = directory.order_by_child("user_id").get()
    users = []
    for key, value in dict(user_list).items():
        user = []
        for itemKey, itemValue in value:
            user.append(itemValue)
        users.append(user)
    return (JSONResponse(
            status_code=200,
            content={users},
            headers={
                "Access-Control-Allow-Origin": "https://refined-density-297301.web.app",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
            }))


@router.patch('/change-password')
def change_password(request: models.ChangePassword = Depends()):
    directory = db.reference("/Users")
    user = directory.order_by_child("email").equal_to(request.email).get()
    userkey = None
    for key, value in dict(user).items():
        userkey = key
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    encrypted_password = get_hashed_password(request.new_password)
    directory.child(userkey).update({"password": encrypted_password})
    return (JSONResponse(
        status_code=200,
        content={"message": "Password changed successfully"}))


@router.post('/logout')
def logout(dependencies=Depends(JWTBearer())):
    directory = db.reference("/TokenTable")
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload['sub']
    token_record = directory.get()
    info = []
    for key, record in dict(token_record).items():
        print("record", record)
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        if (datetime.utcnow() - datetime.strptime(record["created_date"], date_format)).days > 1:
            info.append(key)
    print(tuple(info))
    if info:
        for i in range(len(info)):
            directory.child(info[i]).set("")
    existing_token = directory.order_by_child("user_id").equal_to(int(user_id)).get()
    if existing_token:
        for key, value in dict(existing_token).items():
            directory.child(key).update({"status": 0})
    return (JSONResponse(
        status_code=200,
        content={"message": "Logout Successfully"}))
