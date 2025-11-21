# backend/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from .database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(255), nullable=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), nullable=True, unique=True)
    content = Column(Text, nullable=False)
    published_at = Column(DateTime, nullable=True)

    summary = Column(Text, nullable=True)
    topic = Column(String(100), nullable=True)
    sentiment = Column(String(50), nullable=True)

    image_url = Column(String(1000), nullable=True)  # <-- NEW

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("url", name="uq_news_url"),
    )
