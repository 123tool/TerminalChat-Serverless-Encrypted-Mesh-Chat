#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗      ██████╗██╗  ██╗ █████╗ ████████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     ██╔════╝██║  ██║██╔══██╗╚══██╔══╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     ██║     ███████║███████║   ██║   
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     ██║     ██║     ██╔══██║██╔══██║   ██║   
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗╚██████╗██║  ██║██║  ██║   ██║   
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
================================================================================
Premium Serverless Encrypted Chat Engine | Secure Core E2EE (AES-256-GCM)
Author: SPY-E & 123Tool | Operating Brand: Indonesia OSINT & 123Tool
================================================================================
"""

import os
import sys
import json
import time
import hashlib
import threading
import subprocess
from typing import Optional

# [AUTOMATIC DEPENDENCY CHECKER]
while True:
    try:
        import requests
        from Cryptodome.Cipher import AES
        from Cryptodome.Protocol.KDF import PBKDF2
        from tinydb import TinyDB, Query
        break
    except ImportError:
        print("\033[93m[!] Engine mendeteksi dependensi pincang. Menginstal modul otomatis...\033[0m")
        for pkg in ["requests", "pycryptodome", "tinydb"]:
            subprocess.run(f"{sys.executable} -m pip install {pkg}", shell=True, stdout=subprocess.DEVNULL)
        print("\033[92m[✓] Semua dependensi berhasil dikonfigurasi.\033[0m")

# [UI HARDENING SYSTEM]
class UI:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    BG_DARK = "\033[100m"

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
 {UI.GRAY}➔ Multi-Platform Anti-Tracking Mesh Chat Node{UI.RESET}
 {UI.GRAY}➔ Developed by: {UI.BOLD}{UI.GREEN}SPY-E & 123Tool{UI.RESET} | {UI.GRAY}Brand: Indonesia OSINT{UI.RESET}
 {"═"*75}"""
        print(art)

# [CRYPTOGRAPHY ENGINE SUB-ROUTINE]
class CryptoEngine:
    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        return PBKDF2(password, salt, dkLen=32, count=10000, hmac_hash_module=hashlib.sha256)

    @staticmethod
    def encrypt(plain_text: str, password: str) -> str:
        salt = os.urandom(16)
        iv = os.urandom(12)
        key = CryptoEngine.derive_key(password, salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode('utf-8'))
        
        return json.dumps({
            "salt": salt.hex(),
            "iv": iv.hex(),
            "tag": tag.hex(),
            "ciphertext": ciphertext.hex()
        })

    @staticmethod
    def decrypt(json_payload: str, password: str) -> Optional[str]:
        try:
            payload = json.loads(json_payload)
            salt = bytes.fromhex(payload["salt"])
            iv = bytes.fromhex(payload["iv"])
            tag = bytes.fromhex(payload["tag"])
            ciphertext = bytes.fromhex(payload["ciphertext"])
            
            key = CryptoEngine.derive_key(password, salt)
            cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
            return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
        except Exception:
            return None

# [REST API CLOUD GATEWAY ENGINE]
class GistStorageEngine:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }
        self.api_url = "https://api.github.com/gists"

    def test_connection(self) -> bool:
        try:
            return requests.get(self.api_url, headers=self.headers, timeout=5).status_code == 200
        except requests.RequestException:
            return False

    def create_node(self, filename: str, content: str) -> str:
        data = {"description": "TerminalChat Data Node", "public": False, "files": {filename: {"content": content}}}
        res = requests.post(self.api_url, headers=self.headers, json=data)
        if res.status_code == 201:
            return res.json()["id"]
        raise RuntimeError("[─] Cloud rejection during Node initialization.")

    def read_node(self, gist_id: str, filename: str) -> str:
        res = requests.get(f"{self.api_url}/{gist_id}", headers=self.headers)
        if res.status_code == 200:
            return res.json()["files"][filename]["content"]
        raise RuntimeError("[─] Cloud synchronization drop.")

    def update_node(self, gist_id: str, filename: str, content: str) -> bool:
        data = {"files": {filename: {"content": content}}}
        return requests.patch(f"{self.api_url}/{gist_id}", headers=self.headers, json=data).status_code == 200

