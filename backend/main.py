from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from database import db, create_document, get_documents, ping
from schemas import User, Device, MetricEvent, InferredSchema, InferredField

app = FastAPI(title="Intelleo IoT Agent API", version="0.1.0")

# CORS for local dev and preview
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Intelleo IoT Agent API is running"}


@app.get("/test")
def test_db():
    try:
        ping()
        collections = sorted(db.list_collection_names())
        return {
            "backend": "ok",
            "database": "mongodb",
            "database_url": "hidden",
            "database_name": db.name,
            "connection_status": "connected",
            "collections": collections,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Demo: create a device
@app.post("/devices")
def create_device(device: Device):
    created = create_document("device", device.model_dump())
    return created


# Demo: list devices
@app.get("/devices")
def list_devices(limit: int = 50):
    return get_documents("device", limit=limit)


# Demo: ingest a metric event (simplified)
@app.post("/metrics")
def ingest_metric(evt: MetricEvent):
    created = create_document("metricevent", evt.model_dump())
    return created


# Demo: naive schema inference from a sample metric payload
class SamplePayload(BaseModel):
    source: str
    sample: Dict[str, Any]

@app.post("/infer-schema")
def infer_schema(payload: SamplePayload):
    sample = payload.sample
    inferred: List[InferredField] = []
    for k, v in sample.items():
        dtype = "number" if isinstance(v, (int, float)) else "boolean" if isinstance(v, bool) else "string"
        inferred.append(InferredField(name=k, dtype=dtype))
    schema = InferredSchema(source=payload.source, fields=inferred)
    created = create_document("inferredschema", schema.model_dump())
    return created
