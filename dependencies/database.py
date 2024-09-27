import datetime

import firebase_admin
from firebase_admin import db
import json
import os

firebaseConfig = {
    "apiKey": "AIzaSyC6XVvfqE8zEqT_kxNjaS478N1wkLQuyZk",
    "authDomain": "refined-density-297301.firebaseapp.com",
    "projectId": "refined-density-297301",
    "storageBucket": "refined-density-297301.appspot.com",
    "messagingSenderId": "1022384984816",
    "appId": "1:1022384984816:web:d2d4a6feefeb889c202835",
    "measurementId": "G-9GXBS8ZVCK",
    "databaseURL": "https://refined-density-297301-default-rtdb.asia-southeast1.firebasedatabase.app",
    # "serviceAccount": r"C:\Users\Thunder\Desktop\angkasax\github\localrest\admincreds.json"
}

cwd = os.getcwd()
os.path.join(cwd,)


def get_database_connection():
    try:
        cre_obj = firebase_admin.credentials.Certificate("/onlinerest/admincreds.json")
    except FileNotFoundError:
        cre_obj = firebase_admin.credentials.Certificate(r"C:\Users\Thunder\Desktop\angkasax\github\onlinerest\admincreds.json")
    firebase = firebase_admin.initialize_app(cre_obj, {"databaseURL": firebaseConfig["databaseURL"]})
    return


def create_table():
    get_database_connection()
    directory = db.reference("")
    # ref = parent_ref.child("tokentable")
    # user_data = directory.child("TokenTable").order_by_child("user_id").equal_to(1).get()
    user_list = directory.child("Users").order_by_child("email").equal_to("jason").get()
    email = None
    password = None
    user_id = None
    for key, value in dict(user_list).items():
        email = value["email"]
        password = value["password"]
        user_id = value["user_id"]
    print(user_list)
    print(email)
    # data_list = directory.child("Books").order_by_child("Price").get()
    # data = [value for key, value in dict(data_list).items()]
    # print(data)
    return {'message': 'Table created'}


def insert_data(data):
    directory = db.reference("/AisData")
    with open('AisDataA.json', 'r') as f:
        file_contents = json.load(f)
    directory.push().set(file_contents)
    return {'message': 'Data inserted'}


def insert_data_type_a():
    get_database_connection()
    directory = db.reference("/AisDataA")
    with open(r'.\aisdata.json', 'r') as f:
        file_contents = json.load(f)
    directory.set(file_contents)
    return {'message': 'Data inserted'}


def check_zero(data_point):
    if data_point == '':
        return
    else:
        return data_point


def check_status(status):
    if status == '':
        return 15
    else:
        return status


def check_cargo(cargo):
    if cargo == '':
        return
    else:
        return cargo


def check_type(vesseltype):
    if vesseltype == '':
        return
    else:
        return vesseltype
