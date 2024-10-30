import itertools, math, time, sys
from flask import Flask, request, jsonify
import os


app = Flask(__name__)

time_period = float(os.getenv('TIME_PERIOD', 30.0))
time_slice = float(os.getenv('TIME_SLICE', 0.04))


@app.route('/start', methods=['POST'])
def start_test():
    testCPU()

def testCPU():
    N = int(time_period / time_slice)
    for i in itertools.cycle(range(N)):
        busy_time = time_slice / 2 * (math.sin(2*math.pi*i/N) + 1)
        t = time.perf_counter() + busy_time
        while t > time.perf_counter():
            pass
        time.sleep(time_slice - busy_time);   

if __name__ == '__main__':
    port = int(os.getenv('ADAPTER_PORT', 5000))
    app.run(host='0.0.0.0', port=port)
