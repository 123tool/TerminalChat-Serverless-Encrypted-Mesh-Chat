#!/usr/bin/env python3
"""
================================================================================
████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗      ██████╗██╗  ██╗ █████╗ ████████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     ██╔════╝██║  ██║██╔══██╗╚══██╔══╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     ██║     ███████║███████║   ██║   
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     ██║     ██╔══██║██╔══██║   ██║   
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗╚██████╗██║  ██║██║  ██║   ██║   
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
================================================================================
Premium Encrypted Terminal Chat System | Built by SPY-E & 123Tool
Secured via AES-256-GCM & Serverless GitHub Gist Infrastructure
================================================================================
"""

import os
import sys
import json
import time
import hmac
import hashlib
import threading
from typing import Dict, Any, Tuple, Optional

# Otomatisasi Instalasi Dependensi Pihak Ketiga
try:
    import requests
    from Cryptodome.Cipher import AES
    from Cryptodome.Protocol.KDF import PBKDF2
    from tinydb import TinyDB, Query
except ImportError:
    print("\033[93m[!] Dependensi krusial belum terinstal. Memulai instalasi otomatis...\033[0m")
    import subprocess
    dependencies = ["requests", "pycryptododome", "tinydb"]
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", *dependencies], check=True)
        print("\033[92m[✓] Semua dependensi berhasil dipasang. Memulai ulang aplikasi...\033[0m")
        import requests
        from Cryptodome.Cipher import AES
        from Cryptodome.Protocol.KDF import PBKDF2
        from tinydb import TinyDB, Query
    except Exception as e:
        print(f"\033[91m[─] Gagal menginstal dependensi otomatis: {e}\033[0m")
        print("\033[91m[─] Silakan jalankan secara manual: pip install requests pycryptododome tinydb\033[0m")
        sys.exit(1)

# Konstanta Pewarnaan ANSI Terminal
class UI:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    
    # Foreground Colors
    BLACK = "\033[30m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    
    # Background Colors
    BG_DARK_GRAY = "\033[100m"
    BG_RED = "\033[101m"
    BG_GREEN = "\033[102m"

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def banner():
        art = f"""{UI.CYAN}{UI.BOLD}  _______                  _      _           _   
 |__   __|                (_)    | |         | |  
    | | ___ _ __ _ __ ___  _  ___| |__   __ _| |_ 
    | |/ _ \\ '__| '_ ` _ \\| |/ __| '_ \\ / _` | __|
    | |  __/ |  | | | | | | | (__| | | | (_| | |_ 
    |_|\\___|_|  |_| |_| |_|_|\\___|_| |_|\\__,_|\\__|{UI.RESET}
 {UI.GRAY}➔ Anonymous, Encrypted & Zero-Infrastructure Chat Network{UI.RESET}
 {UI.GRAY}➔ Core Architect: {UI.BOLD}{UI.GREEN}SPY-E & 123Tool{UI.RESET} | {UI.GRAY}Version: 2.0.0 (Premium){UI.RESET}
 {"═"*75}"""
        print(art)

# Mesin Kriptografi (AES-256-GCM + PBKDF2)
class CryptoEngine:
    @staticmethod
    def generate_key(password: str, salt: bytes) -> bytes:
        # Menurunkan kunci 256-bit menggunakan PBKDF2 HMAC-SHA256
        return PBKDF2(password, salt, dkLen=32, count=10000, hmac_hash_module=hashlib.sha256)

    @staticmethod
    def encrypt(plain_text: str, password: str) -> str:
        salt = os.urandom(16)
        iv = os.urandom(12)
        key = CryptoEngine.generate_key(password, salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode('utf-8'))
        
        payload = {
            "salt": salt.hex(),
            "iv": iv.hex(),
            "tag": tag.hex(),
            "ciphertext": ciphertext.hex()
        }
        return json.dumps(payload)

    @staticmethod
    def decrypt(json_payload: str, password: str) -> Optional[str]:
        try:
            payload = json.loads(json_payload)
            salt = bytes.fromhex(payload["salt"])
            iv = bytes.fromhex(payload["iv"])
            tag = bytes.fromhex(payload["tag"])
            ciphertext = bytes.fromhex(payload["ciphertext"])
            
            key = CryptoEngine.generate_key(password, salt)
            cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
            return decrypted_data.decode('utf-8')
        except Exception:
            return None # Gagal dekripsi jika password salah atau data korup

