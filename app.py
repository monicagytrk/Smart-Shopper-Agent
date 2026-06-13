"""
app.py
=======
Streamlit UI untuk E-Commerce AI Agent.

Menjalankan:
    streamlit run app.py
"""

import asyncio
import sys
import os

import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agent.ecommerce_agent import create_runner_and_session, ask_agent


# ── Konfigurasi Halaman ───────────────────────────────────────────────────────

st.set_page_config(
    page_title="E-Commerce AI Agent",
    page_icon="🛒",
    layout="centered",
)


# ── Custom CSS ────────────────────────────────────────────────────────────────

def inject_custom_css() -> None:
    """Menyuntikkan CSS kustom untuk tampilan chat bubble."""
    st.markdown("""
    <style>
        /* ── Header ── */
        .main-header {
            text-align: center;
            padding: 1.5rem 0 0.5rem 0;
            border-bottom: 2px solid #e0e0e0;
            margin-bottom: 1.5rem;
        }
        .main-header h1 {
            font-size: 2rem;
            font-weight: 700;
            color: #1a1a2e;
            margin: 0;
        }
        .main-header p {
            color: #666;
            font-size: 0.9rem;
            margin: 0.3rem 0 0 0;
        }

        /* ── Sembunyikan avatar default Streamlit ── */
        [data-testid="chatAvatarIcon-assistant"],
        [data-testid="chatAvatarIcon-user"] {
            display: none !important;
        }

        /* ── Bubble agent (kiri, gelap) ── */
        [data-testid="chatMessage-assistant"] {
            background-color: #1a1a2e !important;
            border-radius: 0 16px 16px 16px !important;
            padding: 1rem 1.2rem !important;
            margin: 0.5rem 3rem 0.5rem 0 !important;
            color: #ffffff !important;
        }
        [data-testid="chatMessage-assistant"] p,
        [data-testid="chatMessage-assistant"] li,
        [data-testid="chatMessage-assistant"] ul {
            color: #ffffff !important;
        }

        /* ── Bubble user (kanan, ungu) ── */
        [data-testid="chatMessage-user"] {
            background-color: #4a4a8a !important;
            border-radius: 16px 0 16px 16px !important;
            padding: 1rem 1.2rem !important;
            margin: 0.5rem 0 0.5rem 3rem !important;
            color: #ffffff !important;
            text-align: right !important;
        }
        [data-testid="chatMessage-user"] p {
            color: #ffffff !important;
            text-align: right !important;
        }

        /* ── Input area ── */
        [data-testid="stChatInput"] {
            border-radius: 24px !important;
            border: 1.5px solid #4a4a8a !important;
        }
    </style>
    """, unsafe_allow_html=True)


# ── Helper: Jalankan async dari Streamlit ────────────────────────────────────

def run_async(coro):
    """Menjalankan coroutine async dari konteks synchronous Streamlit."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, coro)
                return future.result()
        return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


# ── Session State ─────────────────────────────────────────────────────────────

def init_session() -> None:
    """Inisialisasi runner, session ADK, dan riwayat chat."""
    if "agent_ready" not in st.session_state:
        with st.spinner("Memuat AI Agent..."):
            runner, session = run_async(create_runner_and_session())
            st.session_state.runner = runner
            st.session_state.session = session
            st.session_state.agent_ready = True

    if "messages" not in st.session_state:
        st.session_state.messages = []


def reset_session() -> None:
    """Menghapus riwayat chat dan membuat session agent baru."""
    for key in ["runner", "session", "agent_ready", "messages"]:
        st.session_state.pop(key, None)


# ── Komponen UI ───────────────────────────────────────────────────────────────

def render_header() -> None:
    """Render header halaman."""
    st.markdown("""
        <div class="main-header">
            <h1>🛒 E-Commerce AI Agent</h1>
            <p>Customer Service berbasis AI • Powered by Groq LLM &amp; RAG</p>
        </div>
    """, unsafe_allow_html=True)


def render_sidebar() -> None:
    """Render sidebar dengan contoh pertanyaan dan tombol reset."""
    with st.sidebar:
        st.header("💡 Contoh Pertanyaan")

        example_questions = [
            "Berapa lama pengiriman ke Bandung?",
            "Bagaimana cara refund produk?",
            "Metode pembayaran apa saja?",
            "Rekomendasikan laptop budget 5 juta",
            "iPhone 13 vs Samsung Z Flip 7?",
            "Cara pakai voucher diskon?",
            "Kenapa voucher saya tidak berlaku?",
            "Garansi produk elektronik berapa lama?",
        ]

        for question in example_questions:
            if st.button(question, use_container_width=True, type="secondary"):
                st.session_state.example_input = question

        st.divider()

        if st.button("🔄 Reset Percakapan", use_container_width=True, type="primary"):
            reset_session()
            st.rerun()


def render_chat_history() -> None:
    """Render seluruh riwayat percakapan."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input(user_input: str) -> None:
    """
    Memproses input user: tampilkan bubble, kirim ke agent, tampilkan respons.

    Args:
        user_input: Teks pertanyaan dari user
    """
    if not user_input.strip():
        return

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Agent sedang memproses..."):
            try:
                response = run_async(
                    ask_agent(
                        runner=st.session_state.runner,
                        session=st.session_state.session,
                        query=user_input,
                    )
                )
            except Exception as e:
                response = f"❌ Terjadi kesalahan: {e}\n\nSilakan coba lagi."
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


# ── Main App ──────────────────────────────────────────────────────────────────

def main() -> None:
    """Entry point utama Streamlit app."""
    inject_custom_css()
    init_session()
    render_header()
    render_sidebar()

    # Pesan selamat datang
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown(
                "Halo! 👋 Saya adalah AI Agent customer service toko online Anda.\n\n"
                "Saya bisa membantu Anda dengan:\n"
                "- 📦 Pertanyaan seputar **pengiriman, pembayaran, refund, dan promo**\n"
                "- 🛍️ **Rekomendasi produk** sesuai kebutuhan dan budget Anda\n\n"
                "Silakan ketik pertanyaan Anda di bawah, atau pilih contoh di sidebar! 😊"
            )

    render_chat_history()

    # Handle klik contoh pertanyaan dari sidebar
    if "example_input" in st.session_state:
        example = st.session_state.pop("example_input")
        handle_user_input(example)
        st.rerun()

    # Input chat utama
    if user_input := st.chat_input("Ketik pertanyaan Anda di sini..."):
        handle_user_input(user_input)


if __name__ == "__main__":
    main()
