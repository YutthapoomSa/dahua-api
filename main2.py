import requests
from requests.auth import HTTPDigestAuth
import re
import json

image_name = ""


class DictToObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)


def send_data_to_pocketbase(
    plate_number, color, province, vehicleSize, brand, category, image
):
    url = "http://localhost:8090/api/collections/dahua_master/records"
    headers = {"Content-Type": "application/json"}
    data = {
        "plateNumber": plate_number,
        "color": color,
        "province": province,
        "vehicleSize": vehicleSize,
        "brand": brand,
        "category": category,
        "img": image,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("Data sent successfully to Pocketbase.")
        else:
            print(
                "Failed to send data to Pocketbase. Status code:", response.status_code
            )
    except Exception as e:
        print("Error occurred while sending data to Pocketbase:", e)


def get_response_data(type, data_length, data):
    print("Type:", type)
    print("Data Length:", data_length)
    print("Data:", data)


def string_to_json(input_string):
    pairs = input_string.strip().split("\n")
    json_dict = {}

    for pair in pairs:
        key, value = pair.split("=")
        key_parts = key.split(".")
        temp = json_dict
        for part in key_parts[:-1]:
            if "[" in part:
                part_name, part_index = part.split("[")
                part_index = int(part_index[:-1])
                part_exists = False
                if part_name in temp:
                    if isinstance(temp[part_name], list):
                        if len(temp[part_name]) > part_index:
                            part_exists = True
                    else:
                        temp[part_name] = [{}]
                        part_exists = True
                if not part_exists:
                    temp[part_name] = [{}] * (part_index + 1)
                temp = temp[part_name][part_index]
            else:
                if part not in temp:
                    temp[part] = {}
                temp = temp[part]

        temp[key_parts[-1]] = value.strip()

    return json_dict


def show_data(traffic_car_data):
    # print("data", traffic_car_data)
    try:
        plate_number = traffic_car_data["TrafficCar"]["PlateNumber"]
        print(f"Plate Number: {plate_number}")
    except KeyError:
        print("Plate Number is missing.")
        plate_number = ""

    try:
        province = traffic_car_data["Object"]["Province"]
        print(f"Province: {province}")
    except KeyError:
        print("Province is missing.")
        province = ""

    try:
        category = traffic_car_data["TrafficCar"]["VehicleCategory"]
        print(f"Category: {category}")
    except KeyError:
        print("Category is missing.")
        category = ""

    try:
        color = traffic_car_data["TrafficCar"]["VehicleColor"]
        print(f"Color: {color}")
    except KeyError:
        print("Color is missing.")
        color = ""

    try:
        vehicleSize = traffic_car_data["TrafficCar"]["VehicleSize"]
        print(f"Vehicle Size: {vehicleSize}")
    except KeyError:
        print("Vehicle Size is missing.")
        vehicleSize = ""

    try:
        brand = traffic_car_data["TrafficCar"]["VehicleSign"]
        print(f"Brand: {brand}")
    except KeyError:
        print("Brand is missing.")
        brand = ""
        print(f"image: {image_name}")

    send_data_to_pocketbase(
        plate_number, color, province, vehicleSize, brand, category, image_name
    )


url = "http://10.100.62.203/cgi-bin/snapManager.cgi"
params = {
    "action": "attachFileProc",
    "channel": "1",
    "heartbeat": "5",
    "Flags[0]": "Event",
    "Events": "[TrafficJunction]",
}

auth = HTTPDigestAuth("admin", "nw@army66")

response = requests.get(url, params=params, auth=auth, stream=True)

# Processing the response
try:
    data = b""
    boundary = b"--myboundary\r\n"
    end_marker = b"\r\n\r\n\r\n"
    section_number = 1  # Initialize section number
    with open("response_data.json", "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            data += chunk
            if end_marker in data:
                sections = data.split(boundary)
                for section in sections[
                    :-1
                ]:  # Iterate over all sections except the last one
                    header_end = section.find(b"\r\n\r\n")
                    if header_end != -1:
                        # Ensure section is in bytes format
                        # section_bytes = section.encode('utf-8')

                        content_type_match = re.search(b"Content-Type: (.+)", section)
                        content_length_match = re.search(
                            b"Content-Length:\s*(\d+)", section
                        )

                        if content_type_match and content_length_match:
                            content_type = (
                                content_type_match.group(1).decode("utf-8").strip()
                            )
                            content_length = int(content_length_match.group(1))

                            if content_length > 9:
                                content_start = header_end + 4
                                content_end = header_end + 4 + content_length
                                content_bytes = section[content_start:content_end]
                                print("Content:", content_type == "image/jpeg")
                                # content_latin = content_bytes.decode("latin-1").encode('latin-1').decode('utf-8')

                                if content_type == "image/jpeg":

                                    # Specify the file path where you want to save the image
                                    file_path = "images/" + image_name
                                    image_name = ""

                                    # Open the file in binary write mode and write the image data to it
                                    with open(file_path, "wb") as f:
                                        f.write(content_bytes)

                                    print(f"Image saved as '{file_path}'")
                                else:
                                    print("Content type is not 'image/jpeg'.")
                                    json_data = string_to_json(
                                        content_bytes.decode("utf-8")
                                    )
                                    # print(type(json_data))
                                    my_object = DictToObject(json_data)
                                    my_object.Events[0]["images"] = (
                                        my_object.Events[0]["EventID"] + ".jpg"
                                    )
                                    image_name = my_object.Events[0]["images"]
                                    show_data(my_object.Events[0])
                                    # print(my_object.Events[0]['EventID'])

                                print("Section Number:", section_number)
                        else:
                            print("Content-Type or Content-Length not found.")

                        print("---------------------------------------------------")

                        section_number += 1
                data = sections[-1]

except Exception as e:
    print("An error occurred:", e)
