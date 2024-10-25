import requests
from dahua_rpc import DahuaRpc
from datetime import datetime
import json
import time
import re
import base64


def callback(data):
    #   print("data", data)
    try:
        corrected_json = re.sub(r"\'(.*?)\'", r'"\1"', data)

        # หา substring ที่อยู่ใน "{}"
        start_index = corrected_json.find("{")
        end_index = corrected_json.rfind("}")
        json_data = corrected_json[start_index : end_index + 1]
        # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # แปลงข้อมูล JSON เป็น dictionary ใน Python
        data_dict = json.loads(json_data)
        params_data = data_dict.get("params", {})
        event_list = params_data.get("eventList", [])
        for event_data in event_list:
            data = event_data.get("Data", {})

            object = data.get("Object", {})
            traffic_car = data.get("TrafficCar", {})
            vehicle = data.get("NonMotor", {})

            # base64_data = data.get("ÿØÿà JFIF    ÿÛ Å ", {})

            # ตรวจสอบว่ามีข้อมูล TrafficCar และ PlateNumber หรือไม่
            if traffic_car and "PlateNumber" in traffic_car:
                plate_number_bytes = traffic_car["PlateNumber"].encode("latin-1")
                plate_number = plate_number_bytes.decode("utf-8")

                vehicleSize = traffic_car.get("VehicleSize", "")
                VehicleSign = traffic_car.get("VehicleSign", "")
                # image_bytes = base64.b64decode(base64_data)

                province_bytes = object.get("Province", "").encode("latin-1")
                # print(object)
                province = province_bytes.decode("utf-8")
                # print("data: ", traffic_car)
                # print("data_dict: ", data_dict)
                # full_filename = f"trafficCar_{timestamp}.jpeg"

                # บันทึกภาพเป็นไฟล์แยกต่างหาก (ต้องเพิ่มโค้ดนี้)
                # with open("/image/full_filename", "wb") as f:
                #   f.write(image_bytes)

                url = "http://localhost:8090/api/collections/dahua/records"
                headers = {"Content-Type": "application/json"}
                data = {
                    "plateNumber": plate_number,
                    "color": traffic_car.get("VehicleColor", ""),
                    "province": province,
                    "vehicleSize": vehicleSize,
                    "brand": VehicleSign,
                    # "img": full_filename,
                }
                try:
                    # response = requests.post(url, headers=headers, data={"img": full_filename, **data})
                    response = requests.post(url, headers=headers, json=data)
                    if response.status_code == 200:
                        print("Data sent successfully to Pocketbase.")
                    else:
                        print(
                            "Failed to send data to Pocketbase. Status code:",
                            response.status_code,
                        )
                except Exception as e:
                    print("PlateNumber is undefined.")

    except Exception as e:
        print("Waiting for detection..")


# Function to start listening to events
def start_listen_events():
    # Initialize the object
    dahua = DahuaRpc(host="10.100.62.203", username="admin", password="nw@army66")

    # Login to create session
    dahua.login()

    # Get the current time on the device (assuming get_time is the correct method)
    # print(dahua.get_time())

    # Attach event listener for "TrafficJunction" (assuming attach_event is the correct method)
    print(dahua.attach_event(["TrafficJunction"]))

    print("Starting event listener...")
    return dahua.listen_events(callback)


def stop_listen_events():
    print("Stopping event listener...")
    # listener.stop()
    print(start_listen_events())


# Initial listen
print(start_listen_events())

while True:
    # Wait for 10 seconds before restarting the listener
    time.sleep(10)

    # Restart the listener
    start_listen_events()


# Function to start listening to events
def start_listen_events():
    # Initialize the object
    dahua = DahuaRpc(host="10.100.62.203", username="admin", password="nw@army66")

    # Login to create session
    dahua.login()

    # Get the current time on the device (assuming get_time is the correct method)
    # print(dahua.get_time())

    # Attach event listener for "TrafficJunction" (assuming attach_event is the correct method)
    print(dahua.attach_event(["TrafficJunction"]))

    print("Starting event listener...")
    return dahua.listen_events(callback)


def stop_listen_events():
    print("Stopping event listener...")
    # listener.stop()
    print(start_listen_events())


# Initial listen
print(start_listen_events())

while True:
    # Wait for 10 seconds before restarting the listener
    time.sleep(10)

    # Restart the listener
    start_listen_events()
