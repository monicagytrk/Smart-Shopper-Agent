"""
src/rag/generator.py
=====================
Menghasilkan jawaban kontekstual menggunakan Groq LLM
berdasarkan dokumen yang di-retrieve dari MongoDB.
"""

from groq import Groq
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings
from src.rag.retriever import RetrievedDocument


# Inisialisasi Groq client
_client = Groq(api_key=settings.llm.groq_api_key)


class RAGGenerator:
    """
    Menghasilkan jawaban kontekstual menggunakan Groq LLM
    dengan dokumen relevan sebagai konteks.
    """

    _SYSTEM_PROMPT = """Kamu adalah customer service AI untuk platform e-commerce Indonesia.
Tugasmu adalah menjawab pertanyaan pelanggan berdasarkan informasi yang tersedia.

PANDUAN MENJAWAB:
- Gunakan bahasa Indonesia yang ramah, jelas, dan mudah dipahami
- Jawab hanya berdasarkan konteks yang diberikan
- Jika informasi tidak tersedia dalam konteks, katakan dengan jujur
- Struktur jawaban dengan bullet point jika ada beberapa poin
- Selalu akhiri dengan tawaran bantuan lebih lanjut jika relevan
- Jangan mengarang informasi yang tidak ada di konteks"""

    @retry(
        stop=stop_after_attempt(settings.agent.max_retries),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def generate(self, query: str, retrieved_docs: list[RetrievedDocument]) -> str:
        """
        Menghasilkan jawaban berdasarkan query dan dokumen relevan.

        Args:
            query: Pertanyaan asli dari user
            retrieved_docs: Dokumen relevan hasil retrieval

        Returns:
            Jawaban dalam bahasa Indonesia
        """
        if not retrieved_docs:
            return self._fallback_response(query)

        prompt = self._build_prompt(query, retrieved_docs)
        logger.debug(f"Generating response untuk query: '{query}'")

        response = _client.chat.completions.create(
            model=settings.llm.groq_model,
            messages=[
                {"role": "system", "content": self._SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=settings.llm.temperature,
            max_tokens=600,
        )

        answer = response.choices[0].message.content.strip()
        logger.debug(f"Response dihasilkan ({len(answer)} karakter)")
        return answer

    def _build_prompt(self, query: str, docs: list[RetrievedDocument]) -> str:
        """Membangun prompt terstruktur dari query dan dokumen relevan."""
        context_sections = []
        for i, doc in enumerate(docs, start=1):
            section = (
                f"[Dokumen {i} | Kategori: {doc.category} | Topik: {doc.topic}]\n"
                f"Pertanyaan Serupa: {doc.question}\n"
                f"Jawaban: {doc.answer}"
            )
            context_sections.append(section)

        context_block = "\n\n".join(context_sections)
        return (
            f"KONTEKS INFORMASI:\n{context_block}\n\n"
            f"PERTANYAAN PELANGGAN:\n{query}\n\n"
            f"Berikan jawaban yang membantu berdasarkan konteks di atas."
        )

    @staticmethod
    def _fallback_response(query: str) -> str:
        """Jawaban default ketika tidak ada dokumen relevan ditemukan."""
        logger.warning(f"Tidak ada konteks relevan untuk query: '{query}'")
        return (
            "Maaf, saya tidak menemukan informasi yang relevan untuk pertanyaan Anda. "
            "Untuk bantuan lebih lanjut:\n"
            "• Live Chat: 07.00–22.00 WIB\n"
            "• Email: support@toko.com\n"
            "• WhatsApp: +62 812-XXXX-XXXX\n\n"
            "Apakah ada hal lain yang bisa saya bantu?"
        )
