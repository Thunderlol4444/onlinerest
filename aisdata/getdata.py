from fastapi import FastAPI, Depends, HTTPException, APIRouter
from dependencies.database import get_database_connection
from Login.login import token_required
from Login.auth_bearer import JWTBearer
from firebase_admin import db

router: APIRouter = APIRouter()


@router.get("/ais_data")
@token_required
def ais_data(dependencies=Depends(JWTBearer())):
    directory = db.reference("/ais_data")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM aistable2 WHERE id<=1000")
    data = cursor.fetchall()
    print(data)
    cursor.close()
    connection.close()
    return data


@router.get("/ais_data_A")
@token_required
def ais_data_a(dependencies=Depends(JWTBearer())):
    directory = db.reference("/AISDataA")
    data_list = directory.order_by_child("id").get()
    data = [value for key, value in dict(data_list).items()]
    print(data)
    return data
