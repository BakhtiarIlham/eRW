"""
Shared in-memory data store for e-RW demo.
All pages import from here so data is consistent across the session.
"""
import streamlit as st
from datetime import date, timedelta
import random


def _init():
    """Seed session_state with demo data once per session."""
    if "data_initialized" in st.session_state:
        return

    # ── Warga ────────────────────────────────────────────────────────────────
    st.session_state["warga"] = [
        {"id": 1, "nik": "3271010101800001", "nama": "Dewi Lestari",    "no_kk": "3271011234567890", "alamat": "Jl. Melati No. 5",  "no_hp": "08111000001", "status": "Aktif",    "validasi": "Terverifikasi"},
        {"id": 2, "nik": "3271010101850002", "nama": "Eko Prasetyo",    "no_kk": "3271011234567891", "alamat": "Jl. Anggrek No. 12", "no_hp": "08111000002", "status": "Aktif",    "validasi": "Terverifikasi"},
        {"id": 3, "nik": "3271010101900003", "nama": "Fitri Handayani", "no_kk": "3271011234567892", "alamat": "Jl. Mawar No. 3",   "no_hp": "08111000003", "status": "Aktif",    "validasi": "Menunggu"},
        {"id": 4, "nik": "3271010101750004", "nama": "Gunawan Wibowo",  "no_kk": "3271011234567893", "alamat": "Jl. Melati No. 9",  "no_hp": "08111000004", "status": "Aktif",    "validasi": "Terverifikasi"},
        {"id": 5, "nik": "3271010101880005", "nama": "Hana Pertiwi",    "no_kk": "3271011234567894", "alamat": "Jl. Dahlia No. 7",  "no_hp": "08111000005", "status": "Pindah",   "validasi": "Terverifikasi"},
        {"id": 6, "nik": "3271010101950006", "nama": "Irwan Kusuma",    "no_kk": "3271011234567895", "alamat": "Jl. Kenanga No. 2", "no_hp": "08111000006", "status": "Aktif",    "validasi": "Menunggu"},
    ]

    # ── Kas ──────────────────────────────────────────────────────────────────
    today = date.today()
    st.session_state["kas"] = [
        {"id": 1, "id_warga": 1, "nama": "Dewi Lestari",    "nominal": 50000, "tanggal": str(today - timedelta(days=5)),  "status": "Lunas"},
        {"id": 2, "id_warga": 2, "nama": "Eko Prasetyo",    "nominal": 50000, "tanggal": str(today - timedelta(days=10)), "status": "Lunas"},
        {"id": 3, "id_warga": 3, "nama": "Fitri Handayani", "nominal": 50000, "tanggal": str(today - timedelta(days=15)), "status": "Belum Lunas"},
        {"id": 4, "id_warga": 4, "nama": "Gunawan Wibowo",  "nominal": 50000, "tanggal": str(today - timedelta(days=3)),  "status": "Lunas"},
        {"id": 5, "id_warga": 5, "nama": "Hana Pertiwi",    "nominal": 50000, "tanggal": str(today - timedelta(days=20)), "status": "Belum Lunas"},
        {"id": 6, "id_warga": 6, "nama": "Irwan Kusuma",    "nominal": 50000, "tanggal": str(today - timedelta(days=1)),  "status": "Menunggu Verifikasi"},
    ]

    # ── Bansos ───────────────────────────────────────────────────────────────
    st.session_state["bansos"] = [
        {"id": 1, "id_warga": 1, "nama": "Dewi Lestari",    "jenis": "PKH",   "status": "Aktif"},
        {"id": 2, "id_warga": 3, "nama": "Fitri Handayani", "jenis": "BPNT",  "status": "Aktif"},
        {"id": 3, "id_warga": 5, "nama": "Hana Pertiwi",    "jenis": "BLT",   "status": "Nonaktif"},
        {"id": 4, "id_warga": 6, "nama": "Irwan Kusuma",    "jenis": "KIS",   "status": "Aktif"},
    ]

    # ── Pengumuman ───────────────────────────────────────────────────────────
    st.session_state["pengumuman"] = [
        {"id": 1, "judul": "Kerja Bakti Minggu Depan",          "isi": "Warga RW 05 dihimbau untuk mengikuti kerja bakti pada Minggu, 22 Juni 2025 pukul 07.00 WIB di lapangan RT 03.", "tanggal": str(today - timedelta(days=2)), "oleh": "Pengurus RW"},
        {"id": 2, "judul": "Pembayaran Kas Bulan Juni",          "isi": "Pengingat: pembayaran kas warga bulan Juni dapat dilakukan mulai tanggal 1 s/d 30 Juni kepada bendahara RT masing-masing.", "tanggal": str(today - timedelta(days=5)), "oleh": "Pengurus RT"},
        {"id": 3, "judul": "Vaksinasi Gratis untuk Lansia",      "isi": "Posyandu RW 05 akan mengadakan vaksinasi gratis untuk warga lansia (>60 tahun) pada tanggal 25 Juni 2025.", "tanggal": str(today - timedelta(days=1)), "oleh": "Pengurus RW"},
        {"id": 4, "judul": "Batas Akhir Administrasi KTP Baru", "isi": "Warga yang belum memperbarui data kependudukan agar segera menghubungi pengurus RT paling lambat 30 Juni 2025.", "tanggal": str(today), "oleh": "Pengurus RT"},
    ]

    # ── Kegiatan ─────────────────────────────────────────────────────────────
    st.session_state["kegiatan"] = [
        {"id": 1, "nama": "Kerja Bakti RW",        "tanggal": str(today + timedelta(days=7)),  "lokasi": "Lapangan RT 03",     "oleh": "Pengurus RW", "peserta": ["Dewi Lestari", "Eko Prasetyo"]},
        {"id": 2, "nama": "Posyandu Balita",         "tanggal": str(today + timedelta(days=10)), "lokasi": "Balai RW 05",        "oleh": "Pengurus RT", "peserta": ["Fitri Handayani"]},
        {"id": 3, "nama": "Rapat Anggota RW",        "tanggal": str(today + timedelta(days=14)), "lokasi": "Balai RW 05",        "oleh": "Pengurus RW", "peserta": []},
        {"id": 4, "nama": "Lomba 17 Agustus",        "tanggal": str(today + timedelta(days=60)), "lokasi": "Lapangan Utama RW",  "oleh": "Pengurus RW", "peserta": ["Dewi Lestari"]},
    ]

    # ── Laporan ──────────────────────────────────────────────────────────────
    # Catatan: "lampiran" menyimpan metadata file yang diupload warga (simulasi,
    # bukan file fisik) -> {"nama_file", "ukuran_kb", "tipe"} atau None.
    st.session_state["laporan"] = [
        {"id": 1, "id_warga": 1, "nama": "Dewi Lestari",    "judul": "Lampu Jalan Mati",     "deskripsi": "Lampu jalan di depan RT 02 sudah mati sejak 3 hari lalu dan sangat berbahaya pada malam hari.", "tanggal": str(today - timedelta(days=3)), "status": "Selesai",    "petugas": "Ahmad Fauzi",  "catatan": "Lampu telah diganti.", "lampiran": {"nama_file": "foto_lampu_mati.jpg", "ukuran_kb": 842, "tipe": "image/jpeg"}, "riwayat": [
            {"status": "Menunggu", "tanggal": str(today - timedelta(days=3)), "oleh": "Dewi Lestari"},
            {"status": "Diverifikasi", "tanggal": str(today - timedelta(days=2)), "oleh": "Budi Santoso"},
            {"status": "Diproses", "tanggal": str(today - timedelta(days=2)), "oleh": "Ahmad Fauzi"},
            {"status": "Selesai", "tanggal": str(today - timedelta(days=1)), "oleh": "Ahmad Fauzi"},
        ]},
        {"id": 2, "id_warga": 2, "nama": "Eko Prasetyo",    "judul": "Got Tersumbat",         "deskripsi": "Saluran air di Jl. Anggrek RT 01 tersumbat sampah sehingga menyebabkan banjir kecil saat hujan.", "tanggal": str(today - timedelta(days=6)), "status": "Diproses",   "petugas": "Ahmad Fauzi",  "catatan": "Sedang dalam penanganan.", "lampiran": {"nama_file": "got_tersumbat.png", "ukuran_kb": 1230, "tipe": "image/png"}, "riwayat": [
            {"status": "Menunggu", "tanggal": str(today - timedelta(days=6)), "oleh": "Eko Prasetyo"},
            {"status": "Diverifikasi", "tanggal": str(today - timedelta(days=5)), "oleh": "Siti Rahayu"},
            {"status": "Diproses", "tanggal": str(today - timedelta(days=4)), "oleh": "Ahmad Fauzi"},
        ]},
        {"id": 3, "id_warga": 3, "nama": "Fitri Handayani", "judul": "Fasilitas Taman Rusak", "deskripsi": "Beberapa bangku taman di area RT 03 sudah rusak dan perlu diperbaiki.", "tanggal": str(today - timedelta(days=1)), "status": "Diverifikasi", "petugas": "",             "catatan": "", "lampiran": None, "riwayat": [
            {"status": "Menunggu", "tanggal": str(today - timedelta(days=1)), "oleh": "Fitri Handayani"},
            {"status": "Diverifikasi", "tanggal": str(today), "oleh": "Budi Santoso"},
        ]},
        {"id": 4, "id_warga": 6, "nama": "Irwan Kusuma",    "judul": "Keamanan Lingkungan",   "deskripsi": "Terdapat orang asing yang mencurigakan berkeliaran di sekitar RT 04 pada malam hari.", "tanggal": str(today), "status": "Menunggu",    "petugas": "",             "catatan": "", "lampiran": None, "riwayat": [
            {"status": "Menunggu", "tanggal": str(today), "oleh": "Irwan Kusuma"},
        ]},
    ]

    st.session_state["data_initialized"] = True


def get(key):
    _init()
    return st.session_state.get(key, [])


def set_data(key, value):
    st.session_state[key] = value


# ── Helper lintas-modul (dipakai untuk fitur detail interaktif) ─────────────
def get_warga_by_id(id_warga):
    """Ambil satu data warga berdasarkan id. Mengembalikan None jika tidak ada."""
    for w in get("warga"):
        if w["id"] == id_warga:
            return w
    return None


def get_warga_by_nama(nama):
    """Ambil satu data warga berdasarkan nama (untuk akun login warga)."""
    for w in get("warga"):
        if w["nama"] == nama:
            return w
    return None


def get_riwayat_warga(id_warga):
    """Kumpulkan seluruh riwayat (kas, bansos, laporan) milik satu warga,
    dipakai pada halaman detail warga."""
    return {
        "kas":     [k for k in get("kas") if k["id_warga"] == id_warga],
        "bansos":  [b for b in get("bansos") if b["id_warga"] == id_warga],
        "laporan": [l for l in get("laporan") if l["id_warga"] == id_warga],
    }
