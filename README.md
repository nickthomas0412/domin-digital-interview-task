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
```

2. Install Python requirements
```
cd backend
pip install -r requirement.txt
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

5. Run the backend ap
```
cd backend
flask run
cd ..
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