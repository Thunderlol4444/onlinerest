from Login import login
from aisdata import getdata
from fastapi import FastAPI
from dependencies.database import create_table
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
firebaseConfig = {
  "apiKey": "AIzaSyC6XVvfqE8zEqT_kxNjaS478N1wkLQuyZk",
  "authDomain": "refined-density-297301.firebaseapp.com",
  "projectId": "refined-density-297301",
  "storageBucket": "refined-density-297301.appspot.com",
  "messagingSenderId": "1022384984816",
  "appId": "1:1022384984816:web:d2d4a6feefeb889c202835",
  "measurementId": "G-9GXBS8ZVCK"
}

# firebase = pyrebase.initialize_app(firebaseConfig)
# storage = firebase.storage()
# database = firebase.database()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    print("Connection established")
    yield
    print("Connection closed")
app = FastAPI(lifespan=lifespan)
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")
app.include_router(login.router)
app.include_router(getdata.router)

origins = [
    "http://localhost:3000",
    "localhost:3000"
    "https://refined-density-297301.web.app"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get('PORT', 8080)), log_level="info")