"""This file contains the Suspension Sensor DAQ class."""

import socket
from datetime import datetime
import threading
from queue import Queue
import json


class SuspensionSensor(threading.Thread):
    """SuspensionSensor class responsible for communication to the suspension."""

    UDP_IP = "localhost"
    UDP_PORT = 12345

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
        else:
            raise ValueError("Unknown udp port for suspension")

        sock.bind((SuspensionSensor.UDP_IP, udp_port))

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                receive_time = datetime.now()
                timestamp = receive_time.isoformat()
                decoded = data.decode()
                columns = decoded.split(",")

                if len(columns) == 26:
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

                    # A second queue would be setup to send to actor sending data to the cloud for instance

            except ValueError as e:
                print(f"ValueError while processing data: {e}")

            except Exception as e:
                print(f"General exception triggered while recording sensor data: {e}")
