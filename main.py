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

            object = data.get("Object", {})
            traffic_car = data.get("TrafficCar", {})
            vehicle = data.get("NonMotor", {})
            riderList = vehicle.get("RiderList", [])

            # ตรวจสอบว่ามีข้อมูล TrafficCar และ PlateNumber หรือไม่
            if traffic_car and "PlateNumber" in traffic_car:
                plate_number_bytes = traffic_car["PlateNumber"].encode("latin-1")
                plate_number = plate_number_bytes.decode("utf-8")

                vehicleSize = traffic_car.get("VehicleSize", "")
                # ตรวจสอบว่ามี rider ใน riderList หรือไม่
                # สร้าง log ตามที่คุณต้องการ
                province_bytes = object.get("Province", "").encode("latin-1")
                # print(object)
                province = province_bytes.decode("utf-8")

                url = "http://localhost:8090/api/collections/dahua/records"
                headers = {"Content-Type": "application/json"}
                response = requests.post(
                    url,
                    headers=headers,
                    data={
                        "plateNumber": plate_number,
                        "color": traffic_car.get("VehicleColor", ""),
                        "province": province,
                        "vehicleSize": vehicleSize,
                    },
                )

                if response.status_code == 200:
                    print("Data sent successfully to Pocketbase.")
                else:
                    print(
                        "Failed to send data to Pocketbase. Status code:",
                        response.status_code,
                    )
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
