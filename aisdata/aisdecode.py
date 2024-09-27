data = []

with open(r'type 1.txt', 'r') as file:
    rows = file.readlines()
    for row in rows:
        x = row.strip('\n').split(',')
        data.append({"packet": x[0], "count_of_fragments": x[1], "fragment_number": x[2], "sequential_message_ID": x[3],
                     "radio_channel_code": x[4], "payload": x[5], "fill_bits": x[6][0], "checksum": x[6][1:]})


def dearmoring(payload):
    naked = list()
    for y in payload:
        number = ord(y)
        if number - 48 > 40:
            number -= 56
            naked.append(number)
        else:
            number -= 48
            naked.append(number)
    binary = list()
    for num in naked:
        binary.append(decimal_to_binary(num))
    return binary


def decimal_to_binary(num: int):
    bits = []
    while num > 1:
        if num % 2 == 0:
            bits.insert(0, int(num % 2))
            num /= 2
        else:
            bits.insert(0, (int(num % 2)))
            num = (num-1)/2
    bits.insert(0, int(num))

    while len(bits) < 6:
        bits.insert(0, 0)
    return ''.join(map(str, bits))


def decode_table(bits):
    decode_dict = ({"000000": "@", "000001": "A", "000010": "B", "000011": "C", "000100": "D", "000101": "E",
                    "000110": "F", "000111": "G", "001000": "H", "001001": "I", "001010": "J", "001011": "K",
                    "001100": "L", "001101": "M", "001110": "N", "001111": "O", "010000": "P", "010001": "Q",
                    "010010": "R", "010011": "S", "010100": "T", "010101": "U", "010110": "V", "010111": "W",
                    "011000": "X", "011001": "Y", "011010": "Z", "011011": "[", "011100": "\\", "011101": "]",
                    "011110": "^", "011111": "_", "100000": " ", "100001": "!", "100010": '"', "100011": "#",
                    "100100": "$", "100101": "%", "100110": "&", "100111": "'", "101000": "(", "101001": ")",
                    "101010": "*", "101011": "+", "101100": ",", "101101": "-", "101110": ".", "101111": "/",
                    "110000": "0", "110001": "1", "110010": "2", "110011": "3", "110100": "4", "110101": "5",
                    "110110": "6", "110111": "7", "111000": "8", "111001": "9", "111010": ":", "111011": ";",
                    "111100": "<", "111101": "=", "111110": ">", "111111": "?"
                    })

    binary_dict = ({"000000": 0, "000001": 1, "000010": 2, "000011": 3, "000100": 4, "000101": 5, "000110": 6,
                    "000111": 7, "001000": 8, "001001": 9, "001010": 10, "001011": 11, "001100": 12, "001101": 13,
                    "001110": 14, "001111": 15, "010000": 16, "010001": 17, "010010": 18, "010011": 19, "010100": 20,
                    "010101": 21, "010110": 22, "010111": 23, "011000": 24, "011001": 25, "011010": 26, "011011": 27,
                    "011100": 28, "011101": 29, "011110": 30, "011111": 31, "100000": 32, "100001": 33, "100010": 34,
                    "100011": 35, "100100": 36, "100101": 37, "100110": 38, "100111": 39, "101000": 40, "101001": 41,
                    "101010": 42, "101011": 43, "101100": 44, "101101": 45, "101110": 46, "101111": 47, "110000": 48,
                    "110001": 49, "110010": 50, "110011": 51, "110100": 52, "110101": 53, "110110": 54, "110111": 55,
                    "111000": 56, "111001": 57, "111010": 58, "111011": 59, "111100": 60, "111101": 61, "111110": 62,
                    "111111": 63
                    })

    return decode_dict[bits], binary_dict[bits]


def inner_process(value):
    signed = 1
    if not str(value)[0].isdigit():
        signed = -1
        value = int(str(value)[1:])
    return signed, value


def binary_to_char(binary):
    msg = list()
    for i in range(0, len(binary), 6):
        char = decode_table(binary[i:i + 6])[0]
        if char == '@':
            continue
        msg.append(char)
    msg = ''.join(msg)
    return msg


