"""
src/agent/ecommerce_agent.py
=============================
AI Agent utama untuk e-commerce menggunakan Google ADK.
Routing otomatis: pertanyaan umum → common_info_tool, produk → product_tool.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent
from loguru import logger

from config.settings import settings
from src.tools.common_info_tool import common_info_tool
from src.tools.product_tool import product_tool


AGENT_INSTRUCTION = """Kamu adalah AI Agent customer service untuk platform e-commerce Indonesia.
Tugasmu adalah membantu pelanggan dengan ramah, cepat, dan akurat.

## KEMAMPUANMU

### 1. retrieve_common_information
Gunakan untuk pertanyaan UMUM:
- Pengiriman: estimasi waktu, lacak paket, ongkir
- Pembayaran: metode, batas waktu, gagal bayar
- Refund/Return: cara refund, syarat pengembalian
- Akun: lupa password, akun diretas
- Promo: cara pakai voucher, voucher tidak berlaku
- Garansi produk
- Cara hubungi customer service

### 2. get_product_recommendation
Gunakan untuk pertanyaan PRODUK:
- Rekomendasi produk sesuai budget
- Perbandingan dua produk
- Spesifikasi produk tertentu
- Produk terbaik dalam kategori tertentu

## PANDUAN
- WAJIB gunakan tools, jangan jawab dari pengetahuan sendiri
- Pertanyaan campuran → panggil kedua tools
- Bahasa Indonesia yang ramah dan profesional
- Gunakan emoji secukupnya 😊"""


def create_ecommerce_agent() -> Agent:
    """Membuat dan mengkonfigurasi AI Agent e-commerce."""
    agent = Agent(
        name="ecommerce_cs_agent",
        model=f"groq/{settings.llm.groq_model}",
        description="AI Agent customer service e-commerce Indonesia.",
        instruction=AGENT_INSTRUCTION,
        tools=[common_info_tool, product_tool],
    )
    logger.info(f"Agent '{agent.name}' siap | Model: {settings.llm.groq_model}")
    return agent


async def create_runner_and_session() -> tuple[InMemoryRunner, object]:
    """Membuat runner dan session baru untuk satu percakapan."""
    agent = create_ecommerce_agent()
    runner = InMemoryRunner(agent=agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="user",
    )
    return runner, session


async def ask_agent(runner: InMemoryRunner, session: object, query: str) -> str:
    """
    Mengirim pertanyaan ke agent dan mengembalikan jawaban final.

    Args:
        runner: InMemoryRunner yang sudah diinisialisasi
        session: Session aktif percakapan
        query: Pertanyaan dari user

    Returns:
        Jawaban agent dalam bentuk string
    """
    message = UserContent(parts=[Part(text=query)])

    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            return event.content.parts[0].text

    return "Maaf, tidak ada respons dari agent. Silakan coba lagi."
