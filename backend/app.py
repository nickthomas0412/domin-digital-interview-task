"""This file contains the flask backend endpoints."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from local_database import fetch_latest_data

# Initialize the Flask application
app = Flask(__name__)
CORS(app)


@app.route("/latest_data", methods=["GET"])
def get_latest_data():
    """Return the latest data point for all sensors from the local DB.

    Returns:
        response(flask.Response): Response of the request
    """
    latest_data = fetch_latest_data()
    return jsonify(latest_data), 200


@app.route("/", methods=["GET"])
def get_custom_channels_and_time_period():
    """Return the data points specified by the channels and time period.

    Returns:
        response(flask.Response): Response of the request
    """
    channels = request.args.getlist("channels")
    start_time_str = request.args.get("start_time")
    end_time_str = request.args.get("end_time")

    if not channels or not start_time_str or not end_time_str:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO format."}), 400

    if start_time > end_time:
        return jsonify({"error": "start_time must be less than end_time"}), 400

    # Query not formed
    # queried_data = fetch_custom_data(channels, start_time, end_time)
    queried_data = {}

    return jsonify(queried_data), 200


# Start the Flask application
if __name__ == "__main__":
    app.run()
