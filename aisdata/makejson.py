import csv
import json


def make_json(csvFilePath, jsonFilePath):
    # create a dictionary
    data = []

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        label = list(csvReader.fieldnames)
        next(csvf)
        csvReader = csv.reader(csvf)
        data_dict = {}
        stop = 0
        for row in csvReader:
            if stop == 1000:
                break
            stop += 1
            for i in range(len(row)):
                data_dict[label[i]] = row[i]
            data.append(data_dict)
            print(data_dict)
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


# Driver Code

# Decide the two file paths according to your
# computer system
csvFilePath = r'C:\Users\Thunder\Desktop\angkasax\AIS_2023_01_01\AIS_2023_01_01.csv'
jsonFilePath = r'data.json'

# Call the make_json function
make_json(csvFilePath, jsonFilePath)
