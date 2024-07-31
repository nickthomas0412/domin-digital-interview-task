"""This file simulates the vehicle sensor output and DAQ functions.

Note the spawned threads are not always killed cleanly when the application close.
They are purely for a demonstration of sensors and DAQ functions.
"""

import time
from queue import Queue

from local_database import DatabaseWriter
from sensor_daqs.udp_oem_vehicle_sensor import OEMVehicleSensor
from sensor_daqs.suspension_sensor_example import SuspensionSensor


def main():
    """Launch the sensor DAQs and start stream of sensor data."""
    data_queue = Queue()
    local_database = DatabaseWriter(data_queue)
    local_database.daemon = True
    local_database.start()

    vehicle_sensor_thread = OEMVehicleSensor(data_queue)
    vehicle_sensor_thread.daemon = True
    vehicle_sensor_thread.start()

    front_left_sensor_thread = SuspensionSensor(data_queue, "FrontLeft")
    front_left_sensor_thread.daemon = True
    front_left_sensor_thread.start()

    front_right_sensor_thread = SuspensionSensor(data_queue, "FrontRight")
    front_right_sensor_thread.daemon = True
    front_right_sensor_thread.start()

    
    from local_database import fetch_latest_data
    data = fetch_latest_data()

    while True:
        time.sleep(0.1)


if __name__ == "__main__":
    main()
