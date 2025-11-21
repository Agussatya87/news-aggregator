# backend/schemas.py
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class NewsBase(BaseModel):
    source: Optional[str] = None
    title: str
    url: Optional[str] = None
    content: str
    published_at: Optional[datetime] = None
    image_url: Optional[str] = None  # optional di base


class NewsCreate(NewsBase):
    pass


class NewsOut(NewsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    summary: Optional[str] = None
    topic: Optional[str] = None
    sentiment: Optional[str] = None
    created_at: datetime


class NewsListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total: int
    items: List[NewsOut]
