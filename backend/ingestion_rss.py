# backend/ingestion_rss.py
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import mktime

from .database import SessionLocal
from .models import News
from .config import summarize_and_tag

RSS_SOURCES = [
    {
        "name": "BBC News",
        "url": "https://rss.app/feeds/50T8PbAHQqHn3vXf.xml",
    },
    # Bisa tambah kanal lain kalau mau
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def parse_datetime(entry):
    if getattr(entry, "published_parsed", None):
        return datetime.fromtimestamp(mktime(entry.published_parsed))
    if getattr(entry, "updated_parsed", None):
        return datetime.fromtimestamp(mktime(entry.updated_parsed))
    return None


def fetch_article_content_with_html(url: str):
    """
    Fetch HTML artikel dan ekstrak teks konten + HTML mentah.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"[WARN] Gagal fetch artikel {url} | {e}")
        return "", ""

    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    # Struktur umum Antara: div.post-content atau article
    content_el = soup.find("div", class_="post-content") or soup.find("article")

    if content_el:
        paragraphs = content_el.find_all("p")
    else:
        paragraphs = soup.find_all("p")

    text = " ".join(p.get_text(strip=True) for p in paragraphs)
    return text, html


def extract_image_from_rss(entry):
    """
    Coba ambil image URL dari RSS entry: enclosures, media_content, media_thumbnail.
    """
    # feedparser biasanya pakai .enclosures
    enclosures = getattr(entry, "enclosures", [])
    if enclosures:
        url = enclosures[0].get("url")
        if url:
            return url

    media_content = entry.get("media_content", [])
    if media_content:
        url = media_content[0].get("url")
        if url:
            return url

    media_thumbnail = entry.get("media_thumbnail", [])
    if media_thumbnail:
        url = media_thumbnail[0].get("url")
        if url:
            return url

    return None


def extract_image_from_html(html: str):
    """
    Fallback: cari image dari HTML artikel kalau RSS tidak menyediakan.
    """
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # Coba meta og:image
    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        return og["content"]

    # Coba figure > img
    fig = soup.find("figure")
    if fig:
        img = fig.find("img")
        if img and img.get("src"):
            return img["src"]

    # Coba img pertama secara umum
    img = soup.find("img")
    if img and img.get("src"):
        return img["src"]

    return None


def ingest_from_rss():
    db = SessionLocal()

    for source in RSS_SOURCES:
        print(f"[INFO] Fetching RSS from {source['name']}: {source['url']}")

        try:
            resp = requests.get(source["url"], headers=HEADERS, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"[ERROR] Gagal fetch RSS {source['name']}: {e}")
            continue

        feed = feedparser.parse(resp.content)
        print(f"[INFO] {source['name']} entries: {len(feed.entries)}")

        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()

            if not title or not link:
                print("[WARN] Skip entry karena title atau link kosong")
                continue

            # Cek duplikasi berdasarkan URL
            exists = db.query(News).filter(News.url == link).first()
            if exists:
                continue

            published_at = parse_datetime(entry)
            summary_rss = entry.get("summary", "").strip()

            # Konten + HTML
            content_full, html_page = fetch_article_content_with_html(link)
            if not content_full:
                content_full = summary_rss or title

            if not content_full:
                print(f"[WARN] Konten kosong: {title}")
                continue

            # Ambil image
            img_from_rss = extract_image_from_rss(entry)
            img_from_html = extract_image_from_html(html_page)
            image_url = img_from_rss or img_from_html

            # LLM: summary + topic + sentiment
            summary, topic, sentiment = summarize_and_tag(content_full)

            try:
                news_obj = News(
                    source=source["name"],
                    title=title,
                    url=link,
                    content=content_full,
                    published_at=published_at,
                    summary=summary,
                    topic=topic,
                    sentiment=sentiment,
                    image_url=image_url,
                )

                db.add(news_obj)
                db.commit()
                db.refresh(news_obj)

                print(
                    f"[OK] Inserted: {title[:60]}... "
                    f"[topic={topic}] [sentiment={sentiment}] "
                    f"[image={'yes' if image_url else 'no'}]"
                )

            except Exception as e:
                db.rollback()
                print(f"[ERROR] Gagal insert berita {title[:50]} | {e}")

    db.close()


if __name__ == "__main__":
    ingest_from_rss()
