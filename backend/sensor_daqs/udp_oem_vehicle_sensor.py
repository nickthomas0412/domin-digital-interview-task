"""This file contains the OEM Vehicle Sensor DAQ class."""
import socket
import requests
from datetime import datetime
import threading
from queue import Queue
import json


class OEMVehicleSensor(threading.Thread):
    """OEMVehicleSensor class responsible for udp communication to the vehicle."""

    UDP_IP = "localhost"
    UDP_PORT = 12345
    API_URL = "http://localhost:5000/update_sensor"
    UI_UPDATE_FREQUENCY = 10 

    def __init__(self, data_q: Queue):
        """Initialise the OEMVehicleSensor class.

        Args:
            data_q (Queue): Queue output to the local database.
        """
        super().__init__()
        self._data_q = data_q

    def run(self):
        """Main function called when the thread is started that captures any UDP messages and sends them on."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((OEMVehicleSensor.UDP_IP, OEMVehicleSensor.UDP_PORT))

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
                        "altitude": float(columns[0]),
                        "body_x_axis": float(columns[1]),
                        "body_y_axis": float(columns[2]),
                        "body_z_axis": float(columns[3]),
                        "fix": bool(int(columns[4])),
                        "horizontal_dilution": float(columns[5]),
                        "latitude": float(columns[6]),
                        "longitude": float(columns[7]),
                        "num_sats": float(columns[8]),
                        "spd_over_grnd": float(columns[9]),
                        "timestamps": float(columns[10]),
                        "vehicle_accel_x": float(columns[11]),
                        "vehicle_accel_y": float(columns[12]),
                        "vehicle_accel_z": float(columns[13]),
                        "vehicle_gyro_x": float(columns[14]),
                        "vehicle_gyro_y": float(columns[15]),
                        "vehicle_gyro_z": float(columns[16]),
                        "vehicle_mag_x": float(columns[17]),
                        "vehicle_mag_y": float(columns[18]),
                        "vehicle_mag_z": float(columns[19]),
                        "vehicle_orientation_x": float(columns[20]),
                        "vehicle_orientation_y": float(columns[21]),
                        "vehicle_orientation_z": float(columns[22]),
                        "wheel_x_axis": float(columns[23]),
                        "wheel_y_axis": float(columns[24]),
                        "wheel_z_axis": float(columns[25]),
                    }

                    payload = {
                        "timestamp": timestamp,
                        "sensor_name": "VehicleSensor1",
                        "sensor_type": "VehicleData",
                        "attributes": json.dumps(data_dict),
                    }

                    # Add data to the queue
                    self._data_q.put(payload)
                    payload = {
                        "sensor_name": "VehicleSensor",
                        "sensor_type": "VehicleData",
                        "attributes": data_dict,
                    }
                    # Send data to the API endpoint at intervals
                    if (datetime.now() - last_ui_update).total_seconds() > (
                        1 / OEMVehicleSensor.UI_UPDATE_FREQUENCY
                    ):
                        response = requests.post(OEMVehicleSensor.API_URL, json=payload)
                        if response.status_code != 200:
                            print(f"Failed to send data: {response.status_code}, {response.text}")
                        last_ui_update = datetime.now()

                except ValueError as e:
                    print(f"ValueError while processing data: {e}")
                except requests.RequestException as e:
                    print(f"RequestException while sending data to API: {e}")
