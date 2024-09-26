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
        cre_obj = firebase_admin.credentials.Certificate(r".\admincreds.json")
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
    return {'message': 'Table created'}


def insert_data(data):
    connection = get_database_connection()
    cursor = connection.cursor()
    """query2 = ("INSERT INTO aistable (VESSEL_HASH, speed, LON, LAT, COURSE, HEADING, TIMESTAMP, departurePortName)\
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    for i in range(0, len(data)):
        values = (data[i]['VESSEL_HASH'], data[i]['speed'], data[i]['LON'], data[i]['LAT'],
                  data[i]['COURSE'], data[i]['HEADING'], data[i]['TIMESTAMP'], data[i]['DEPARTURE'])
        cursor.execute(query2, values)
        connection.commit()"""

    query2 = ("INSERT INTO aistable2 (CONTACT_NUMBER, BASEDATETIME, LAT, LON, SOG, COG, HEADING, VESSELNAME, IMO,\
               CALLSIGN, VESSELTYPE, STATUS, LENGTH, WIDTH, DRAFT, CARGO, TRANSCEIVERCLASS)\
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    for row in data:
        values = (row['MMSI'], row['BaseDateTime'], row['LAT'], row['LON'], row['SOG'], row['COG'], row['Heading'],
                  row['VesselName'], row['IMO'], row['CallSign'], check_cargo(row['VesselType']),
                  check_status(row['Status']), check_zero(row['Length']), check_zero(row['Width']),
                  check_zero(row['Draft']), check_cargo(row['Cargo']), row['TransceiverClass'])
        cursor.execute(query2, values)
        connection.commit()

    cursor.close()
    connection.close()
    return {'message': 'Data inserted'}


def create_type_a_table():
    connection = get_database_connection()
    cursor = connection.cursor()
    query = ("CREATE TABLE IF NOT EXISTS ais_type_a (\
                id INT AUTO_INCREMENT PRIMARY KEY,\
                MESSAGETYPE VARCHAR(5) NOT NULL,\
                REPEATINDICATOR INT NOT NULL ,\
                MMSI INT(15) NOT NULL,\
                NAVIGATIONSTATUS INT(5) NOT NULL DEFAULT 15,\
                RATEOFTURN FLOAT(10) NOT NULL,\
                SOG FLOAT(10) NOT NULL,\
                POSITIONACCURACY INT(2),\
                LONGITUDE FLOAT(10) NOT NULL,\
                LATITUDE FLOAT(10) NOT NULL,\
                COG FLOAT(10) NOT NULL,\
                TRUEHEADING INT(10) NOT NULL,\
                TIMESTAMP INT(5) NOT NULL,\
                MANOEUVERINDICATOR INT(5),\
                SPARE INT(5),\
                RAIMFLAG INT(5),\
                RADIOSTATUS INT(10)\
                );\
            ")
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return {'message': 'Table created'}


def insert_data_type_a(data):
    connection = get_database_connection()
    cursor = connection.cursor()

    query2 = ("INSERT INTO ais_type_a (MESSAGETYPE, REPEATINDICATOR, MMSI, NAVIGATIONSTATUS, RATEOFTURN, SOG,\
                POSITIONACCURACY, LONGITUDE, LATITUDE, COG, TRUEHEADING, TIMESTAMP, MANOEUVERINDICATOR, SPARE,\
                RAIMFLAG, RADIOSTATUS)\
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    for row in data:
        values = (row['Message Type'], row['Repeat Indicator'], row['MMSI'], row['Navigation Status'],
                  row['Rate of Turn'], row['Speed Over Ground'], row['Position Accuracy'], row['Longitude'],
                  row['Latitude'], row['Course Over Ground'], row['True Heading'], row['Time Stamp'],
                  row['Manoeuver Indicator'], row['Spare'], row['RAIM Flag'], row['Radio Status'])
        cursor.execute(query2, values)
        connection.commit()

    cursor.close()
    connection.close()
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
