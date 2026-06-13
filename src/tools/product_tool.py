"""
src/tools/product_tool.py
==========================
Tool untuk rekomendasi dan informasi produk e-commerce menggunakan Groq LLM.
"""

from groq import Groq
from google.adk.tools import FunctionTool
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings


# Inisialisasi Groq client
_client = Groq(api_key=settings.llm.groq_api_key)

_PRODUCT_SYSTEM_PROMPT = """Kamu adalah asisten rekomendasi produk e-commerce Indonesia.
Tugasmu membantu user menemukan produk yang sesuai kebutuhan dan budget mereka.

PANDUAN:
- Rekomendasikan 2-3 produk spesifik dengan alasan yang jelas
- Sebutkan kisaran harga dalam Rupiah (perkiraan)
- Jelaskan kelebihan dan kekurangan singkat
- Gunakan bahasa Indonesia yang ramah dan mudah dipahami
- Jika ditanya perbandingan, buat poin-poin yang terstruktur
- Sarankan pelanggan untuk mengecek ketersediaan dan harga terbaru di platform"""


@retry(
    stop=stop_after_attempt(settings.agent.max_retries),
    wait=wait_exponential(multiplier=1, min=2, max=10),
)
def get_product_recommendation(query: str, budget: str = "", category: str = "") -> dict:
    """
    Memberikan rekomendasi produk berdasarkan kebutuhan user.

    Args:
        query: Pertanyaan tentang produk dari user
        budget: Budget yang dimiliki user (opsional, contoh: "5 juta")
        category: Kategori produk (opsional, contoh: "elektronik", "fashion")

    Returns:
        Dict dengan keys:
        - recommendation (str): Rekomendasi produk dalam bahasa Indonesia
        - category (str): Kategori produk yang diidentifikasi
    """
    if not query or not query.strip():
        return {"recommendation": "Pertanyaan produk tidak boleh kosong.", "category": "unknown"}

    logger.info(f"[ProductTool] Query: '{query}' | Budget: '{budget}' | Kategori: '{category}'")

    context_parts = [f"Pertanyaan: {query}"]
    if budget:
        context_parts.append(f"Budget: {budget}")
    if category:
        context_parts.append(f"Kategori: {category}")

    prompt = "\n".join(context_parts)

    response = _client.chat.completions.create(
        model=settings.llm.groq_model,
        messages=[
            {"role": "system", "content": _PRODUCT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=700,
    )

    recommendation = response.choices[0].message.content.strip()
    detected_category = _detect_product_category(query, category)

    logger.info(f"[ProductTool] Selesai | Kategori: {detected_category}")
    return {"recommendation": recommendation, "category": detected_category}


def _detect_product_category(query: str, explicit_category: str) -> str:
    """Mendeteksi kategori produk dari query menggunakan keyword matching."""
    if explicit_category:
        return explicit_category.lower()

    query_lower = query.lower()
    category_keywords = {
        "elektronik": ["laptop", "hp", "smartphone", "tablet", "kamera", "headphone", "tv", "monitor"],
        "fashion": ["baju", "sepatu", "tas", "jaket", "celana", "dress", "kaos"],
        "rumah_tangga": ["kulkas", "ac", "mesin cuci", "blender", "rice cooker", "sofa"],
        "olahraga": ["sepeda", "dumbbell", "treadmill", "sepatu lari", "raket"],
        "kecantikan": ["skincare", "makeup", "serum", "moisturizer", "sunscreen"],
    }

    for cat, keywords in category_keywords.items():
        if any(keyword in query_lower for keyword in keywords):
            return cat

    return "umum"


product_tool = FunctionTool(func=get_product_recommendation)