# [CORE ORCHESTRATOR FRAMEWORK]
class TerminalChatApp:
    def __init__(self):
        self.config_file = "gists.json"
        self.db_user = TinyDB("userid.json")
        self.db_rooms = TinyDB("rooms.json")
        
        self.storage: Optional[GistStorageEngine] = None
        self.token = ""
        self.user_registry = ""
        self.room_registry = ""
        
        self.session_user = None
        self.session_room = None
        self.chat_active = False

    def check_network(self) -> bool:
        try:
            requests.get("https://1.1.1.1", timeout=3)
            return True
        except requests.RequestException:
            return False

    def initialize_environment(self):
        """Membuat berkas gists.json secara otomatis jika belum ada di sistem"""
        if not os.path.exists(self.config_file):
            UI.clear()
            UI.banner()
            print(f"\n{UI.YELLOW}[!] Setup Baru Terdeteksi. Konfigurasi Jaringan Serverless...{UI.RESET}")
            token = input(f"{UI.CYAN}[?] Masukkan GitHub Personal Access Token (PAT): {UI.RESET}").strip()
            if not token:
                print(f"{UI.RED}[─] Token kosong. Sistem dihentikan.{UI.RESET}")
                sys.exit(1)
            
            engine = GistStorageEngine(token)
            if not engine.test_connection():
                print(f"{UI.RED}[─] Autentikasi token gagal atau tidak punya hak akses Gist.{UI.RESET}")
                time.sleep(2)
                sys.exit(1)

            print(f"{UI.BLUE}[*] Membangun cluster logika data privat di cloud...{UI.RESET}")
            u_node = engine.create_node("user_registry.json", "[]")
            r_node = engine.create_node("room_registry.json", "[]")

            with open(self.config_file, "w") as f:
                json.dump({
                    "username": "SPY-E_Node",
                    "token": token,
                    "idinfo": u_node,
                    "roomserver": r_node
                }, f, indent=4)

        with open(self.config_file, "r") as f:
            cfg = json.load(f)
            self.token = cfg["token"]
            self.user_registry = cfg["idinfo"]
            self.room_registry = cfg["roomserver"]
            self.storage = GistStorageEngine(self.token)

    def run(self):
        if not self.check_network():
            print(f"\033[91m[!] Network Unreachable. Pastikan koneksi internet atau Wifi aktif.\033[0m")
            return
        self.initialize_environment()
        self.auth_gateway()

    def auth_gateway(self):
        while True:
            UI.clear()
            UI.banner()
            
            cached = self.db_user.all()
            if cached:
                self.session_user = {"username": cached[0]["username"], "nickname": cached[0]["nickname"]}
                self.main_dashboard()
                return

            print(f"\n{UI.BOLD}{UI.WHITE}🔒 ENCRYPTED GATEWAY PANEL{UI.RESET}")
            print(f" [{UI.GREEN}1{UI.RESET}] Login Identity Node")
            print(f" [{UI.GREEN}2{UI.RESET}] Register Identity Node")
            print(f" [{UI.GREEN}3{UI.RESET}] Exit")
            
            op = input(f"\n{UI.CYAN}TerminalChat ➔ {UI.RESET}").strip()
            if op == "1":
                self.login_node()
            elif op == "2":
                self.register_node()
            elif op == "3":
                sys.exit(0)

    def login_node(self):
        UI.clear()
        UI.banner()
        print(f"\n{UI.BOLD}{UI.WHITE}👥 LOGIN GATEWAY{UI.RESET} (Ketik '-b' untuk kembali)")
        user = input(f"{UI.CYAN}➔ Username: {UI.RESET}").strip()
        if user == '-b': return
        passwd = input(f"{UI.CYAN}➔ Password: {UI.RESET}").strip()
        if passwd == '-b': return

        print(f"{UI.BLUE}[*] Sinkronisasi identitas global...{UI.RESET}")
        try:
            users = json.loads(self.storage.read_node(self.user_registry, "user_registry.json"))
            hashed = hashlib.sha256(passwd.encode()).hexdigest()
            for u in users:
                if u["username"] == user and u["password"] == hashed:
                    self.session_user = {"username": u["username"], "nickname": u["nickname"]}
                    self.db_user.truncate()
                    self.db_user.insert(u)
                    self.main_dashboard()
                    return
            input(f"{UI.RED}[─] Kredensial salah. Tekan Enter...{UI.RESET}")
        except Exception as e:
            input(f"{UI.RED}[─] Gagal terhubung ke node cluster: {e}. Tekan Enter...{UI.RESET}")

    def register_node(self):
        UI.clear()
        UI.banner()
        print(f"\n{UI.BOLD}{UI.WHITE}📝 DAFTAR IDENTITAS BARU{UI.RESET} (Ketik '-b' untuk kembali)")
        user = input(f"{UI.CYAN}➔ Username : {UI.RESET}").strip()
        if user == '-b' or not user: return
        nick = input(f"{UI.CYAN}➔ Nickname : {UI.RESET}").strip()
        if nick == '-b' or not nick: return
        passwd = input(f"{UI.CYAN}➔ Password : {UI.RESET}").strip()
        if passwd == '-b' or not passwd: return

        try:
            users = json.loads(self.storage.read_node(self.user_registry, "user_registry.json"))
            if any(u["username"] == user for u in users):
                input(f"{UI.RED}[─] Username sudah terdaftar di jaringan global. Tekan Enter...{UI.RESET}")
                return
            
            users.append({
                "username": user,
                "nickname": nick,
                "password": hashlib.sha256(passwd.encode()).hexdigest()
            })
            self.storage.update_node(self.user_registry, "user_registry.json", json.dumps(users))
            print(f"{UI.GREEN}[✓] Registrasi sukses. Silakan lakukan login.{UI.RESET}")
            time.sleep(1.5)
        except Exception as e:
            input(f"{UI.RED}[─] Registrasi gagal: {e}. Tekan Enter...{UI.RESET}")

    def main_dashboard(self):
        while True:
            UI.clear()
            UI.banner()
            print(f"\n{UI.GRAY}Sesi Aktif: {UI.BOLD}{UI.GREEN}{self.session_user['nickname']}{UI.RESET} (@{self.session_user['username']})")
            print(f"\n{UI.BOLD}{UI.WHITE}🎛️ CORE PANEL OPERATIONS{UI.RESET}")
            print(f" [{UI.GREEN}1{UI.RESET}] Create Premium Room")
            print(f" [{UI.GREEN}2{UI.RESET}] Join Encrypted Room")
            print(f" [{UI.GREEN}3{UI.RESET}] History Connected Rooms")
            print(f" [{UI.GREEN}4{UI.RESET}] Clear Session & Logout")
            
            ch = input(f"\n{UI.CYAN}Dashboard ➔ {UI.RESET}").strip()
            if ch == "1":
                self.create_room_flow()
            elif ch == "2":
                self.join_room_flow()
            elif ch == "3":
                self.history_rooms_flow()
            elif ch == "4":
                self.db_user.truncate()
                self.session_user = None
                self.auth_gateway()
                return

    def create_room_flow(self):
        UI.clear()
        UI.banner()
        print(f"\n{UI.BOLD}{UI.WHITE}🧱 FORM PEMBUATAN ROOM SECURE{UI.RESET}")
        name = input(f"{UI.CYAN}➔ Nama Room     : {UI.RESET}").strip()
        passwd = input(f"{UI.CYAN}➔ Password Room : {UI.RESET}").strip()
        if not name or not passwd: return

        print(f"{UI.BLUE}[*] Mengalokasikan enkripsi isolasi klaster...{UI.RESET}")
        try:
            g_id = self.storage.create_node(f"{name}.json", "[]")
            r_id = str(int(time.time()))[-7:]
            
            meta = {
                "room_id": r_id,
                "room_name": name,
                "gist_id": g_id,
                "password_verify_hash": hashlib.sha256(passwd.encode()).hexdigest()
            }
            
            rooms = json.loads(self.storage.read_node(self.room_registry, "room_registry.json"))
            rooms.append(meta)
            self.storage.update_node(self.room_registry, "room_registry.json", json.dumps(rooms))
            
            self.db_rooms.insert({"room_id": r_id, "room_name": name, "gist_id": g_id, "pass": passwd})
            print(f"\n{UI.GREEN}[✓] Ruang Obrolan Terenkripsi Berhasil Dibuat!{UI.RESET}")
            print(f" ROOM ID  : {UI.BOLD}{UI.YELLOW}{r_id}{UI.RESET}")
            print(f" PASSWORD : {UI.BOLD}{UI.YELLOW}{passwd}{UI.RESET}")
            input(f"\nTekan Enter untuk melanjutkan...")
        except Exception as e:
            input(f"{UI.RED}[─] Pembuatan room gagal: {e}. Tekan Enter...{UI.RESET}")

    def join_room_flow(self):
        UI.clear()
        UI.banner()
        print(f"\n{UI.BOLD}{UI.WHITE}🔑 MERGE TO ENCRYPTED CHANNEL{UI.RESET}")
        r_id = input(f"{UI.CYAN}➔ Room ID  : {UI.RESET}").strip()
        passwd = input(f"{UI.CYAN}➔ Password : {UI.RESET}").strip()

        print(f"{UI.BLUE}[*] Menguji validitas keamanan kriptografi...{UI.RESET}")
        try:
            rooms = json.loads(self.storage.read_node(self.room_registry, "room_registry.json"))
            for r in rooms:
                if r["room_id"] == r_id:
                    if r["password_verify_hash"] == hashlib.sha256(passwd.encode()).hexdigest():
                        self.session_room = {
                            "room_id": r["room_id"],
                            "room_name": r["room_name"],
                            "gist_id": r["gist_id"],
                            "password": passwd
                        }
                        
                        Room = Query()
                        if not self.db_rooms.search(Room.room_id == r_id):
                            self.db_rooms.insert({"room_id": r["room_id"], "room_name": r["room_name"], "gist_id": r["gist_id"], "pass": passwd})
                        
                        self.chat_interface()
                        return
                    else:
                        input(f"{UI.RED}[─] Kunci sandi salah. Handshake ditolak. Tekan Enter...{UI.RESET}")
                        return
            input(f"{UI.RED}[─] Room ID tidak terdaftar atau telah kadaluarsa. Tekan Enter...{UI.RESET}")
        except Exception as e:
            input(f"{UI.RED}[─] Handshake error: {e}. Tekan Enter...{UI.RESET}")

    def history_rooms_flow(self):
        UI.clear()
        UI.banner()
        print(f"\n{UI.BOLD}{UI.WHITE}📂 RIWAYAT ROOM TERHUBUNG DI PERANGKAT INI{UI.RESET}")
        rooms = self.db_rooms.all()
        if not rooms:
            input(f"{UI.YELLOW}[!] Tidak ada riwayat koneksi. Tekan Enter...{UI.RESET}")
            return
            
        for i, r in enumerate(rooms, start=1):
            print(f" [{UI.GREEN}{i}{UI.RESET}] ID: {r['room_id']} | Nama Alias: {r['room_name']}")
        print(f" [{UI.RED}x{UI.RESET}] Kembali")
        
        ch = input(f"\nPilih Nomor ➔ {UI.RESET}").strip()
        if ch.lower() == 'x': return
        try:
            idx = int(ch) - 1
            if 0 <= idx < len(rooms):
                target = rooms[idx]
                self.session_room = {
                    "room_id": target["room_id"],
                    "room_name": target["room_name"],
                    "gist_id": target["gist_id"],
                    "password": target["pass"]
                }
                self.chat_interface()
        except (ValueError, IndexError):
            pass

    def chat_interface(self):
        self.chat_active = True
        UI.clear()
        UI.banner()
        print(f"\n{UI.BG_DARK}{UI.WHITE}{UI.BOLD} ENCRYPTED CHANNEL: {self.session_room['room_name'].upper()} | NODE ID: {self.session_room['room_id']} {UI.RESET}")
        print(f"{UI.GRAY}Ketik ':q' untuk memutus koneksi, ketik ':r' untuk me-refresh layar.{UI.RESET}\n")
        print(f"{UI.GRAY}─" * 75 + f"{UI.RESET}")

        threading.Thread(target=self._listener_thread, daemon=True).start()

        while self.chat_active:
            try:
                inp = input().strip()
                if not inp: continue
                if inp.lower() == ':q':
                    self.chat_active = False
                    break
                elif inp.lower() == ':r':
                    UI.clear()
                    UI.banner()
                    print(f"\n{UI.BG_DARK}{UI.WHITE}{UI.BOLD} ENCRYPTED CHANNEL: {self.session_room['room_name'].upper()} | NODE ID: {self.session_room['room_id']} {UI.RESET}")
                    print(f"{UI.GRAY}─" * 75 + f"{UI.RESET}")
                    continue

                sys.stdout.write("\033[F\033[K")
                sys.stdout.flush()

                self._send_payload(inp)
            except (KeyboardInterrupt, EOFError):
                self.chat_active = False
                break
        self.session_room = None

    def _send_payload(self, text: str):
        try:
            fn = f"{self.session_room['room_name']}.json"
            raw = self.storage.read_node(self.session_room["gist_id"], fn)
            msg_list = json.loads(raw)
            
            packet = {
                "sender": self.session_user["nickname"],
                "username": self.session_user["username"],
                "text": text,
                "timestamp": time.strftime("%H:%M:%S")
            }
            
            enc_packet = CryptoEngine.encrypt(json.dumps(packet), self.session_room["password"])
            msg_list.append(enc_packet)
            self.storage.update_node(self.session_room["gist_id"], fn, json.dumps(msg_list))
        except Exception as e:
            print(f"{UI.RED}[─] Pengiriman pesan gagal (Network Error): {e}{UI.RESET}")

    def _listener_thread(self):
        ptr = 0
        fn = f"{self.session_room['room_name']}.json"
        while self.chat_active:
            try:
                raw = self.storage.read_node(self.session_room["gist_id"], fn)
                msg_list = json.loads(raw)
                if len(msg_list) > ptr:
                    for pack in msg_list[ptr:]:
                        plain = CryptoEngine.decrypt(pack, self.session_room["password"])
                        if plain:
                            m = json.loads(plain)
                            if m["username"] == self.session_user["username"]:
                                print(f" {UI.GRAY}[{m['timestamp']}]{UI.RESET} {UI.GREEN}{UI.BOLD}Anda{UI.RESET} : {m['text']}")
                            else:
                                print(f" {UI.GRAY}[{m['timestamp']}]{UI.RESET} {UI.BLUE}{UI.BOLD}{m['sender']}{UI.RESET} : {m['text']}")
                        else:
                            print(f" {UI.RED}[─] Data korup atau password room ilegal terdeteksi.{UI.RESET}")
                    ptr = len(msg_list)
            except Exception:
                pass
            time.sleep(1.8)

if __name__ == "__main__":
    try:
        app = TerminalChatApp()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\033[91m[-] Koneksi TerminalChat diputus.\033[0m")
        sys.exit(0)
