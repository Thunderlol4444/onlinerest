import csv
from database import *

data_list = list()


# with open(r'C:\Users\Thunder\Downloads\MT-AIS-DEBS2018\DEBS_DATASET_PUBLIC_second.csv') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     next(reader, None)
#     i = 0
#     for row in reader:
#         i += 1
#         if row[0] == "VESSEL_HASH" or i > 50:
#             continue
#         data_list.append({'VESSEL_HASH': row[0], 'speed': float(row[1]),
#                           'LON': float(row[2]), 'LAT': float(row[3]),
#                           'COURSE': row[4], 'HEADING': row[5],
#                          'TIMESTAMP': row[6], 'DEPARTURE': row[7]})
#
#     print(data_list)

with open(r'C:\Users\Thunder\Downloads\decoded_data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    create_type_a_table()
    insert_data_type_a(reader)
    #create_data_table()
    #insert_data(reader)
