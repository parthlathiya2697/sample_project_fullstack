from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ItemCreate(BaseModel):
    value: str
    name: str
    notes: Optional[str] = None
    completed: bool = False
    duration: Optional[int] = None


class ItemUpdate(ItemCreate):
    pass


class Item(ItemCreate):
    id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True
