from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

# Example schemas to reference when defining real collections
class User(BaseModel):
    email: EmailStr
    password_hash: str
    company: Optional[str] = None
    role: str = Field(default="member")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Device(BaseModel):
    device_id: str
    name: str
    org_id: Optional[str] = None
    tags: List[str] = []
    metrics: Dict[str, float] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Task(BaseModel):
    title: str
    done: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
