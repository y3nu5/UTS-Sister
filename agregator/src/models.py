from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Any, Dict

class Event(BaseModel):
    topic: str = Field(..., min_length=1)
    event_id: str = Field(..., min_length=1)
    timestamp: str
    source: str
    payload: Dict[str, Any]

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(cls, value):
        try:
            datetime.fromisoformat(value)
        except Exception:
            raise ValueError("timestamp must be ISO8601")
        return value