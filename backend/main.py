# backend/main.py
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import News
from .schemas import NewsCreate, NewsOut, NewsListResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI News Aggregator API (Ollama)")


@app.post("/news", response_model=NewsOut)
def create_news(item: NewsCreate, db: Session = Depends(get_db)):
    if item.url:
        existing = db.query(News).filter(News.url == item.url).first()
        if existing:
            return existing

    news_obj = News(
        source=item.source,
        title=item.title,
        url=item.url,
        content=item.content,
        published_at=item.published_at,
        image_url=item.image_url,
    )
    db.add(news_obj)
    db.commit()
    db.refresh(news_obj)
    return news_obj


@app.get("/news", response_model=NewsListResponse)
def list_news(
    db: Session = Depends(get_db),
    topic: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    query = db.query(News)

    if topic:
        query = query.filter(News.topic.ilike(f"%{topic}%"))
    if q:
        pattern = f"%{q}%"
        query = query.filter(
            News.title.ilike(pattern) | News.content.ilike(pattern)
        )

    total = query.count()
    items = (
        query.order_by(News.published_at.desc().nullslast(), News.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return NewsListResponse(total=total, items=items)


@app.get("/news/{news_id}", response_model=NewsOut)
def get_news(news_id: int, db: Session = Depends(get_db)):
    news_obj = db.query(News).filter(News.id == news_id).first()
    if not news_obj:
        raise HTTPException(status_code=404, detail="News not found")
    return news_obj
