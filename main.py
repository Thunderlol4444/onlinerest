from Login import login
from aisdata import getdata
from fastapi import FastAPI
from dependencies.database import create_table
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    print("Connection established")
    yield
    print("Connection closed")
app = FastAPI(lifespan=lifespan)
app.include_router(login.router)
app.include_router(getdata.router)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
