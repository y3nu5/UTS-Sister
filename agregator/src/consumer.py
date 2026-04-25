import asyncio

from src.queue_worker import event_queue
from src.dedup_store import add_if_not_duplicate
from src.storage_event import store_event
from src.stats import stats


async def consumer_worker():
    print("[CONSUMER] started")

    while True:
        event = await event_queue.get()

        try:
            topic = event.topic
            event_id = event.event_id

            is_new = await add_if_not_duplicate(topic, event_id)

            if is_new:
                store_event(event)
                stats.unique_processed += 1
                stats.topics.add(topic)
                print(f"[OK]        topic={topic} event_id={event_id}")
            else:
                stats.duplicate_dropped += 1
                print(f"[DUPLICATE] topic={topic} event_id={event_id}")

        except Exception as e:
            print(f"[ERROR] consumer error: {e}")

        finally:
            event_queue.task_done()