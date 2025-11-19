from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# Intelleo core schemas map directly to MongoDB collections via their lowercase class names
# user -> users collection responsibilities (simple auth demo only)
class User(BaseModel):
    email: EmailStr
    password_hash: str
    company: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# devices coming from MQTT or external connectors
class Device(BaseModel):
    device_id: str
    name: str
    org: Optional[str] = None
    tags: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# minimal event frame representing 52+ metrics - flexible key/value map
class MetricEvent(BaseModel):
    device_id: str
    ts: datetime
    metrics: Dict[str, float] = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# inferred schema record for demo purposes
class InferredField(BaseModel):
    name: str
    dtype: str
    nullable: bool = True

class InferredSchema(BaseModel):
    source: str
    fields: List[InferredField]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# simple session token for demo auth flow
class SessionToken(BaseModel):
    user_id: str
    token: str
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
