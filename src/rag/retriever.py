"""
src/rag/retriever.py
=====================
Mengambil dokumen relevan dari MongoDB Atlas menggunakan cosine similarity.
"""

from dataclasses import dataclass

import numpy as np
from pymongo import MongoClient
from loguru import logger
from sentence_transformers import SentenceTransformer

from config.settings import settings


@dataclass
class RetrievedDocument:
    """Hasil satu dokumen yang berhasil di-retrieve."""
    doc_id: str
    category: str
    topic: str
    question: str
    answer: str
    similarity_score: float


class CommonInfoRetriever:
    """
    Mengambil dokumen Common Information yang relevan dengan query user
    menggunakan cosine similarity pada vector embeddings.

    Semua embedding dimuat ke memori saat init untuk menghindari
    latensi query ke MongoDB di setiap request.
    """

    def __init__(self) -> None:
        self._embed_model = SentenceTransformer(settings.llm.embedding_model)
        self._documents: list[dict] = []
        self._doc_embeddings: np.ndarray | None = None
        self._load_documents_from_mongodb()

    def _load_documents_from_mongodb(self) -> None:
        """Memuat semua dokumen dan embedding dari MongoDB ke memori."""
        logger.info("Memuat dokumen dari MongoDB Atlas...")

        client = MongoClient(settings.mongo.uri, serverSelectionTimeoutMS=10_000)
        db = client[settings.mongo.db_name]
        collection = db[settings.mongo.collection_name]
        raw_documents = list(collection.find({}, {"_id": 0}))
        client.close()

        if not raw_documents:
            logger.warning("Tidak ada dokumen. Jalankan 'python scripts/store_data.py' dulu.")
            return

        self._documents = raw_documents
        self._doc_embeddings = np.array(
            [doc["embedding"] for doc in raw_documents],
            dtype=np.float32,
        )
        logger.info(f"Berhasil memuat {len(self._documents)} dokumen.")

    def retrieve(self, query: str, top_k: int | None = None) -> list[RetrievedDocument]:
        """
        Mengambil dokumen paling relevan untuk query yang diberikan.

        Args:
            query: Pertanyaan dari user
            top_k: Jumlah dokumen yang dikembalikan

        Returns:
            List dokumen terurut dari yang paling relevan
        """
        if self._doc_embeddings is None or len(self._documents) == 0:
            return []

        k = top_k or settings.rag.top_k
        query_embedding = self._embed_model.encode(query, convert_to_numpy=True).astype(np.float32)
        scores = self._compute_cosine_similarity(query_embedding, self._doc_embeddings)
        top_indices = np.argsort(scores)[::-1][:k]

        results = []
        for idx in top_indices:
            score = float(scores[idx])
            if score < settings.rag.similarity_threshold:
                continue
            doc = self._documents[idx]
            results.append(RetrievedDocument(
                doc_id=doc["doc_id"],
                category=doc["category"],
                topic=doc["topic"],
                question=doc["question"],
                answer=doc["answer"],
                similarity_score=score,
            ))

        logger.debug(f"Query: '{query}' → {len(results)} dokumen ditemukan")
        return results

    @staticmethod
    def _compute_cosine_similarity(query_vec: np.ndarray, doc_matrix: np.ndarray) -> np.ndarray:
        """Menghitung cosine similarity antara query dan semua dokumen."""
        query_norm = query_vec / (np.linalg.norm(query_vec) + 1e-10)
        doc_norms = doc_matrix / (np.linalg.norm(doc_matrix, axis=1, keepdims=True) + 1e-10)
        return doc_norms @ query_norm
