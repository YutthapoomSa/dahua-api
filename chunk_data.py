import requests
from dahua_rpc import DahuaRpc
from datetime import datetime
import json
import time
import re
import base64

def checkdata(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.text.split('--myboundary')
            for chunk in data:
                if 'Heartbeat' in chunk:
                    print("Found Heartbeat")
                else:
                    print("Heartbeat not found")
        else:
            print("Failed. Status code:", response.status_code)
    except Exception as e:
        print("Data is undefined.")

# URL to check
url = "http://10.100.62.203/cgi-bin/snapManager.cgi?action=attachFileProc&channel=1&heartbeat=5&Flags[0]=Event&Events=[VideoMotion%2CANPR]"

checkdata(url)

def start_listen_events():
    # Initialize the object
    dahua = DahuaRpc(host="10.100.62.202", username="admin", password="nw@army66")

    # Login to create session
    dahua.login()

    # Get the current time on the device (assuming get_time is the correct method)
    # print(dahua.get_time())

    # Attach event listener for "TrafficJunction" (assuming attach_event is the correct method)
    print(dahua.attach_event(["TrafficJunction"]))

    print("Starting event listener...")
    return dahua.listen_events(checkdata)

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