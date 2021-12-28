#Parms
#python3 ingest_cputemperature.py <start_time> <duration>
#<start_time> cpu temperature will increase for <duration> minutes

import requests, time, sched, random, datetime, sys
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
timenow = int(now.strftime("%H%M"))

if (len(sys.argv) > 1):
    droptime = int(sys.argv[1])
    duration = int(sys.argv[2])
else:
    droptime = "0000"
    duration = 10

print("Current time: " + now.strftime("%H%M"))
print("Start simulation at: " + str(droptime) + " for " + str(duration) + " minutes")

METRICS_DROP = [
        {'id' : 'cpu.temperature', 'dims' : {'cpu' : 'cpu1'}, 'min' : 120, 'max' : 150 },
        {'id' : 'cpu.temperature', 'dims' : {'cpu' : 'cpu2'}, 'min' : 120, 'max' : 150 },
        {'id' : 'cpu.temperature', 'dims' : {'cpu' : 'cpu3'}, 'min' : 120, 'max' : 150 },
        {'id' : 'cpu.temperature', 'dims' : {'cpu' : 'cpu4'}, 'min' : 120, 'max' : 150 }
    ]

METRICS = [
        {'id' : 'cpu.temperature', 'dims' : {'cpu' : 'cpu1'}, 'min' : 30, 'max' : 90 },
        {'id' : 'cpu.temperature', 'dims' : {'cpu' : 'cpu2'}, 'min' : 30, 'max' : 90 },
        {'id' : 'cpu.temperature', 'dims' : {'cpu' : 'cpu3'}, 'min' : 30, 'max' : 90 },
        {'id' : 'cpu.temperature', 'dims' : {'cpu' : 'cpu4'}, 'min' : 30, 'max' : 90 }
    ]
scheduler = sched.scheduler(time.time, time.sleep)

def genSeries():
    mStr = ""
    now = datetime.now()
    timenow = int(now.strftime("%H%M"))
    if (timenow > int(droptime)) and (timenow < (int(droptime) + duration)):
        CURR_METRICS=METRICS_DROP
        print("Simulating high cpu temperature...")
    else:
        CURR_METRICS=METRICS  
    for metric in CURR_METRICS:
        dimStr = ""
        for dK in metric['dims']:
            dimStr += "," + dK + "=" + metric['dims'][dK]
        mStr += metric['id'] + dimStr + " " + str(random.randint(metric['min'], metric['max'])) + "\n"
    return mStr


def doit():
    scheduler.enter(60, 1, doit)
    payload = genSeries()
    print(payload)
    r = requests.post('http://localhost:14499/metrics/ingest', headers={'Content-Type': 'text/plain; charset=utf-8'}, data=payload)
    print(r)
    print(r.text)

print("START")
scheduler.enter(1, 1, doit)
scheduler.run()
