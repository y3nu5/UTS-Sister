import pytest
import asyncio

from src.dedup_store import init_db, add_event, is_duplicate


@pytest.mark.asyncio
async def test_dedup():

    await init_db()

    topic = "test"
    event_id = "123"

    await add_event(topic, event_id)

    duplicate = await is_duplicate(topic, event_id)

    assert duplicate is True