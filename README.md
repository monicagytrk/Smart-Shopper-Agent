🛒 Smart Shopper Agent

AI Agent customer service untuk platform e-commerce Indonesia, dibangun menggunakan Google ADK, Groq LLM, MongoDB Atlas, dan Streamlit.


🤖 Fitur


Routing otomatis — Agent menentukan tools yang tepat berdasarkan jenis pertanyaan
Common Info Tool — Menjawab pertanyaan umum (pengiriman, refund, pembayaran, promo, garansi) menggunakan RAG
Product Tool — Memberikan rekomendasi dan perbandingan produk menggunakan Groq LLM
Chat UI — Antarmuka chat berbasis Streamlit


🗂️ Struktur Proyek

ecommerce-v2/
├── app.py                          # Streamlit UI
├── config/
│   └── settings.py                 # Konfigurasi terpusat
├── src/
│   ├── agent/ecommerce_agent.py    # AI Agent & routing
│   ├── tools/
│   │   ├── common_info_tool.py     # Tool pertanyaan umum (RAG)
│   │   └── product_tool.py         # Tool rekomendasi produk
│   ├── rag/
│   │   ├── retriever.py            # Cosine similarity search
│   │   └── generator.py            # Response generation
│   └── data/
│       └── common_info_dataset.py  # Dataset FAQ e-commerce
├── scripts/
│   └── store_data.py               # Storing data ke MongoDB Atlas
├── requirements.txt
└── .env.example

