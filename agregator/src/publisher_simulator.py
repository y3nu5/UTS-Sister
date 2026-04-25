import requests
import random
from datetime import datetime
import time

URL = "http://localhost:8080/publish"

TOTAL = 5000


def generate_event(i):
    return {
        "topic": "sensor",
        "event_id": str(i),
        "timestamp": datetime.now().isoformat(),  # sudah benar
        "source": "publisher",
        "payload": {"value": random.randint(1, 100)}
    }

for i in range(TOTAL):
    e = generate_event(i)

    requests.post(URL, json=[e])

    if i % 500 == 0:
        print("sent:", i)

    # duplicate 20%
    if random.random() < 0.2:
        requests.post(URL, json=[e])

    time.sleep(0.001)

print("DONE")
r = requests.post(URL, json=[e])
print(r.status_code, r.text)