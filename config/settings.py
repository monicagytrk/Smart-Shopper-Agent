"""
config/settings.py
==================
Konfigurasi terpusat untuk seluruh aplikasi.
Semua nilai dibaca dari environment variables (.env).
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class MongoConfig:
    """Konfigurasi koneksi MongoDB Atlas."""
    uri: str
    db_name: str
    collection_name: str = "common_information"

    @classmethod
    def from_env(cls) -> "MongoConfig":
        uri = os.getenv("MONGODB_URI")
        if not uri:
            raise EnvironmentError("MONGODB_URI tidak ditemukan di .env")
        return cls(uri=uri, db_name=os.getenv("MONGODB_DB_NAME", "ecommerce_agent"))


@dataclass(frozen=True)
class LLMConfig:
    """Konfigurasi model bahasa (Groq) dan embedding."""
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    embedding_model: str = "all-MiniLM-L6-v2"
    temperature: float = 0.3

    @classmethod
    def from_env(cls) -> "LLMConfig":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY tidak ditemukan di .env")
        return cls(
            groq_api_key=api_key,
            groq_model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            embedding_model=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
            temperature=float(os.getenv("AGENT_TEMPERATURE", "0.3")),
        )


@dataclass(frozen=True)
class RAGConfig:
    """Konfigurasi pipeline RAG."""
    top_k: int = 3
    similarity_threshold: float = 0.5

    @classmethod
    def from_env(cls) -> "RAGConfig":
        return cls(
            top_k=int(os.getenv("RAG_TOP_K", "3")),
            similarity_threshold=float(os.getenv("RAG_SIMILARITY_THRESHOLD", "0.5")),
        )


@dataclass(frozen=True)
class AgentConfig:
    """Konfigurasi AI Agent."""
    max_retries: int = 3
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "AgentConfig":
        return cls(
            max_retries=int(os.getenv("AGENT_MAX_RETRIES", "3")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )


class Settings:
    """Accessor tunggal untuk semua konfigurasi aplikasi."""

    def __init__(self) -> None:
        self.mongo = MongoConfig.from_env()
        self.llm = LLMConfig.from_env()
        self.rag = RAGConfig.from_env()
        self.agent = AgentConfig.from_env()


settings = Settings()
