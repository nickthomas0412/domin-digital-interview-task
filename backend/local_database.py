"""This file contains the DatabaseWriter and DatabaseAccessor class to communicate with the local database."""

from datetime import datetime, timedelta
import threading
import time
from queue import Queue
import json

from sqlalchemy import text

from models import engine

DB_LOCK = threading.Lock()


class DatabaseWriter(threading.Thread):
    """DatabaseWriter class responsible for writing sensor data to the local database."""

    def __init__(self, data_q: Queue):
        """Initialise the DatabaseWriter class.

        Args:
            data_q (Queue): Input data queue.
        """
        super().__init__()
        self._queue = data_q
        self.lock = threading.Lock()
        self._write_interval = timedelta(seconds=0.5)
        self._retention_period = timedelta(seconds=100)
        self._clear_check_interval = timedelta(seconds=5)

    def run(self):
        """Main function called when the thread is started that handles writing and clear data from the database."""
        loop_start_time = datetime.now()
        last_write_time = loop_start_time
        last_clear_time = loop_start_time

        while True:
            current_time = datetime.now()
            # Write data to database every write interval
            if current_time - last_write_time >= self._write_interval:
                self._write_data_to_db()
                last_write_time = current_time
            # Clear any data now out of data every clear check interval
            if current_time - last_clear_time >= self._clear_check_interval:
                last_clear_time = current_time
                self._clear_old_data()
            time.sleep(0.1)

    def _write_data_to_db(self):
        """Write data from the input queue to the database."""
        if self._queue.empty():
            return

        with DB_LOCK:
            t_start = datetime.now()
            buffer = []
            while not self._queue.empty() and (datetime.now() - t_start) <= self._write_interval:
                buffer.append(self._queue.get())

            with engine.connect() as conn:
                conn.execute(
                    text(
                        "INSERT INTO sensor_data (timestamp, sensor_name, sensor_type, attributes) VALUES (:timestamp, :sensor_name, :sensor_type, :attributes)"
                    ),
                    buffer,
                )
                conn.commit()

    def _clear_old_data(self):
        """Clear data from the database that is older than the retention period."""
        with DB_LOCK:
            cutoff_time = datetime.now() - self._retention_period
            with engine.connect() as conn:
                conn.execute(
                    text("DELETE FROM sensor_data WHERE timestamp < :cutoff_time"),
                    {"cutoff_time": cutoff_time.isoformat()},
                )
                conn.commit()


def fetch_latest_data():
    """Fetch the latest data point for every sensor in the database.

    Returns:
        latest_data(list): List of latests data points for every sensor.
    """
    query = """
    SELECT timestamp, sensor_name, attributes
            FROM sensor_data
            WHERE (sensor_name, timestamp) IN (
                SELECT sensor_name, MAX(timestamp)
                FROM sensor_data
                GROUP BY sensor_name
            )
            """
    with DB_LOCK:
        with engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            latest_data = {}
            for row in result:
                result_dict = row._asdict()
                latest_data[result_dict["sensor_name"]] = json.loads(result_dict["attributes"])

    return latest_data
