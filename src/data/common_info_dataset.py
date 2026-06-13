"""
src/data/common_info_dataset.py
================================
Dataset Common Information untuk e-commerce Indonesia.

Setiap entri memiliki:
- category  : kategori topik (digunakan untuk filtering)
- topic     : sub-topik spesifik
- question  : contoh pertanyaan user (membantu similarity search)
- answer    : jawaban lengkap dan akurat
- keywords  : kata kunci untuk retrieval tambahan

Dataset ini dibuat berdasarkan pertanyaan umum yang sering muncul
pada platform e-commerce Indonesia (Tokopedia, Shopee, Lazada style).
"""

from typing import TypedDict


class CommonInfoEntry(TypedDict):
    """Schema satu entri common information."""
    category: str
    topic: str
    question: str
    answer: str
    keywords: list[str]


# ── Dataset ───────────────────────────────────────────────────────────────────

COMMON_INFO_DATASET: list[CommonInfoEntry] = [

    # ── PENGIRIMAN ────────────────────────────────────────────────────────────

    {
        "category": "pengiriman",
        "topic": "estimasi_waktu_pengiriman",
        "question": "Berapa lama waktu pengiriman ke kota saya?",
        "answer": (
            "Estimasi waktu pengiriman tergantung lokasi tujuan dan kurir yang dipilih:\n"
            "• Same Day / Instant: 2–8 jam (hanya area kota tertentu)\n"
            "• Reguler (JNE REG, J&T, SiCepat): 1–3 hari kerja (Jawa), "
            "3–7 hari kerja (luar Jawa)\n"
            "• Kargo / Trucking: 7–14 hari kerja (luar Jawa / daerah terpencil)\n"
            "Hari kerja tidak termasuk Sabtu, Minggu, dan hari libur nasional. "
            "Kamu bisa cek estimasi lebih akurat di halaman checkout sebelum pembayaran."
        ),
        "keywords": ["pengiriman", "lama", "hari", "estimasi", "sampai", "kurir", "ekspedisi"],
    },
    {
        "category": "pengiriman",
        "topic": "ongkos_kirim",
        "question": "Apakah ada gratis ongkir?",
        "answer": (
            "Ya, tersedia beberapa cara untuk mendapatkan gratis ongkos kirim:\n"
            "1. Voucher Gratis Ongkir: Klaim di halaman Promo & Voucher setiap hari\n"
            "2. Minimum Pembelian: Gratis ongkir untuk pembelian di atas Rp 50.000 "
            "dengan kurir tertentu\n"
            "3. Program Member: Member Gold & Platinum mendapat kuota gratis ongkir "
            "hingga 10x per bulan\n"
            "4. Flash Sale Ongkir: Setiap Senin dan Jumat pukul 00.00–23.59\n"
            "Cek halaman Promo untuk voucher gratis ongkir yang sedang aktif."
        ),
        "keywords": ["gratis ongkir", "ongkos kirim", "biaya kirim", "bebas ongkir", "promo"],
    },
    {
        "category": "pengiriman",
        "topic": "lacak_paket",
        "question": "Bagaimana cara melacak status pengiriman paket saya?",
        "answer": (
            "Ada 3 cara untuk melacak paket:\n"
            "1. Aplikasi/Website: Masuk ke akun → Menu 'Pesanan Saya' → Klik nomor pesanan "
            "→ Tombol 'Lacak Paket'\n"
            "2. Nomor Resi: Masuk ke website resmi kurir (JNE, J&T, SiCepat, dll) dan "
            "masukkan nomor resi\n"
            "3. Notifikasi: Aktifkan notifikasi aplikasi untuk update otomatis setiap "
            "perubahan status pengiriman\n"
            "Nomor resi biasanya tersedia 1×24 jam setelah penjual mengkonfirmasi pengiriman."
        ),
        "keywords": ["lacak", "tracking", "resi", "status", "paket", "cek kiriman"],
    },
    {
        "category": "pengiriman",
        "topic": "paket_hilang_rusak",
        "question": "Paket saya hilang atau rusak saat pengiriman, apa yang harus dilakukan?",
        "answer": (
            "Jika paket hilang atau rusak:\n"
            "1. Dokumentasikan: Foto/video kondisi paket atau bukti tidak sampai\n"
            "2. Hubungi Penjual: Ajukan komplain melalui fitur 'Chat Penjual' dalam 2×24 jam "
            "setelah status 'Terkirim'\n"
            "3. Ajukan Komplain Resmi: Masuk ke Pesanan Saya → Klik 'Ajukan Komplain' → "
            "Upload bukti → Pilih solusi (refund/kirim ulang)\n"
            "4. Proteksi Pengiriman: Jika kamu mengaktifkan asuransi pengiriman, klaim "
            "akan diproses dalam 3–7 hari kerja\n"
            "Tim Customer Service kami siap membantu 24/7 melalui live chat."
        ),
        "keywords": ["hilang", "rusak", "paket tidak sampai", "komplain", "klaim", "asuransi pengiriman"],
    },

    # ── PEMBAYARAN ────────────────────────────────────────────────────────────

    {
        "category": "pembayaran",
        "topic": "metode_pembayaran",
        "question": "Metode pembayaran apa saja yang tersedia?",
        "answer": (
            "Kami menyediakan berbagai metode pembayaran:\n"
            "Transfer Bank:\n"
            "• BCA, Mandiri, BNI, BRI, CIMB Niaga (Virtual Account)\n"
            "Dompet Digital:\n"
            "• GoPay, OVO, DANA, ShopeePay, LinkAja\n"
            "Kartu:\n"
            "• Kartu Kredit/Debit Visa, Mastercard, JCB\n"
            "Paylater:\n"
            "• Kredivo, Akulaku, Shopee PayLater\n"
            "Minimarket:\n"
            "• Alfamart, Indomaret (bayar tunai dengan kode pembayaran)\n"
            "COD (Cash on Delivery) tersedia di kota-kota tertentu."
        ),
        "keywords": ["pembayaran", "bayar", "transfer", "kartu kredit", "gopay", "ovo", "dana", "cod"],
    },
    {
        "category": "pembayaran",
        "topic": "batas_waktu_pembayaran",
        "question": "Berapa lama batas waktu pembayaran setelah checkout?",
        "answer": (
            "Batas waktu pembayaran berbeda berdasarkan metode:\n"
            "• Transfer Bank / Virtual Account: 1×24 jam\n"
            "• Minimarket (Alfamart/Indomaret): 1×24 jam\n"
            "• GoPay / OVO / DANA: 15 menit\n"
            "• Kartu Kredit/Debit: 15 menit\n"
            "Jika melewati batas waktu, pesanan otomatis dibatalkan dan kamu perlu "
            "membuat pesanan baru. "
            "Stok produk akan dikembalikan ke sistem setelah pembatalan otomatis."
        ),
        "keywords": ["batas waktu", "expired", "kadaluarsa", "lupa bayar", "deadline pembayaran"],
    },
    {
        "category": "pembayaran",
        "topic": "pembayaran_gagal",
        "question": "Kenapa pembayaran saya gagal atau ditolak?",
        "answer": (
            "Pembayaran gagal bisa disebabkan beberapa hal:\n"
            "1. Saldo tidak cukup di dompet digital atau rekening bank\n"
            "2. Limit kartu kredit/debit terlampaui\n"
            "3. Koneksi internet terputus saat proses pembayaran\n"
            "4. Kartu kredit diblokir oleh bank untuk transaksi online\n"
            "5. Batas waktu pembayaran terlampaui\n\n"
            "Solusi: Coba metode pembayaran lain, pastikan saldo mencukupi, "
            "atau hubungi bank penerbit kartu untuk mengaktifkan transaksi online. "
            "Pesanan tidak akan dibatalkan selama masih dalam batas waktu pembayaran."
        ),
        "keywords": ["gagal bayar", "ditolak", "payment failed", "error pembayaran", "tidak bisa bayar"],
    },

    # ── REFUND & PENGEMBALIAN ─────────────────────────────────────────────────

    {
        "category": "refund",
        "topic": "prosedur_refund",
        "question": "Bagaimana cara mengajukan refund atau pengembalian dana?",
        "answer": (
            "Langkah mengajukan refund:\n"
            "1. Masuk ke 'Pesanan Saya' → Pilih pesanan yang ingin direfund\n"
            "2. Klik 'Ajukan Komplain' atau 'Minta Refund'\n"
            "3. Pilih alasan: Produk tidak sesuai / cacat / tidak sampai\n"
            "4. Upload foto/video bukti sebagai lampiran\n"
            "5. Pilih solusi: Refund dana atau kirim produk pengganti\n"
            "6. Tunggu respons penjual (maks. 3×24 jam)\n"
            "7. Jika tidak ada respons, sistem otomatis meneruskan ke tim mediasi\n\n"
            "Dana refund dikembalikan ke metode pembayaran asal dalam 1–5 hari kerja "
            "setelah persetujuan."
        ),
        "keywords": ["refund", "kembalikan dana", "pengembalian", "komplain", "retur", "cancel"],
    },
    {
        "category": "refund",
        "topic": "syarat_return",
        "question": "Produk apa saja yang bisa dikembalikan?",
        "answer": (
            "Produk dapat dikembalikan jika:\n"
            "✅ Kondisi yang memenuhi syarat:\n"
            "• Produk cacat atau rusak saat diterima\n"
            "• Produk tidak sesuai deskripsi/gambar toko\n"
            "• Produk salah warna, ukuran, atau tipe\n"
            "• Produk palsu atau tidak original\n"
            "• Produk tidak lengkap (ada aksesoris yang hilang)\n\n"
            "❌ Produk yang TIDAK bisa dikembalikan:\n"
            "• Produk digital (voucher, software, game)\n"
            "• Produk intimate/underwear demi alasan higienitas\n"
            "• Produk yang sudah digunakan dan kerusakannya disebabkan pengguna\n"
            "• Makanan dan minuman segar\n\n"
            "Pengajuan return harus dilakukan dalam 2×24 jam setelah paket diterima."
        ),
        "keywords": ["syarat return", "bisa dikembalikan", "retur", "produk cacat", "tidak sesuai"],
    },
    {
        "category": "refund",
        "topic": "lama_refund",
        "question": "Berapa lama dana refund masuk ke rekening saya?",
        "answer": (
            "Estimasi waktu refund berdasarkan metode pembayaran asal:\n"
            "• GoPay / OVO / DANA / ShopeePay: 1–3 hari kerja\n"
            "• Transfer Bank (Virtual Account): 2–5 hari kerja\n"
            "• Kartu Kredit: 7–14 hari kerja (tergantung kebijakan bank)\n"
            "• Kartu Debit: 3–7 hari kerja\n"
            "• Minimarket (Alfamart/Indomaret): Dana dikembalikan ke saldo toko "
            "untuk digunakan pada transaksi berikutnya\n\n"
            "Hitungan hari dimulai sejak penjual menyetujui permintaan refund."
        ),
        "keywords": ["lama refund", "kapan dana masuk", "proses refund", "estimasi refund"],
    },

    # ── AKUN & KEAMANAN ───────────────────────────────────────────────────────

    {
        "category": "akun",
        "topic": "lupa_password",
        "question": "Saya lupa password, bagaimana cara reset?",
        "answer": (
            "Cara reset password:\n"
            "1. Klik 'Lupa Password' di halaman login\n"
            "2. Masukkan email atau nomor HP terdaftar\n"
            "3. Pilih metode verifikasi: Email atau SMS OTP\n"
            "4. Masukkan kode OTP yang diterima (berlaku 5 menit)\n"
            "5. Buat password baru (minimal 8 karakter, kombinasi huruf & angka)\n"
            "6. Konfirmasi password baru → Selesai\n\n"
            "Jika tidak menerima OTP setelah 2 menit, klik 'Kirim Ulang'. "
            "Pastikan nomor HP masih aktif dan email tidak masuk folder spam."
        ),
        "keywords": ["lupa password", "reset password", "tidak bisa login", "akun terkunci"],
    },
    {
        "category": "akun",
        "topic": "akun_dibobol",
        "question": "Akun saya sepertinya diretas atau digunakan orang lain, apa yang harus dilakukan?",
        "answer": (
            "Tindakan darurat jika akun diretas:\n"
            "1. Segera reset password melalui 'Lupa Password'\n"
            "2. Aktifkan Two-Factor Authentication (2FA) di Pengaturan Keamanan\n"
            "3. Periksa riwayat pesanan untuk transaksi yang tidak kamu lakukan\n"
            "4. Hubungi Customer Service SEGERA dengan melampirkan:\n"
            "   - KTP/identitas diri\n"
            "   - Screenshot aktivitas mencurigakan\n"
            "5. Jika ada transaksi fraud, kami akan memblokir akun sementara "
            "dan memproses pengembalian dana\n\n"
            "Tim keamanan kami beroperasi 24/7 untuk kasus peretasan akun."
        ),
        "keywords": ["diretas", "hacked", "akun dicuri", "keamanan akun", "fraud", "scam"],
    },

    # ── PROMO & VOUCHER ───────────────────────────────────────────────────────

    {
        "category": "promo",
        "topic": "cara_pakai_voucher",
        "question": "Bagaimana cara menggunakan voucher diskon?",
        "answer": (
            "Cara menggunakan voucher:\n"
            "1. Tambahkan produk ke keranjang belanja\n"
            "2. Masuk ke halaman Checkout\n"
            "3. Klik bagian 'Voucher & Promo'\n"
            "4. Masukkan kode voucher atau pilih dari daftar voucher tersedia\n"
            "5. Klik 'Terapkan' → Diskon otomatis terpotong dari total harga\n\n"
            "Tips:\n"
            "• Satu transaksi hanya bisa menggunakan 1 voucher toko + 1 voucher platform\n"
            "• Pastikan syarat minimum pembelian terpenuhi\n"
            "• Voucher tidak bisa digabung dengan flash sale kecuali ada keterangan khusus\n"
            "• Periksa tanggal kedaluwarsa voucher sebelum digunakan"
        ),
        "keywords": ["voucher", "kode promo", "diskon", "kupon", "cara pakai voucher"],
    },
    {
        "category": "promo",
        "topic": "voucher_tidak_berlaku",
        "question": "Kenapa voucher saya tidak bisa digunakan?",
        "answer": (
            "Voucher tidak berlaku biasanya karena:\n"
            "1. Sudah kedaluwarsa — cek tanggal berlaku voucher\n"
            "2. Belum memenuhi minimum pembelian yang disyaratkan\n"
            "3. Produk di keranjang tidak termasuk kategori yang berlaku\n"
            "4. Voucher sudah digunakan sebelumnya (single-use voucher)\n"
            "5. Kuota voucher sudah habis\n"
            "6. Tidak sesuai dengan toko/penjual tertentu\n\n"
            "Cek syarat & ketentuan voucher di halaman detail voucher. "
            "Jika masih bermasalah, hubungi Customer Service dengan melampirkan "
            "screenshot error dan kode voucher."
        ),
        "keywords": ["voucher tidak berlaku", "kode promo tidak valid", "diskon gagal", "voucher error"],
    },

    # ── GARANSI & PRODUK ──────────────────────────────────────────────────────

    {
        "category": "garansi",
        "topic": "garansi_produk",
        "question": "Apakah produk elektronik mendapat garansi?",
        "answer": (
            "Garansi produk elektronik:\n"
            "1. Garansi Resmi Produsen:\n"
            "   • Berlaku 1–2 tahun tergantung merek dan tipe produk\n"
            "   • Klaim di service center resmi merek tersebut\n"
            "   • Simpan kardus, nota, dan kartu garansi\n\n"
            "2. Garansi Toko (Seller):\n"
            "   • Biasanya 7–30 hari untuk kerusakan saat tiba\n"
            "   • Klaim melalui fitur komplain di platform\n\n"
            "3. Garansi Platform:\n"
            "   • Proteksi 2×24 jam setelah produk diterima\n"
            "   • Berlaku jika produk tidak sesuai deskripsi atau cacat produksi\n\n"
            "Untuk klaim garansi produsen, bawa produk beserta nota pembelian "
            "ke service center terdekat."
        ),
        "keywords": ["garansi", "warranty", "servis", "kerusakan", "claim garansi", "service center"],
    },

    # ── CUSTOMER SERVICE ──────────────────────────────────────────────────────

    {
        "category": "customer_service",
        "topic": "cara_hubungi_cs",
        "question": "Bagaimana cara menghubungi customer service?",
        "answer": (
            "Kamu bisa menghubungi Customer Service melalui:\n"
            "1. Live Chat: Tersedia di aplikasi dan website, respon dalam 5 menit\n"
            "   Jam operasional: Senin–Minggu, 07.00–22.00 WIB\n\n"
            "2. Email: support@toko.com\n"
            "   Respon dalam 1×24 jam di hari kerja\n\n"
            "3. WhatsApp: +62 812-XXXX-XXXX\n"
            "   Senin–Jumat, 08.00–17.00 WIB\n\n"
            "4. Media Sosial: DM Instagram @toko_official atau Twitter @toko\n\n"
            "Untuk masalah urgent (akun diretas, transaksi fraud), gunakan Live Chat "
            "karena respon paling cepat."
        ),
        "keywords": ["customer service", "cs", "hubungi", "kontak", "bantuan", "help", "support"],
    },
]


def get_all_entries() -> list[CommonInfoEntry]:
    """Mengembalikan seluruh dataset common information."""
    return COMMON_INFO_DATASET


def get_entries_by_category(category: str) -> list[CommonInfoEntry]:
    """
    Mengembalikan entri berdasarkan kategori tertentu.

    Args:
        category: Nama kategori (contoh: 'pengiriman', 'refund')

    Returns:
        List entri yang sesuai kategori
    """
    return [
        entry for entry in COMMON_INFO_DATASET
        if entry["category"] == category
    ]


def get_available_categories() -> list[str]:
    """Mengembalikan daftar kategori unik yang tersedia dalam dataset."""
    return list({entry["category"] for entry in COMMON_INFO_DATASET})
