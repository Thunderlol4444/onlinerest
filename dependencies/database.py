import mysql.connector


def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="Thunder",
        password="020708",
        database="mydatabase"
    )


def create_table():
    connection = get_database_connection()
    cursor = connection.cursor()
    query = ("CREATE DATABASE IF NOT EXISTS mydatabase ;\
             USE mydatabase;\
             CREATE TABLE IF NOT EXISTS users2 (\
                id INT AUTO_INCREMENT PRIMARY KEY,\
                username VARCHAR(50) NOT NULL,\
                email VARCHAR(100) NOT NULL,\
                password VARCHAR(100) NOT NULL\
                );\
             CREATE TABLE IF NOT EXISTS TokenTable(\
                user_id INT,\
                access_toke VARCHAR(450) PRIMARY KEY,\
                refresh_toke VARCHAR(450) NOT NULL,\
                status BOOLEAN,\
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP\
                )\
             "
             )
    cursor.execute(query, multi=True)
    cursor.close()
    connection.close()
    return {'message': 'Table created'}


def create_data_table():
    connection = get_database_connection()
    cursor = connection.cursor()
    """    query = ("CREATE DATABASE IF NOT EXISTS mydatabase ;\
                     USE mydatabase;\
                     CREATE TABLE IF NOT EXISTS aistable (\
                        id INT AUTO_INCREMENT PRIMARY KEY,\
                        VESSEL_HASH VARCHAR(50) NOT NULL,\
                        speed FLOAT(15, 4) NOT NULL,\
                        LON INT(10) NOT NULL,\
                        LAT INT(10) NOT NULL,\
                        COURSE INT(10) NOT NULL,\
                        HEADING INT(10) NOT NULL,\
                        TIMESTAMP VARCHAR(50) NOT NULL,\
                        departurePortName VARCHAR(50) NOT NULL\
                        );\
                     "
             )"""
    query = ("CREATE TABLE IF NOT EXISTS aistable2 (\
                id INT AUTO_INCREMENT PRIMARY KEY,\
                CONTACT_NUMBER VARCHAR(50) NOT NULL,\
                BASEDATETIME DATETIME NOT NULL ,\
                LAT FLOAT(10) NOT NULL,\
                LON FLOAT(10) NOT NULL,\
                SOG FLOAT(10) NOT NULL,\
                COG FLOAT(10) NOT NULL,\
                HEADING INT(10) NOT NULL,\
                VESSELNAME VARCHAR(50) NOT NULL,\
                IMO VARCHAR(50),\
                CALLSIGN VARCHAR(50),\
                VESSELTYPE INT(5),\
                STATUS INT(5) DEFAULT 15,\
                LENGTH INT(10),\
                WIDTH INT(10),\
                DRAFT FLOAT(10),\
                CARGO INT(10),\
                TRANSCEIVERCLASS VARCHAR(5)\
                );\
            ")
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
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
