import aiosqlite

DB_FILE = "data/dedup.db"


async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS dedup (
                topic    TEXT NOT NULL,
                event_id TEXT NOT NULL,
                PRIMARY KEY (topic, event_id)
            )
            """
        )
        await db.commit()


async def add_if_not_duplicate(topic: str, event_id: str) -> bool:
    """
    Coba insert event secara atomik.
    Return True  → event baru, berhasil diinsert.
    Return False → duplikat, diabaikan.
    """
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute(
            "INSERT OR IGNORE INTO dedup(topic, event_id) VALUES (?, ?)",
            (topic, event_id),
        )
        await db.commit()
        return cursor.rowcount > 0