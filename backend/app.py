"""This file contains the flask backend endpoints."""
from flask import Flask, request, jsonify
from flask_cors import CORS

from local_database import fetch_latest_data
from in_memory_data_store import InMemoryDataStore

# Initialize the Flask application and the datastore
app = Flask(__name__)
CORS(app)
data_store = InMemoryDataStore()


@app.route("/update_sensor", methods=["POST"])
def update_sensor():
    """Update the latest sensor data point in the in-memory database."""
    data = request.json
    sensor_name = data.get("sensor_name")
    sensor_type = data.get("sensor_type")
    attributes = data.get("attributes")

    if not sensor_name or not isinstance(attributes, dict):
        return jsonify({"error": "Invalid request data"}), 400

    data_store.update_sensor_data(sensor_name, attributes)
    return jsonify({"message": "Data updated successfully"}), 200


@app.route("/latest_data", methods=["GET"])
def get_latest_data():
    """Return the latest data point for all sensors.

    Returns:
        response(flask.Response): Response of the request
    """
    #latest_data = data_store.get_latest_data()
    latest_data = fetch_latest_data()
    return jsonify(latest_data), 200


# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
