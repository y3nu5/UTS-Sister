Event Aggregator — UTS Sistem Terdistribusi
NamaMuhammad YunusNIM11231066Mata KuliahSistem Terdistribusi

Deskripsi Sistem
Event Aggregator adalah layanan berbasis FastAPI yang mensimulasikan pola at-least-once delivery pada sistem terdistribusi. Sistem menerima event dari publisher, memproses event secara asinkron melalui antrian internal, dan menjamin idempotency menggunakan dedup store berbasis SQLite.

Arsitektur
Publisher (HTTP POST /publish)
        │
        ▼
  [ FastAPI Endpoint ]
        │
        ▼
  [ asyncio.Queue ]
        │
        ▼
  [ Consumer Worker ]
        │
        ├──► Duplicate? ──► Drop + stats.duplicate_dropped++
        │        │
        │    (SQLite dedup store — INSERT OR IGNORE)
        │
        └──► Baru? ──► store_event() + stats.unique_processed++
                              │
                         [ In-Memory Storage ]

Struktur Folder
agregator/
├── Dockerfile
├── requirements.txt
├── data/                       # Volume mount — dedup.db disimpan di sini
└── src/
    ├── main.py                 # FastAPI app, startup, routing
    ├── consumer.py             # Async consumer worker
    ├── dedup_store.py          # SQLite dedup dengan INSERT OR IGNORE (atomik)
    ├── models.py               # Pydantic model Event
    ├── queue_worker.py         # asyncio.Queue instance
    ├── stats.py                # Counter stats (received, unique, duplicate)
    ├── storage_event.py        # In-memory event storage
    └── publisher_simulator.py  # Simulasi 5000 event + 20% duplikat

Cara Menjalankan
1. Build Docker Image
bashdocker build -t event-processor .
2. Run Container
bashdocker run -p 8080:8080 -v $(pwd)/data:/app/data event-processor

Catatan: Flag -v $(pwd)/data:/app/data memastikan dedup.db tersimpan di host sehingga data tetap ada setelah container di-restart.

3. Kirim Event (Simulator)
bashpython -m src.publisher_simulator
Simulator mengirim 5.000 event unik ditambah ~20% duplikat secara acak.

Endpoint API
MethodEndpointDeskripsiPOST/publishMenerima list Event, masukkan ke queueGET/eventsAmbil semua event (opsional filter ?topic=)GET/statsLihat statistik sistem
Contoh POST /publish
json[
  {
    "topic": "sensor",
    "event_id": "abc-123",
    "timestamp": "2025-01-01T00:00:00",
    "source": "device-1",
    "payload": {"value": 42}
  }
]
Contoh GET /stats
json{
  "received": 6024,
  "unique_processed": 5000,
  "duplicate_dropped": 1024,
  "topics": ["sensor"],
  "uptime": 312
}

Idempotency & Dedup
Dedup store menggunakan INSERT OR IGNORE pada SQLite dengan primary key (topic, event_id). Operasi ini atomik — tidak ada race condition antara pengecekan duplikat dan insert, karena keduanya terjadi dalam satu transaksi database.
pythoncursor = await db.execute(
    "INSERT OR IGNORE INTO dedup(topic, event_id) VALUES (?, ?)",
    (topic, event_id),
)
return cursor.rowcount > 0  # True = baru, False = duplikat

Persistensi Dedup Store
dedup.db di-mount sebagai Docker volume ke ./data/ di host. Ketika container di-restart, data dedup tetap ada sehingga event yang sudah diproses tidak akan diproses ulang.

Video Demo
🎥 Link video demo: [akan ditambahkan setelah upload ke YouTube]

Referensi
Tanenbaum, A. S., & Van Steen, M. (2007). Distributed systems: Principles and paradigms (2nd ed.). Prentice Hall.
