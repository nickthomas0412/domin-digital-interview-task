"""This file contains the InMemoryDataStore which looks after the latest attribute value for each sensor.

"""

import threading
from typing import Dict, Any


class InMemoryDataStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.data = {}

    def update_sensor_data(self, sensor_name: str, attributes: Dict[str, Any]):
        with self.lock:
            if sensor_name not in self.data:
                self.data[sensor_name] = {}
            self.data[sensor_name] = attributes

    def get_latest_data(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        with self.lock:
            return self.data.copy()
