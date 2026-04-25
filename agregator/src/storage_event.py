from collections import defaultdict

event_storage = defaultdict(list)


def store_event(event):

    event_storage[event.topic].append(event)


def get_events(topic=None):

    if topic:
        return event_storage.get(topic, [])

    all_events = []

    for t in event_storage:
        all_events.extend(event_storage[t])

    return all_events