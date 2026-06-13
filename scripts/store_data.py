"""
scripts/store_data.py
======================
Script untuk menyimpan dataset Common Information ke MongoDB Atlas.

Menjalankan script ini:
    python scripts/store_data.py

Proses yang dilakukan:
1. Load dataset dari src/data/common_info_dataset.py
2. Generate vector embedding untuk setiap dokumen
3. Simpan dokumen + embedding ke MongoDB Atlas
4. Buat index untuk pencarian yang efisien

Strategi Penyimpanan:
    Lihat docs/storage_strategy.md untuk penjelasan lengkap.
"""

import sys
import os
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient, UpdateOne
from pymongo.collection import Collection
from sentence_transformers import SentenceTransformer
from loguru import logger

from config.settings import settings
from src.data.common_info_dataset import get_all_entries, CommonInfoEntry


logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    level=settings.agent.log_level,
)


def build_embedding_text(entry: CommonInfoEntry) -> str:
    """
    Menggabungkan teks dari beberapa field untuk menghasilkan embedding
    yang kaya konteks.

    Menggabungkan question + keywords memberikan representasi vektor
    yang lebih akurat dibanding hanya menggunakan question saja.

    Args:
        entry: Satu entri dari common information dataset

    Returns:
        String gabungan yang akan di-embed
    """
    keywords_str = " ".join(entry["keywords"])
    return f"{entry['question']} {keywords_str}"


def build_document(entry: CommonInfoEntry, embedding: list[float]) -> dict:
    """
    Membangun dokumen MongoDB dari satu entri dataset + embedding-nya.

    Args:
        entry: Data common information
        embedding: Vector float hasil embedding model

    Returns:
        Dokumen siap simpan ke MongoDB
    """
    return {
        # Identifikasi unik berdasarkan kategori + topic
        "doc_id": f"{entry['category']}_{entry['topic']}",

        # Metadata untuk filtering dan display
        "category": entry["category"],
        "topic": entry["topic"],
        "keywords": entry["keywords"],

        # Konten utama
        "question": entry["question"],
        "answer": entry["answer"],

        # Vector embedding untuk similarity search
        "embedding": embedding,

        # Metadata teknis
        "updated_at": datetime.now(timezone.utc),
    }


def ensure_indexes(collection: Collection) -> None:
    """
    Membuat index MongoDB untuk performa pencarian optimal.

    Index yang dibuat:
    - category (ascending): untuk filter berdasarkan kategori
    - doc_id (unique): mencegah duplikasi data

    Args:
        collection: MongoDB collection object
    """
    collection.create_index("category")
    collection.create_index("doc_id", unique=True)
    logger.info("Index MongoDB berhasil dibuat/diverifikasi.")


def upsert_documents(collection: Collection, documents: list[dict]) -> dict:
    """
    Menyimpan dokumen ke MongoDB dengan strategi upsert.

    Upsert = Update jika doc_id sudah ada, Insert jika belum.
    Ini memastikan script bisa dijalankan ulang tanpa duplikasi data.

    Args:
        collection: MongoDB collection object
        documents: List dokumen yang akan disimpan

    Returns:
        Ringkasan hasil operasi (inserted, modified, total)
    """
    operations = [
        UpdateOne(
            filter={"doc_id": doc["doc_id"]},
            update={"$set": doc},
            upsert=True,
        )
        for doc in documents
    ]

    result = collection.bulk_write(operations, ordered=False)

    return {
        "inserted": result.upserted_count,
        "modified": result.modified_count,
        "total_processed": len(documents),
    }


def store_common_info_to_mongodb() -> None:
    """
    Pipeline utama: Load → Embed → Store ke MongoDB Atlas.

    Alur:
    1. Load semua entri dari dataset
    2. Inisialisasi embedding model (CPU-only, ~80MB)
    3. Generate embedding untuk setiap entri
    4. Simpan ke MongoDB dengan strategi upsert
    5. Buat index untuk pencarian efisien
    """
    logger.info("=" * 50)
    logger.info("Mulai proses storing data ke MongoDB Atlas")
    logger.info("=" * 50)

    # Step 1: Load dataset
    dataset = get_all_entries()
    logger.info(f"Dataset dimuat: {len(dataset)} entri dari {len(set(e['category'] for e in dataset))} kategori")

    # Step 2: Inisialisasi embedding model
    # all-MiniLM-L6-v2 dipilih karena:
    # - Ukuran kecil (~80MB, berjalan baik di RAM 3GB)
    # - Performa baik untuk semantic similarity
    # - Tidak memerlukan GPU
    logger.info(f"Loading embedding model: {settings.llm.embedding_model}")
    embed_model = SentenceTransformer(settings.llm.embedding_model)
    logger.info("Embedding model berhasil dimuat.")

    # Step 3: Generate embeddings secara batch (lebih efisien dari 1-per-1)
    logger.info("Generating embeddings untuk semua entri...")
    texts_to_embed = [build_embedding_text(entry) for entry in dataset]
    embeddings = embed_model.encode(
        texts_to_embed,
        batch_size=16,          # Batch kecil agar hemat RAM
        show_progress_bar=True,
        convert_to_numpy=True,
    )
    logger.info(f"Embedding selesai. Dimensi vector: {embeddings.shape[1]}")

    # Step 4: Bangun dokumen MongoDB
    documents = [
        build_document(entry, embedding.tolist())
        for entry, embedding in zip(dataset, embeddings)
    ]

    # Step 5: Simpan ke MongoDB Atlas
    logger.info("Menghubungkan ke MongoDB Atlas...")
    client = MongoClient(settings.mongo.uri, serverSelectionTimeoutMS=10_000)

    # Verifikasi koneksi
    client.admin.command("ping")
    logger.info("Koneksi MongoDB Atlas berhasil.")

    db = client[settings.mongo.db_name]
    collection = db[settings.mongo.collection_name]

    # Step 6: Buat index
    ensure_indexes(collection)

    # Step 7: Simpan dokumen (upsert)
    logger.info(f"Menyimpan {len(documents)} dokumen...")
    summary = upsert_documents(collection, documents)

    client.close()

    # Laporan hasil
    logger.info("=" * 50)
    logger.success("Proses storing selesai!")
    logger.info(f"  Dokumen baru       : {summary['inserted']}")
    logger.info(f"  Dokumen diperbarui : {summary['modified']}")
    logger.info(f"  Total diproses     : {summary['total_processed']}")
    logger.info(f"  Database           : {settings.mongo.db_name}")
    logger.info(f"  Collection         : {settings.mongo.collection_name}")
    logger.info("=" * 50)


if __name__ == "__main__":
    store_common_info_to_mongodb()
