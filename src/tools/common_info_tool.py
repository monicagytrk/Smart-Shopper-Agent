"""
src/tools/common_info_tool.py
==============================
Tool untuk menjawab pertanyaan umum (FAQ) e-commerce menggunakan RAG.
"""

from google.adk.tools import FunctionTool
from loguru import logger

from src.rag.retriever import CommonInfoRetriever
from src.rag.generator import RAGGenerator
from config.settings import settings


_retriever: CommonInfoRetriever | None = None
_generator: RAGGenerator | None = None


def _get_rag_pipeline() -> tuple[CommonInfoRetriever, RAGGenerator]:
    """Inisialisasi RAG pipeline sekali (lazy singleton)."""
    global _retriever, _generator
    if _retriever is None:
        logger.info("Inisialisasi Common Info RAG pipeline...")
        _retriever = CommonInfoRetriever()
        _generator = RAGGenerator()
        logger.info("RAG pipeline siap.")
    return _retriever, _generator


def retrieve_common_information(query: str) -> dict:
    """
    Mengambil dan menghasilkan jawaban untuk pertanyaan umum e-commerce.

    Cocok untuk pertanyaan tentang pengiriman, pembayaran, refund,
    akun, promo, garansi, dan informasi umum lainnya.

    Args:
        query: Pertanyaan dari user dalam bahasa Indonesia

    Returns:
        Dict dengan keys:
        - answer (str): Jawaban dalam bahasa Indonesia
        - sources (list): Kategori dokumen yang digunakan
        - confidence (float): Skor kemiripan tertinggi (0.0–1.0)
    """
    if not query or not query.strip():
        return {"answer": "Pertanyaan tidak boleh kosong.", "sources": [], "confidence": 0.0}

    logger.info(f"[CommonInfoTool] Query: '{query}'")
    retriever, generator = _get_rag_pipeline()

    retrieved_docs = retriever.retrieve(query, top_k=settings.rag.top_k)
    answer = generator.generate(query, retrieved_docs)
    sources = list({doc.category for doc in retrieved_docs})
    confidence = max((doc.similarity_score for doc in retrieved_docs), default=0.0)

    logger.info(f"[CommonInfoTool] Selesai | Docs: {len(retrieved_docs)} | Confidence: {confidence:.2f}")
    return {"answer": answer, "sources": sources, "confidence": round(confidence, 3)}


common_info_tool = FunctionTool(func=retrieve_common_information)
