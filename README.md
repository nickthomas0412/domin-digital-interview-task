# domin-digital-interview-task
Interview task for the Software Engineer role at Domin

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

2. Install Python requirements (activate or create a python environment)
If a new venv is required for the directory then:

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

```
pip install -r requirements.txt
cd ..
```

3. Install the Node requirements
```
cd frontend
npm install
cd ..
```

4. Run the sensor application
```
cd backend
python main.py
```

5. Run the backend app
```
cd backend
flask run
``` 

6. Run the frontend:
```
cd frontend
npm run dev
```

7. Run simulated data through the system
```
cd backend
cd simulated_sensors
python udp_publisher.py
```

## Architecture talking points/ decisions:
1. Local DB, SQLite instead of more performant time based database selected as installed with Python
2. Showing latest value for all captured data attributes on the UI capped at 10 Hz pulled from in memory database compared to local DB due to performance
3. Flask vs FASTAPI