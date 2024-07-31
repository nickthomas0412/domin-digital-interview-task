"""This file was forked from the Domin GitHub interview task repo with minor modifications."""
import csv
import socket
import time
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

data = []
with open(
    os.path.join(os.path.dirname(__file__), "sample_vehicle_data_6kph.csv"), newline=""
) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create a UDP socket

start_time = time.time()
data = data[2:]  # remove the header

logger.log(logging.INFO, "sending data")

for index, row in enumerate(data):
    while float(row[10]) > time.time() - start_time:  # check row ts is not in the future
        logger.log(logging.INFO, {"waiting for": row[10]})
        pass
    message = ",".join(row).encode()
    sock.sendto(message, ("localhost", 12345)) # Vehicle data
    if index % 10 == 0:
        sock.sendto(message, ("localhost", 12346)) # Suspension front left
        sock.sendto(message, ("localhost", 12347)) # Suspension front right

    logger.log(logging.INFO, {"sent:": message})

sock.close()
logger.log(logging.INFO, "done")
