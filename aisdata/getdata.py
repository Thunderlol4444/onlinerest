from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
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
    return (JSONResponse(
        status_code=200,
        content={data},
        headers={
            "Access-Control-Allow-Origin": "https://refined-density-297301.web.app",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }))


@router.get("/ais_data_A")
@token_required
def ais_data_a(dependencies=Depends(JWTBearer())):
    directory = db.reference("/AISDataA")
    data_list = directory.order_by_child("id").get()
    data = [value for key, value in dict(data_list).items()]
    print(data)
    return (JSONResponse(
        status_code=200,
        content={data},
        headers={
            "Access-Control-Allow-Origin": "https://refined-density-297301.web.app",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }))
