# Domin Digital Interview Task
Interview task for the Software Engineer role at Domin.

## Prerequisites
- Node (Tested with 20.16.0)
- Python (Tested with 3.10.6)
- git

## Installation
1. Clone the repository
```
git clone https://github.com/nickthomas0412/domin-digital-interview-task.git
cd domin-digital-interview-task
```

2. Activate or create a python environment if one is required for the directory

On Windows
```
cd backend
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux
```
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the Python requirements
```
pip install -r requirements.txt
cd ..
```

4. Install the Node requirements
```
cd frontend
npm install
cd ..
```

5. Run the sensor application
```
cd backend
python main.py
```

6. Run the backend app
```
cd backend
flask run
``` 

7. Run the frontend:
```
cd frontend
npm run dev
```

8. Run simulated data through the system
```
cd backend
cd simulated_sensors
python udp_publisher.py
```

## Architecture talking points/ decisions:
1. Local DB, SQLite instead of more performant time based database selected as installed with Python
2. Showing latest value for all captured data attributes on the UI capped at 4 Hz as not specified
3. UI very basic due to brief but could easily be extended (embedded Grafana)
4. Flask chosen over FASTAPI as a known framework to myself and backend was very basic in this case
5. Threads spawned for each external sensor in the system - modular and isolated
6. Left and right suspension simulated with UDP connection at 100 Hz showcasing extendability
7. SQL data was set to only write its buffer every 0.5 seconds for performance on my laptop
8. SQL table configured with one table regardless of schema from sensors for querying ease and extendability
9. Sensor DAQ have error handling and simulated data checking, so it is failure tolerant
10. Sensor DAQ read data and put straight into a queue so that it is ready for the next datapoint (expecting no timestamp to be sent with data)