def segment_process_type_a(segments):
    sign1, segment1 = inner_process(segments['Rate of Turn'])
    segments['Rate of Turn'] = (segment1 / 4.733) ** 2 * sign1
    sign2, segment2 = inner_process(segments['Longitude'])
    segments['Longitude'] = segment2 / 600000 * sign2
    sign3, segment3 = inner_process(segments['Latitude'])
    segments['Latitude'] = segment3/600000 * sign3
    return segments


def segment_process_type_5(segments):
    segments['Draught'] = segments['Draught'] / 10
    return segments


def segment_process_type_18(segments):
    sign1, segment1 = inner_process(segments['Longitude'])
    segments['Longitude'] = segment1 / 600000 * sign1
    sign2, segment2 = inner_process(segments['Latitude'])
    segments['Latitude'] = segment2/600000 * sign2
    segments['Course Over Ground'] = segments['Course Over Ground'] / 10
    return segments


def ais_type_a(raw_data):
    decoded = list()

    for index in range(len(raw_data)):
        raw = dearmoring(raw_data[index]['payload'])
        raw = ''.join(raw)
        raw_segments = ({"Message Type": raw[:6], "Repeat Indicator": raw[6:8], "MMSI": raw[8:38],
                         "Navigation Status": raw[38:42], "Rate of Turn": raw[42:50], "Speed Over Ground": raw[50:60],
                         "Position Accuracy": raw[60], "Longitude": raw[61:89], "Latitude": raw[89:116],
                         "Course Over Ground": raw[116:128], "True Heading": raw[128:137], "Time Stamp": raw[137:143],
                         "Manoeuver Indicator": raw[143:145], "Spare": raw[145:148], "RAIM Flag": raw[148],
                         "Radio Status": raw[149:]})
        decimal_segments = ({})
        for segment in raw_segments:
            segmented = raw_segments[segment]
            if segment == 'Message Type':
                decimal_segments[segment] = decode_table(str(segmented))[1]
            else:
                sign = 1
                if segment == 'Rate of Turn' or segment == 'Longitude' or segment == 'Latitude':
                    segmented = raw_segments[segment][1:]
                    if raw_segments[segment][0] == '1':
                        sign = -1
                sums = 0
                y = 0
                for i in range(0, len(segmented)):
                    sums += int(segmented[-i-1]) * 2 ** y
                    y += 1
                if segment == 'Rate of Turn' and sums == 0:
                    sums = 128
                decimal_segments[segment] = sums*sign
        decoded.append(segment_process_type_a(decimal_segments))
    return decoded


def ais_type_5(raw_data):
    decoded = list()
    for index in range(len(raw_data)):
        raw = dearmoring(raw_data[index]['payload'])
        raw = ''.join(raw)
        raw_segments = ({"Message Type": raw[:6], "Repeat Indicator": raw[6:8], "MMSI": raw[8:38],
                         "AIS Version": raw[38:40], "IMO Number": raw[40:70], "Call Sign": raw[70:112],
                         "Vessel Name": raw[112:232], "Ship type": raw[232:240], "Dimension to Bow": raw[240:249],
                         "Dimension to Stern": raw[249:258], "Dimension to Port": raw[258:264],
                         "Dimension to Starboard": raw[264:270], "Position Fix Type": raw[270:274],
                         "ETA month": raw[274:278], "ETA day": raw[278:282], "ETA hour": raw[282:288],
                         "ETA minute": raw[288:294], "Draught": raw[294:302], "Destination": raw[302:422],
                         "DTE": raw[422], "Spare": raw[423]})
        decimal_segments = ({})
        for segment in raw_segments:
            segmented = raw_segments[segment]
            if segment == 'Message Type':
                decimal_segments[segment] = decode_table(str(segmented))[1]
            elif segment == 'Call Sign' or segment == 'Vessel Name' or segment == 'Destination':
                decimal_segments[segment] = binary_to_char(segmented)
            else:
                sums = 0
                y = 0
                for i in range(0, len(segmented)):
                    sums += int(segmented[-i - 1]) * 2 ** y
                    y += 1
                decimal_segments[segment] = sums
        decoded.append(segment_process_type_5(decimal_segments))
    return decoded


