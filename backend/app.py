"""This file contains the flask backend endpoints."""

from flask import Flask, jsonify
from flask_cors import CORS

from local_database import fetch_latest_data

# Initialize the Flask application and the datastore
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


# Start the Flask application
if __name__ == "__main__":
    app.run()
