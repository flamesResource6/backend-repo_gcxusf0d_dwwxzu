import os
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app_db")

_client: Optional[MongoClient] = None
_db = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(DATABASE_URL, serverSelectionTimeoutMS=3000)
    return _client


def get_db():
    global _db
    if _db is None:
        _db = get_client()[DATABASE_NAME]
    return _db


# Expose db handle for convenience
_db_handle = get_db()
db = _db_handle


def collection(name: str) -> Collection:
    return get_db()[name]


def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.utcnow()
    payload = {**data, "created_at": now, "updated_at": now}
    col = collection(collection_name)
    result = col.insert_one(payload)
    return {"_id": str(result.inserted_id), **{k: v for k, v in payload.items()}}


def get_documents(
    collection_name: str,
    filter_dict: Optional[Dict[str, Any]] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    filter_dict = filter_dict or {}
    docs = collection(collection_name).find(filter_dict).limit(limit)
    out: List[Dict[str, Any]] = []
    for d in docs:
        d["_id"] = str(d.get("_id"))
        out.append(d)
    return out


def ping() -> Dict[str, str]:
    client = get_client()
    client.admin.command("ping")
    return {"status": "ok"}
