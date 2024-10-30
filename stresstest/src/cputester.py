import itertools, math, time, sys
from flask import Flask, request, jsonify
import os
import requests
import datetime

app = Flask(__name__)
app.debug = True
time_period = float(os.getenv('TIME_PERIOD', 30.0))
time_slice = float(os.getenv('TIME_SLICE', 0.04))

# Get host and port from environment variables
metric_host = os.getenv('METRIC_HOST', 'localhost')
metric_port = os.getenv('METRIC_PORT', '8000')

@app.route('/start', methods=['POST'])
def start_test():
    print("start endpoint", flush=True)
    testCPU()
    return jsonify({"message": "Test started successfully"}), 200

def testCPU():
    print("start testing", flush=True)
    recordEntry("stresstest::testCPU")
    N = int(time_period / time_slice)
    print("N is "+ str(N), flush=True)
    entime = time.time()+N
    t = time.time()
    while t < entime:
        t = t/3.1415
        t = time.time()
    recordExit("stresstest::testCPU")
    print("stop testing", flush=True)

def testCPU2():
    print("start testing2", flush=True)
    recordEntry("stresstest::testCPU")
    N = int(time_period / time_slice)
    print("N is "+ str(N), flush=True)
    for i in itertools.cycle(range(N)):
        busy_time = time_slice / 2 * (math.sin(2*math.pi*i/N) + 1)
        t = time.perf_counter() + busy_time
        while t > time.perf_counter():
            pass
        time.sleep(time_slice - busy_time);   
    recordExit("stresstest::testCPU")
    print("stop testing2", flush=True)

def recordEntry(entrypoint):    
    # Construct the API URL
    url = f"http://{metric_host}:{metric_port}/entry"
    
    # Get the current UTC timestamp
    observed_at = int(datetime.datetime.utcnow().timestamp())
    
    # Create the JSON payload
    payload = {
        "entryPoint": entrypoint,
        "observedAt": observed_at
    }
    
    try:
        # Send the POST request
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        print(f"Successfully recorded entry for {entrypoint} at {observed_at}")
    except requests.exceptions.RequestException as e:
        print(f"Error recording entry for {entrypoint}: {e}")

def recordExit(exitpoint):    
    # Construct the API URL
    url = f"http://{metric_host}:{metric_port}/exit"
    
    # Get the current UTC timestamp
    observed_at = int(datetime.datetime.utcnow().timestamp())
    
    # Create the JSON payload
    payload = {
        "exitPoint": exitpoint,
        "observedAt": observed_at
    }
    
    try:
        # Send the POST request
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        print(f"Successfully recorded exit for {exitpoint} at {observed_at}")
    except requests.exceptions.RequestException as e:
        print(f"Error recording exit for {exitpoint}: {e}")

if __name__ == '__main__':
    port = int(os.getenv('ADAPTER_PORT', 5000))
    app.run(host='0.0.0.0', port=port)
