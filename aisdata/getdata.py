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
    data_list = directory.order_by_child("id").get()
    data = [value for key, value in dict(data_list).items()]
    print(data)
    return (JSONResponse(
        status_code=200,
        content={data}))


@router.get("/ais_data_A")
@token_required
def ais_data_a(dependencies=Depends(JWTBearer())):
    directory = db.reference("/AISDataA")
    data_list = directory.order_by_child("id").get()
    data = [value for key, value in dict(data_list).items()]
    print(data)
    return (JSONResponse(
        status_code=200,
        content={data}))
