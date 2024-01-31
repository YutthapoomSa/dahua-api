import requests
from dahua_rpc import DahuaRpc
from bs4 import BeautifulSoup
import json
import time
import re
import codecs


def callback(data):
    try:
        corrected_json = re.sub(r"\'(.*?)\'", r'"\1"', data)

        # หา substring ที่อยู่ใน "{}"
        start_index = corrected_json.find("{")
        end_index = corrected_json.rfind("}")
        json_data = corrected_json[start_index : end_index + 1]

        # แปลงข้อมูล JSON เป็น dictionary ใน Python
        data_dict = json.loads(json_data)
        params_data = data_dict.get("params", {})
        event_list = params_data.get("eventList", [])
        for event_data in event_list:
            data = event_data.get("Data", {})
            traffic_car = data.get("TrafficCar", {})
            vehicle = data.get("Vehicle", {})

            # ตรวจสอบว่ามีข้อมูล TrafficCar และ PlateNumber หรือไม่
            if traffic_car and "PlateNumber" in traffic_car:
                plate_number_bytes = traffic_car["PlateNumber"].encode("latin-1")
                plate_number = plate_number_bytes.decode("utf-8")

                # สร้าง log ตามที่คุณต้องการ
                log_data = {
                    "plateNumber": plate_number,
                    # "mainColor": vehicle.get("MainColor", ""),
                    # เพิ่มข้อมูลอื่น ๆ ตามต้องการ
                }
                print("data =", log_data)
            else:
                print("PlateNumber is undefined")
    except json.JSONDecodeError as e:
        print("...")


# Function to start listening to events
def start_listen_events():
    # Initialize the object
    dahua = DahuaRpc(host="localhost", username="admin", password="nw@army66")

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