def ais_type_18(raw_data):
    decoded = list()
    for index in range(len(raw_data)):
        raw = dearmoring(raw_data[index]['payload'])
        raw = ''.join(raw)
        raw_segments = ({"Message Type": raw[:6], "Repeat Indicator": raw[6:8], "MMSI": raw[8:38],
                         "Regional Reserved": raw[38:46], "Speed Over Ground": raw[46:56], "Position Accuracy": raw[56],
                         "Longitude": raw[57:85], "Latitude": raw[85:112], "Course Over Ground": raw[112:124],
                         "True Heading": raw[124:133], "Time Stamp": raw[133:139], "Regional Reserved 2": raw[139:141],
                         "CD Unit": raw[141], "Display flag": raw[142], "DSC Flag": raw[143], "Band Flag": raw[144],
                         "Message 22 Flag": raw[145], "Assigned": raw[146], "RAIM Flag": raw[147],
                         "Radio Status": raw[148:]})
        decimal_segments = ({})
        for segment in raw_segments:
            segmented = raw_segments[segment]
            if segment == 'Message Type':
                decimal_segments[segment] = decode_table(str(segmented))[1]
            else:
                sign = 1
                if segment == 'Longitude' or segment == 'Latitude':
                    segmented = raw_segments[segment][1:]
                    if raw_segments[segment][0] == '1':
                        sign = -1
                sums = 0
                y = 0
                for i in range(0, len(segmented)):
                    sums += int(segmented[-i - 1]) * 2 ** y
                    y += 1
                decimal_segments[segment] = sums * sign
        decoded.append(segment_process_type_18(decimal_segments))
    return decoded


def ais_type_24(raw_data):
    decoded = list()
    for index in range(len(raw_data)):
        raw = dearmoring(raw_data[index]['payload'])
        raw = ''.join(raw)
        raw_segments = ({"Message Type": raw[:6], "Repeat Indicator": raw[6:8], "MMSI": raw[8:38],
                         "Part Number": raw[38:40], "Vessel Name": None, "Spare": None, "Ship type": None,
                         "Vendor ID": None, "Unit Model Code": None, "Serial Number": None, "Call Sign": None,
                         "Dimension to Bow": None, "Dimension to Stern": None, "Dimension to Port": None,
                         "Dimension to Starboard": None, "Mothership MMSI": None})
        if raw_segments["Part Number"] == '00':
            raw_segments.update({"Vessel Name": raw[40:160], "Spare": raw[160:168]})
        else:
            raw_segments.update({"Ship type": raw[40:48], "Vendor ID": raw[48:66], "Unit Model Code": raw[66:70],
                                 "Serial Number": raw[70:90], "Call Sign": raw[90:132],
                                 "Dimension to Bow": raw[132:141], "Dimension to Stern": raw[141:150],
                                 "Dimension to Port": raw[150:156], "Dimension to Starboard": raw[156:163],
                                 "Mothership MMSI": raw[132:162], "Spare": raw[162:]})
        decimal_segments = ({})
        for segment in raw_segments:
            segmented = raw_segments[segment]
            print(segmented)
            if segmented is None:
                decimal_segments[segment] = segmented
                continue
            elif segment == 'Message Type':
                decimal_segments[segment] = decode_table(str(segmented))[1]
            elif segment == 'Call Sign' or segment == 'Vessel Name' or segment == 'Vendor ID':
                decimal_segments[segment] = binary_to_char(segmented)
            else:
                sums = 0
                y = 0
                for i in range(0, len(segmented)):
                    sums += int(segmented[-i - 1]) * 2 ** y
                    y += 1
                decimal_segments[segment] = sums
        decoded.append(decimal_segments)
    return decoded


def type_determining(raw_data):
    code = dearmoring(raw_data[0]['payload'])
    code = code[0]
    data_type = int(decode_table(code)[1])
    return data_type


with open('decoded_data.csv', 'w') as file:
    match type_determining(data):
        case _ if type_determining(data) <= 3:
            decoded_data = ais_type_a(data)
        case 5:
            decoded_data = ais_type_5(data)
        case 18:
            decoded_data = ais_type_18(data)
        case 24:
            decoded_data = ais_type_24(data)
    file.write(','.join(decoded_data[0].keys()))
    file.write('\n')
    for row in decoded_data:
        file.write(','.join([str(x) for x in row.values()]))
        file.write('\n')