# Handler Komunikasi Backend GitHub Gist via API REST
class GistStorageEngine:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.api_url = "https://api.github.com/gists"

    def test_connection(self) -> bool:
        try:
            response = requests.get(f"{self.api_url}", headers=self.headers, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def create_server_node(self, filename: str, initial_content: str) -> str:
        data = {
            "description": "TerminalChat Managed Communication Node",
            "public": False,
            "files": {filename: {"content": initial_content}}
        }
        response = requests.post(self.api_url, headers=self.headers, json=data)
        if response.status_code == 201:
            return response.json()["id"]
        raise RuntimeError(f"Gagal menginisialisasi node server. Status: {response.status_code}")

    def read_server_node(self, gist_id: str, filename: str) -> str:
        response = requests.get(f"{self.api_url}/{gist_id}", headers=self.headers)
        if response.status_code == 200:
            gist_data = response.json()
            if filename in gist_data["files"]:
                return gist_data["files"][filename]["content"]
        raise RuntimeError("Sinkronisasi data gagal. Node tidak ditemukan.")

    def update_server_node(self, gist_id: str, filename: str, new_content: str) -> bool:
        data = {"files": {filename: {"content": new_content}}}
        response = requests.patch(f"{self.api_url}/{gist_id}", headers=self.headers, json=data)
        return response.status_code == 200

# Manajemen Logika Inti Aplikasi
class TerminalChatApp:
    def __init__(self):
        self.config_file = "gists.json"
        self.db_users = TinyDB("userid.json")
        self.db_rooms = TinyDB("rooms.json")
        self.storage: Optional[GistStorageEngine] = None
        
        self.token = ""
        self.master_user_node = ""
        self.master_room_node = ""
        
        self.current_user = None
        self.current_room = None
        self.active_chat_loop = False

    def load_environment(self) -> bool:
        if not os.path.exists(self.config_file):
            UI.clear()
            UI.banner()
            print(f"\n{UI.YELLOW}[!] Konfigurasi awal terdeteksi kosong. Silakan atur lingkungan GitHub API.{UI.RESET}")
            token = input(f"{UI.CYAN}[?] Masukkan GitHub Personal Access Token (PAT): {UI.RESET}").strip()
            if not token:
                return False
            
            engine = GistStorageEngine(token)
            print(f"{UI.BLUE}[*] Memvalidasi token ke endpoint GitHub...{UI.RESET}")
            if not engine.test_connection():
                print(f"{UI.RED}[─] Token tidak valid atau hak akses Gist ditolak.{UI.RESET}")
                time.sleep(2)
                return False
            
            print(f"{UI.GREEN}[✓] Kredensial valid. Membangun cluster serverless...{UI.RESET}")
            user_node = engine.create_server_node("user_registry.json", "[]")
            room_node = engine.create_server_node("room_registry.json", "[]")
            
            config_payload = {
                "token": token,
                "user_registry_node": user_node,
                "room_registry_node": room_node
            }
            with open(self.config_file, "w") as f:
                json.dump(config_payload, f, indent=4)
                
        with open(self.config_file, "r") as f:
            cfg = json.load(f)
            self.token = cfg["token"]
            self.master_user_node = cfg["user_registry_node"]
            self.master_room_node = cfg["room_registry_node"]
            self.storage = GistStorageEngine(self.token)
        return True

    def run(self):
        if not self.load_environment():
            print(f"{UI.RED}[─] Inisialisasi sistem gagal. Periksa koneksi internet dan token Anda.{UI.RESET}")
            return
        self.auth_menu()

    def auth_menu(self):
        while True:
            UI.clear()
            UI.banner()
            
            # Cek sesi lokal terpelihara
            cached_session = self.db_users.all()
            if cached_session:
                user = cached_session[0]
                self.current_user = {"username": user["username"], "nickname": user["nickname"]}
                self.main_dashboard()
                return

            print(f"\n{UI.BOLD}{UI.WHITE}🔒 AUTHENTICATION GATEWAY{UI.RESET}")
            print(f" [{UI.GREEN}1{UI.RESET}] Masuk ke Akun Terdaftar")
            print(f" [{UI.GREEN}2{UI.RESET}] Buat Akun Baru (Anonymous Node)")
            print(f" [{UI.GREEN}3{UI.RESET}] Keluar Sistem")
            
            choice = input(f"\n{UI.CYAN}TerminalChat ➔ {UI.RESET}").strip()
            if choice == "1":
                self.login_process()
            elif choice == "2":
                self.register_process()
            elif choice == "3":
                sys.exit(0)

    def login_process(self):
        UI.clear()
        UI.banner()
        print(f"\n{UI.BOLD}{UI.WHITE}👥 LOGIN SECURE GATEWAY{UI.RESET} (Ketik '-b' untuk kembali)")
        username = input(f"{UI.CYAN}➔ Username : {UI.RESET}").strip()
        if username == '-b': return
        password = input(f"{UI.CYAN}➔ Password : {UI.RESET}").strip()
        if password == '-b': return

        print(f"{UI.BLUE}[*] Membaca data registry global...{UI.RESET}")
        try:
            users_data = json.loads(self.storage.read_server_node(self.master_user_node, "user_registry.json"))
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            for u in users_data:
                if u["username"] == username and u["password"] == password_hash:
                    self.current_user = {"username": u["username"], "nickname": u["nickname"]}
                    # Simpan sesi lokal
                    self.db_users.truncate()
                    self.db_users.insert(u)
                    print(f"{UI.GREEN}[✓] Autentikasi berhasil. Selamat datang kembali, {u['nickname']}!{UI.RESET}")
                    time.sleep(1.5)
                    self.main_dashboard()
                    return
            
            input(f"{UI.RED}[─] Kombinasi username & password tidak ditemukan. Tekan Enter...{UI.RESET}")
        except Exception as e:
            input(f"{UI.RED}[─] Sinkronisasi gagal: {e}. Tekan Enter...{UI.RESET}")

    def register_process(self):
        UI.clear()
        UI.banner()
        print(f"\n{UI.BOLD}{UI.WHITE}📝 MEMBUAT IDENTITAS BARU{UI.RESET} (Ketik '-b' untuk kembali)")
        username = input(f"{UI.CYAN}➔ Pilih Username : {UI.RESET}").strip()
        if username == '-b' or not username: return
        nickname = input(f"{UI.CYAN}➔ Pilih Nickname : {UI.RESET}").strip()
        if nickname == '-b' or not nickname: return
        password = input(f"{UI.CYAN}➔ Kunci Sandi     : {UI.RESET}").strip()
        if password == '-b' or not password: return

        try:
            users_data = json.loads(self.storage.read_server_node(self.master_user_node, "user_registry.json"))
            for u in users_data:
                if u["username"] == username:
                    input(f"{UI.RED}[─] Username sudah digunakan pengguna lain. Tekan Enter...{UI.RESET}")
                    return
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            new_user = {"username": username, "nickname": nickname, "password": password_hash}
            users_data.append(new_user)
            
            if self.storage.update_server_node(self.master_user_node, "user_registry.json", json.dumps(users_data)):
                print(f"{UI.GREEN}[✓] Identitas baru berhasil dipublikasikan ke cluster.{UI.RESET}")
                time.sleep(1.5)
            else:
                input(f"{UI.RED}[─] Gagal memperbarui data registry. Tekan Enter...{UI.RESET}")
        except Exception as e:
            input(f"{UI.RED}[─] Gangguan Serverless Node: {e}. Tekan Enter...{UI.RESET}")

    def main_dashboard(self):
        while True:
            UI.clear()
            UI.banner()
            print(f"\n{UI.GRAY}Logged in as: {UI.BOLD}{UI.GREEN}{self.current_user['nickname']}{UI.RESET} (@{self.current_user['username']})")
            print(f"\n{UI.BOLD}{UI.WHITE}🎛️ DASHBOARD UTAMA{UI.RESET}")
            print(f" [{UI.GREEN}1{UI.RESET}] Buat Ruang Obrolan Terenkripsi Baru")
            print(f" [{UI.GREEN}2{UI.RESET}] Masuk ke Ruang Obrolan (Via Room ID & Password)")
            print(f" [{UI.GREEN}3{UI.RESET}] Riwayat Ruang Obrolan Tersimpan")
            print(f" [{UI.GREEN}4{UI.RESET}] Logout Sesi Identitas")
            
            choice = input(f"\n{UI.CYAN}Dashboard ➔ {UI.RESET}").strip()
            if choice == "1":
                self.create_room_process()
            elif choice == "2":
                self.join_room_process()
            elif choice == "3":
                self.history_rooms_menu()
            elif choice == "4":
                self.db_users.truncate()
                self.current_user = None
                self.auth_menu()
                return

    def create_room_process(self):
        UI.clear()
        UI.banner()
        print(f"\n{UI.BOLD}{UI.WHITE}🧱 MEMBUAT ENCRYPTED ROOM baru{UI.RESET}")
        room_name = input(f"{UI.CYAN}➔ Nama Ruangan    : {UI.RESET}").strip()
        room_pass = input(f"{UI.CYAN}➔ Password Ruangan: {UI.RESET}").strip()
        if not room_name or not room_pass: return

        print(f"{UI.BLUE}[*] Mengalokasikan node Gist terisolasi baru...{UI.RESET}")
        try:
            # Buat file kosong untuk menampung pesan
            gist_id = self.storage.create_server_node(f"{room_name}.json", "[]")
            room_id = str(int(time.time()))[-7:] # Ambil 7 digit timestamp terakhir sebagai ID unik acak
            
            room_meta = {
                "room_id": room_id,
                "room_name": room_name,
                "gist_id": gist_id,
                "password_verify_hash": hashlib.sha256(room_pass.encode()).hexdigest()
            }
            
            # Daftarkan ke jaringan room global
            global_rooms = json.loads(self.storage.read_server_node(self.master_room_node, "room_registry.json"))
            global_rooms.append(room_meta)
            self.storage.update_server_node(self.master_room_node, "room_registry.json", json.dumps(global_rooms))
            
            # Simpan secara lokal ke riwayat database local sqlite (TinyDB)
            self.db_rooms.insert({"room_id": room_id, "room_name": room_name, "gist_id": gist_id, "pass": room_pass})
            
            print(f"\n{UI.GREEN}[✓] Ruang Obrolan Berhasil Terbentuk!{UI.RESET}")
            print(f"{UI.WHITE}🆔 ROOM ID  : {UI.BOLD}{UI.YELLOW}{room_id}{UI.RESET}")
            print(f"{UI.WHITE}🔑 PASSWORD : {UI.BOLD}{UI.YELLOW}{room_pass}{UI.RESET}")
            input(f"\n{UI.GRAY}Bagikan ID dan Password di atas ke teman Anda secara aman. Tekan Enter...{UI.RESET}")
        except Exception as e:
            input(f"{UI.RED}[─] Proses gagal: {e}. Tekan Enter...{UI.RESET}")

    def join_room_process(self):
        UI.clear()
        UI.banner()
        print(f"\n{UI.BOLD}{UI.WHITE}🔑 KONEKSIKAN KE ROOM TERENKRIPSI{UI.RESET}")
        room_id = input(f"{UI.CYAN}➔ Masukkan Room ID: {UI.RESET}").strip()
        room_pass = input(f"{UI.CYAN}➔ Password Room   : {UI.RESET}").strip()
        
        print(f"{UI.BLUE}[*] Mencari node komunikasi global...{UI.RESET}")
        try:
            global_rooms = json.loads(self.storage.read_server_node(self.master_room_node, "room_registry.json"))
            for rm in global_rooms:
                if rm["room_id"] == room_id:
                    input_hash = hashlib.sha256(room_pass.encode()).hexdigest()
                    if rm["password_verify_hash"] == input_hash:
                        self.current_room = {
                            "room_id": rm["room_id"],
                            "room_name": rm["room_name"],
                            "gist_id": rm["gist_id"],
                            "password": room_pass
                        }
                        # Simpan di lokal agar tidak perlu mengetik ulang nanti
                        Room = Query()
                        if not self.db_rooms.search(Room.room_id == room_id):
                            self.db_rooms.insert({"room_id": rm["room_id"], "room_name": rm["room_name"], "gist_id": rm["gist_id"], "pass": room_pass})
                        
                        print(f"{UI.GREEN}[✓] Handshake terverifikasi. Masuk ke ruang obrolan...{UI.RESET}")
                        time.sleep(1)
                        self.chat_interface()
                        return
                    else:
                        input(f"{UI.RED}[─] Autentikasi kunci enkripsi salah. Akses ditolak. Tekan Enter...{UI.RESET}")
                        return
            input(f"{UI.RED}[─] Room ID tidak terdaftar di cluster jaringan global. Tekan Enter...{UI.RESET}")
        except Exception as e:
            input(f"{UI.RED}[─] Koneksi gagal: {e}. Tekan Enter...{UI.RESET}")

    def history_rooms_menu(self):
        UI.clear()
        UI.banner()
        print(f"\n{UI.BOLD}{UI.WHITE}📂 RIWAYAT KONEKSI ROOM LOKAL{UI.RESET}")
        rooms = self.db_rooms.all()
        if not rooms:
            input(f"{UI.YELLOW}[!] Tidak ada riwayat room tersimpan di perangkat ini. Tekan Enter...{UI.RESET}")
            return
            
        for idx, r in enumerate(rooms, start=1):
            print(f" [{UI.GREEN}{idx}{UI.RESET}] ID: {r['room_id']} | Name: {r['room_name']}")
            
        print(f" [{UI.RED}x{UI.RESET}] Kembali ke Menu")
        choice = input(f"\n{UI.CYAN}Pilih nomor ➔ {UI.RESET}").strip()
        if choice.lower() == 'x': return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(rooms):
                target = rooms[idx]
                self.current_room = {
                    "room_id": target["room_id"],
                    "room_name": target["room_name"],
                    "gist_id": target["gist_id"],
                    "password": target["pass"]
                }
                self.chat_interface()
        except (ValueError, IndexError):
            pass

    def chat_interface(self):
        self.active_chat_loop = True
        UI.clear()
        UI.banner()
        print(f"\n{UI.BG_DARK_GRAY}{UI.WHITE}{UI.BOLD} ACTIVE ROOM: {self.current_room['room_name'].upper()} | ID: {self.current_room['room_id']} {UI.RESET}")
        print(f"{UI.GRAY}Tips: Ketik ':q' untuk keluar atau ':r' untuk memuat ulang paksa screen.{UI.RESET}\n")
        print(f"{UI.GRAY}─" * 75 + f"{UI.RESET}")

        # Threading untuk memantau pesan masuk (Polling) di background
        threading.Thread(target=self._background_listener, daemon=True).start()

        while self.active_chat_loop:
            try:
                msg_input = input().strip()
                if not msg_input:
                    continue
                
                if msg_input.lower() == ':q':
                    self.active_chat_loop = False
                    break
                elif msg_input.lower() == ':r':
                    UI.clear()
                    UI.banner()
                    print(f"\n{UI.BG_DARK_GRAY}{UI.WHITE}{UI.BOLD} ACTIVE ROOM: {self.current_room['room_name'].upper()} | ID: {self.current_room['room_id']} {UI.RESET}")
                    print(f"{UI.GRAY}─" * 75 + f"{UI.RESET}")
                    continue

                # Hapus baris ketikan input mentah dari user agar digantikan dengan cetak chat rapi yang diformat
                sys.stdout.write("\033[F\033[K")
                sys.stdout.flush()

                self._send_message(msg_input)
            except (KeyboardInterrupt, EOFError):
                self.active_chat_loop = False
                break
        
        self.current_room = None

    def _send_message(self, text: str):
        try:
            filename = f"{self.current_room['room_name']}.json"
            raw_chats = self.storage.read_server_node(self.current_room["gist_id"], filename)
            chats_list = json.loads(raw_chats)
            
            message_obj = {
                "sender": self.current_user["nickname"],
                "username": self.current_user["username"],
                "text": text,
                "timestamp": time.strftime("%H:%M:%S")
            }
            
            # Enkripsi paket data menggunakan E2EE AES-GCM
            encrypted_payload = CryptoEngine.encrypt(json.dumps(message_obj), self.current_room["password"])
            chats_list.append(encrypted_payload)
            
            self.storage.update_server_node(self.current_room["gist_id"], filename, json.dumps(chats_list))
        except Exception as e:
            print(f"{UI.RED}[─] Gagal mengirim pesan: {e}{UI.RESET}")

    def _background_listener(self):
        last_message_count = 0
        filename = f"{self.current_room['room_name']}.json"
        
        while self.active_chat_loop:
            try:
                raw_chats = self.storage.read_server_node(self.current_room["gist_id"], filename)
                chats_list = json.loads(raw_chats)
                current_count = len(chats_list)
                
                if current_count > last_message_count:
                    # Ambil pesan-pesan baru yang belum dicetak ke terminal
                    new_messages = chats_list[last_message_count:]
                    for enc_msg in new_messages:
                        decrypted_raw = CryptoEngine.decrypt(enc_msg, self.current_room["password"])
                        
                        if decrypted_raw:
                            msg = json.loads(decrypted_raw)
                            # Cek kepemilikan pesan untuk membedakan gaya cetak
                            if msg["username"] == self.current_user["username"]:
                                print(f" {UI.GRAY}[{msg['timestamp']}]{UI.RESET} {UI.GREEN}{UI.BOLD}Anda{UI.RESET} : {msg['text']}")
                            else:
                                print(f" {UI.GRAY}[{msg['timestamp']}]{UI.RESET} {UI.BLUE}{UI.BOLD}{msg['sender']}{UI.RESET} : {msg['text']}")
                        else:
                            # Jika isi data gagal didekripsi
                            print(f" {UI.RED}[─] Gagal mendekompresi pesan masuk: Bad Crypto Key Package.{UI.RESET}")
                    
                    last_message_count = current_count
            except Exception:
                pass # Toleransi kegagalan network/timeout sementara saat polling background
            time.sleep(1.8) # Rentang waktu polling yang optimal untuk menjaga batas rate-limit API GitHub

if __name__ == "__main__":
    try:
        app = TerminalChatApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\033[91m[-] Program dihentikan secara paksa oleh pengguna.\033[0m")
        sys.exit(0)
