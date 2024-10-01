from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from Login.login import token_required
from Login.auth_bearer import JWTBearer
from firebase_admin import db

router: APIRouter = APIRouter()


@router.get("/ais_data")
@token_required
def ais_data(dependencies=Depends(JWTBearer())):
    directory = db.reference("/AisData")
    data_list = directory.order_by_child("MMSI").get()
    data = []
    for data_point in data_list:
        data_list = []
        for key, value in dict(data_point).items():
            data_list.append(value)
        data.append(data_list)
    return data


@router.get("/ais_data_A")
@token_required
def ais_data_a(dependencies=Depends(JWTBearer())):
    directory = db.reference("/AisDataA")
    data_list = directory.order_by_child("MMSI").get()
    data = []
    for data_point in data_list:
        data_list = []
        for key, value in dict(data_point).items():
            data_list.append(value)
        data.append(data_list)
    print(data)
    return data
