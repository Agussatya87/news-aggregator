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
📩 1. **Daily Email Digest — Automated HTML Summary Delivery**

<img width="1396" height="627" alt="Image" src="https://github.com/user-attachments/assets/a59e9cd4-5ec1-4c73-bc67-0658a3282ddb" />

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

📰 2.  **RSS Processing Log — ETL + LLM Pipeline Validation**

<img width="1170" height="135" alt="Image" src="https://github.com/user-attachments/assets/7cb6d18d-5bb7-4bee-afde-4e935df79197" />

Gambar ini menunjukkan output log dari backend FastAPI ketika sistem melakukan proses RSS fetching, text extraction, LLM analysis, dan database insertion.
🔍 Alur Teknis yang Direpresentasikan dalam Gambar:
- RSS Feed Fetching, Sistem melakukan GET request ke feed BBC melalui RSS.App.
- Entry Parsing, Total berita yang ditemukan: 25 entries.
- Processing Setiap Artikel
  Langkah-langkah:
  - Ekstraksi title, description, published date, image URL
  - Normalization dan cleaning teks
  - LLM prompt: summarization, topic classification, sentiment detection
  - Duplicate checking melalui checksum
- Database Insertion (PostgreSQL)

⏰ 3. **n8n Workflow — Automated Email Scheduler**

<img width="1918" height="738" alt="Image" src="https://github.com/user-attachments/assets/1f2bf22a-af1e-470a-bdac-4c07d0994dde" />

Ini adalah inti automation dalam project: workflow n8n yang mengirimkan email setiap pagi.
- 🟢 Schedule Trigger
  - Menggunakan cron-style scheduler
  - Berjalan setiap hari pukul 08:00 WITA
  - Memastikan user mendapat briefing pagi secara konsisten
- 🌐 HTTP Request Node
  - Memanggil endpoint FastAPI
  - Mengambil 10 berita terbaru yang sudah diringkas LLM
  - Terintegrasi dengan Docker internal network
- 🟧 Code Node (JavaScript)
  - Mengubah array berita → HTML template
  - Looping setiap berita untuk membentuk email section lengkap (gambar, summary, metadata)
  - Sanitasi HTML untuk menghindari broken formatting
  - Menghasilkan final email body dalam bentuk string
- ✉️ Gmail Send Message
  - Mengirim email menggunakan OAuth Gmail API
  - Subjek email: “Your AI News Digest — {tanggal}”
  - Body email: HTML full format yang dikirimkan ke inbox

🌐 4. **Streamlit Dashboard — Interactive News Exploration UI**

<img width="1918" height="1078" alt="Image" src="https://github.com/user-attachments/assets/638bd956-b530-4786-a90e-76972543e8ba" />

Streamlit Dashboard adalah antarmuka front-end utama yang digunakan user untuk membaca, memfilter, dan menelusuri berita secara visual.
🔍 Komponen Penting pada Dashboard:
- 🎛️ Sidebar Filters
  - Filter category — politics, technology, sports, dll.
  - Number of news — slider untuk memilih jumlah artikel yang ditampilkan
  - Keyword search — pencarian cepat berdasarkan kata kunci
  - Fitur ini memungkinkan user menyesuaikan tampilan sesuai kebutuhan mereka.
- 🖼️ Article Display Panel
  - Gambar utama artikel
  - Metadata lengkap:
    - Sumber
    - Topik Hasil LLM
    - Sentimen
    - Tanggal publikasi
  - Ringkasan AI yang padat
  - Link “Baca di sumber asli”

# 🌟 Conclusion
AI News Aggregator adalah solusi end-to-end yang mengubah proses konsumsi berita dari manual menjadi otomatis. Proyek ini memberikan informasi yang lebih ringkas, relevan, dan mudah dipahami, sekaligus menghemat waktu pengguna dan meningkatkan daya analisis. Sistem ini sangat bermanfaat bagi individu maupun perusahaan yang bergantung pada informasi untuk mengambil keputusan. AI News Aggregator berhasil membuktikan bahwa sistem berbasis LLM dapat digunakan secara efektif untuk mengotomatiskan proses pengumpulan, analisis, dan penyajian informasi dari sumber berita yang tersebar. Dengan mengintegrasikan RSS fetching, LLM summarization, topic & sentiment classification, database storage, automation scheduling, dan dashboard visualisasi, proyek ini menghasilkan sebuah platform yang bekerja secara mandiri, memberikan update berita harian tanpa intervensi manual.
