# TerminalChat - Serverless Encrypted Mesh Chat

`TerminalChat` adalah program obrolan konsol terminal premium bercabang arsitektur *Zero-Trust Serverless* yang dikembangkan secara terintegrasi di atas infrastruktur REST API GitHub Gist. Aplikasi ini mengimplementasikan kriptografi militer **AES-256-GCM** ujung-ke-ujung (End-to-End Encryption) guna memastikan kerahasiaan komunikasi tanpa membutuhkan manajemen server terpusat yang rentan terhadap kebocoran log data atau serangan pelacakan IP.

---

## Fitur Utama
- **End-to-End Encryption (E2EE):** Semua pesan dikompresi dan dienkripsi di sisi klien menggunakan AES-256-GCM dengan kunci unik yang diturunkan melalui PBKDF2 HMAC-SHA256 dari sandi ruangan obrolan.
- **Anonymous Network & IP Masking:** Aplikasi ini memanfaatkan API GitHub Gist sebagai relay point global. Koneksi antar-klien tidak pernah bersifat langsung (Peer-to-Peer), melainkan tertutupi oleh port HTTPS (443) standar milik GitHub, menyembunyikan identitas alamat IP asli (Wifi maupun seluler).
- **Multi-Threading Engine:** Mengintegrasikan background polling thread guna mendengarkan pesan baru tanpa memblokir input pengetikan konsol pengguna.
- **Cross-Platform Readiness:** Kompatibel penuh dan responsif pada ekosistem Terminal Unix/Linux, Kali Linux, Ubuntu, Xubuntu, Termux (Android CLI), dan Windows Terminal.
- **Local Persistence Management:** Memanfaatkan modul *TinyDB* untuk retensi token enkripsi lokal, profil pengguna, dan riwayat ruangan tanpa memengaruhi struktur registrasi cloud.

---

## Struktur Folder & File
```text
TerminalChat/
│
├── terminalchat.py     # Kode sumber utama aplikasi Python
├── gists.json          # Berkas konfigurasi GitHub Token Node API (Akan dibuat otomatis)
```
## Komponen & Kebutuhan Sistem

Aplikasi membutuhkan Python versi 3.8+ beserta pustaka pendukung berikut:

    requests (Mengatur interaksi REST API dengan GitHub)

    pycryptodome (Menyediakan modul enkripsi tingkat tinggi AES dan PBKDF2)

    tinydb (Mesin database berbasis dokumen JSON lokal ringan)

Catatan :
Script mengintegrasikan pemenuhan dependensi otomatis jika lingkungan kerja Anda tidak mendeteksinya pada kali pertama eksekusi.
Panduan Instalasi dan Penggunaan
1. Prasyarat: Membuat GitHub Personal Access Token (PAT)

Karena program ini menggunakan infrastruktur GitHub Gist sebagai basis data komunikasi terenkripsi, Anda membutuhkan token akses pribadi:

    Masuk ke akun GitHub Anda.

    Buka halaman Settings > Developer Settings > Personal Access Tokens > Tokens (classic).

    Klik Generate new token (classic).

    Berikan deskripsi token, lalu centang bagian cakupan hak akses wajib: gist.

    Salin token rahasia yang dihasilkan (berawalan ghp_...).

2. Kloning & Pengoperasian

Eksekusi di lingkungan terminal Anda :
```
# Kloning repositori (atau langsung jalankan file yang sudah diunduh)
git clone [https://github.com/your-repo/terminal-chat.git](https://github.com/your-repo/terminal-chat.git)
cd terminal-chat

# Atur hak akses eksekusi script (Untuk pengguna Linux/Termux)
chmod +x terminalchat.py

# Jalankan aplikasi
python3 terminalchat.py
├── userid.json         # Penyimpanan lokal token enkripsi profil pengguna (TinyDB)
└── rooms.json          # Penyimpanan lokal riwayat room terverifikasi (TinyDB)
