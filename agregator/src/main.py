from fastapi import FastAPI
from typing import List, Union

import asyncio

from src.models import Event
from src.queue_worker import event_queue
from src.stats import stats
from src.consumer import consumer_worker
from src.storage_event import get_events
from src.dedup_store import init_db
from fastapi import Body


app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_db()
    asyncio.create_task(consumer_worker())  # langsung, tanpa get_event_loop()
    print("APP STARTED")


@app.post("/publish")
async def publish(events: list[Event] = Body(...)):

    for event in events:

        await event_queue.put(event)

        stats.received += 1

    return {"status": "accepted", "count": len(events)}


@app.get("/events")
def events(topic: str = None):

    data = get_events(topic)

    return [e.model_dump() for e in data]


@app.get("/stats")
def get_stats():

    return {
        "received": stats.received,
        "unique_processed": stats.unique_processed,
        "duplicate_dropped": stats.duplicate_dropped,
        "topics": list(stats.topics),
        "uptime": stats.uptime(),
    }