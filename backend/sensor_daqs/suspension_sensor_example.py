"""This file contains the Suspension Sensor DAQ class."""
import socket
import requests
from datetime import datetime
import threading
from queue import Queue
import json


class SuspensionSensor(threading.Thread):
    """SuspensionSensor class responsible for communication to the suspension."""

    UDP_IP = "localhost"
    UDP_PORT = 12345
    API_URL = "http://localhost:5000/update_sensor"
    UI_UPDATE_FREQUENCY = 10 

    def __init__(self, data_q: Queue, corner: str):
        """Initialise the class SuspensionSensor class.

        Args:
            data_q (Queue): Queue output to the local database.
            corner (string): Corner of the vehicle.
        """
        super().__init__()
        self._data_q = data_q
        self._corner = corner

    def run(self):
        """Main function called when the thread is started that captures any UDP messages and sends them on."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self._corner.upper() == "FRONTLEFT":
            udp_port = SuspensionSensor.UDP_PORT + 1
        elif self._corner.upper() == "FRONTRIGHT":
            udp_port = SuspensionSensor.UDP_PORT + 2
        elif self._corner.upper() == "BACKLEFT":
            udp_port = SuspensionSensor.UDP_PORT + 3
        elif self._corner.upper() == "BACKRIGHT":
            udp_port = SuspensionSensor.UDP_PORT + 4

        sock.bind((SuspensionSensor.UDP_IP, udp_port ))

        last_ui_update = datetime.now()

        while True:
            data, addr = sock.recvfrom(1024)
            receive_time = datetime.now()
            timestamp = receive_time.isoformat()
            decoded = data.decode()
            columns = decoded.split(",")

            if len(columns) == 26:
                try:
                    data_dict = {
                        "potentiometer": float(columns[1]),
                        "timestamps": float(columns[10]),
                        "hub_accel_x": float(columns[11]),
                        "hub_accel_y": float(columns[12]),
                        "hub_accel_z": float(columns[13]),
                        "wheel_accel_x": float(columns[11]) * 1.5,
                        "wheel_accel_y": float(columns[12]) * 1.5,
                        "wheel_accel_z": float(columns[13]) * 1.5,
                    }

                    payload = {
                        "timestamp": timestamp,
                        "sensor_name": f"SuspensionSensor{self._corner}",
                        "sensor_type": "SuspensionData",
                        "attributes": json.dumps(data_dict),
                    }

                    # Add data to the queue
                    self._data_q.put(payload)
                    payload = {
                        "sensor_name": f"SuspensionSensor{self._corner}",
                        "sensor_type": "SuspensionData",
                        "attributes": data_dict,
                    }
                    # Send data to the API endpoint at intervals
                    if (datetime.now() - last_ui_update).total_seconds() > (
                        1 / SuspensionSensor.UI_UPDATE_FREQUENCY
                    ):
                        response = requests.post(SuspensionSensor.API_URL, json=payload)
                        if response.status_code != 200:
                            print(f"Failed to send data: {response.status_code}, {response.text}")
                        last_ui_update = datetime.now()

                except ValueError as e:
                    print(f"ValueError while processing data: {e}")
                except requests.RequestException as e:
                    print(f"RequestException while sending data to API: {e}")
