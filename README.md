# AI News Aggregator

AI-powered system that ingests trusted RSS feeds, scrapes full articles, summarizes them with an on-prem LLM (Ollama), classifies topic & sentiment, and serves the curated feed through a FastAPI backend and Streamlit dashboard.

## 📌 Project Overview
AI News Aggregator adalah platform end-to-end yang mengotomatiskan pengambilan berita, menganalisis konten menggunakan Large Language Models (LLM), menyimpan hasilnya dalam database PostgreSQL, menampilkannya melalui dashboard interaktif, dan mengirimkan ringkasan berita terbaru setiap pagi ke email pengguna.

## 🚀 Key Features
1. **RSS Ingestion & Intelligent News Processing**
- Mengambil berita dari RSS feed (contoh: BBC News)
- Ekstraksi metadata: judul, waktu, gambar, link, deskripsi
- Deteksi duplikasi dan validasi sumber

2. **AI-Powered LLM Pipeline**
- Summarization – ringkas artikel menjadi 3–5 kalimat
- Topic Classification – politics, technology, sports, dll.
- Sentiment Analysis – positive, neutral, negative
- Image context awareness untuk artikelnya

3. **PostgreSQL Storage**
- Menyimpan ringkasan, metadata, kategori, sentimen, dan image URL
- Optimized indexing untuk query cepat

4. **FastAPI Backend**
- Endpoint untuk fetch berita terbaru
- Endpoint filter berdasarkan kategori, keyword, sentimen
- Digunakan oleh dashboard & n8n automation

5. **Streamlit Web Dashboard**
- UI interaktif untuk menelusuri berita AI
- Filter berdasarkan kategori, jumlah berita, keyword
- Tampilan bersih bergaya modern (dark theme)

6. **Automated Email Digest (08:00 AM)**
- n8n Schedule Trigger → Fetch API → Format HTML → Send Gmail
- Email berisi ringkasan AI + gambar + link ke artikel asli
- Semua dilakukan otomatis setiap pagi

## Result
1. **📩 1. Daily Email Digest — Automated HTML Summary Delivery**

Gambar ini menunjukkan email harian otomatis yang dikirimkan oleh sistem AI News Aggregator setiap pukul 08:00 WITA melalui workflow n8n.
**🔍 Komponen yang Terlihat dalam Email:**
- Hero Image (Gambar Berita Utama) Diambil langsung dari metadata RSS feed untuk meningkatkan engagement visual.
- Metadata Lanjutan
  - Source: BBC News
  - Topic Classification: technology
  - Sentiment Score: neutral
  - Semua metadata ini berasal dari LLM pipeline yang melakukan klasifikasi topik dan sentiment analysis secara otomatis.
- AI Summary Ringkasan 3–5 kalimat yang dihasilkan LLM. Dirancang untuk menghindari informasi redundant, menangkap konteks berita, dan mudah dibaca dalam waktu < 10 detik
- CTA Button — “Read Full Article” Mengarahkan user ke sumber asli menggunakan URL valid dari RSS.
