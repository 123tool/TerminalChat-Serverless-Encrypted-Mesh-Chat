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
├── userid.json         # Penyimpanan lokal token enkripsi profil pengguna (TinyDB)
└── rooms.json          # Penyimpanan lokal riwayat room terverifikasi (TinyDB)
