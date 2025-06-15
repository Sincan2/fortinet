````markdown
# 🔥 Sincan2 Fortinet Exploitation Framework

(demo.png)

## 💡 Alur Kerja Tool

Sincan2 menggunakan arsitektur **modular** yang memisahkan antarmuka pengguna, mesin utama, dan logika eksploitasi demi kemudahan penggunaan dan pengembangan.

### 🧩 Komponen Utama

#### `sodok.sh` - Antarmuka Pengguna (Runner)
- Titik masuk utama.
- Menu interaktif untuk memilih mode pindai (Tunggal / Massal).
- Deteksi otomatis kunci SSH dan IP publik untuk saran default.
- Mengumpulkan semua parameter dari pengguna.
- Konfirmasi sebelum eksploitasi yang memerlukan listener.
- Membangun dan mengeksekusi perintah akhir ke `sincan2.py`.

#### `sincan2.py` - (Core Engine)
- Menerima argumen dari `sodok.sh` atau langsung dari CLI.
- Mengelola daftar target tunggal atau dari file.
- Memanggil fungsi eksploitasi dari `_exploits.py` secara berurutan.
- Melewati pengujian CVE jika parameter tidak lengkap (contoh: `--forti-ssh-key`, `--reverse-host`).
- Menampilkan status real-time: Rentan, Tidak Rentan, Error, atau Dilewati.

#### `_exploits.py` - Eksploitasi
- Berisi implementasi teknis untuk setiap CVE Fortinet yang didukung.
- Tiap fungsi menerima target + argumen, mengembalikan hasil terstruktur.
- Fokus pada logika eksploitasi — **tidak menangani antarmuka**.

---

## 🛡️ Dukungan Kerentanan (CVE)

| CVE ID            | Deskripsi                                   | Tipe Eksploitasi         |
|-------------------|----------------------------------------------|---------------------------|
| CVE-2022-40684    | Authentication Bypass                        | Penambahan Kunci SSH      |
| CVE-2022-42475    | Pre-Auth RCE di SSL-VPN                      | Crash Test                |
| CVE-2023-27997    | Heap-based Buffer Overflow di SSL-VPN       | Reverse Shell             |
| CVE-2024-21762    | Out-of-Bounds Write di SSL-VPN              | Reverse Shell / DNS Call |

---

## 🛠️ Instalasi

### 1. Prasyarat
Pastikan sistem memiliki:
- `git`
- `python3`
- `pip`
- `curl`

### 2. Kloning Repositori
```bash
git clone https://github.com/Sincan2/fortinet.git
cd fortinet
````

### 3. Instal Dependensi

```bash
pip install -r requirements.txt
```

Jika `requirements.txt` belum tersedia, buat dengan isi:

```txt
requests
pwntools
pycryptodome
urllib3
```

---

## 🏃‍♂️ Cara Menjalankan

Jalankan tool melalui skrip utama:

```bash
./sodok.sh
```

### Langkah:

1. **Pilih Mode**: Target Tunggal atau Massal.
2. **Masukkan Detail**: URL/IP atau file daftar, port, dll.
3. **Konfigurasi Parameter**: Isi interaktif, auto-saran untuk kunci SSH dan IP publik.
4. **Konfirmasi Listener**: Siapkan listener bila eksploitasi membutuhkannya.
5. **Analisis Hasil**: Tool menampilkan laporan semua uji CVE secara langsung.

---

## ⚠️ Disclaimer

> Alat ini dibuat **hanya untuk tujuan pendidikan dan audit keamanan yang sah**.
> **Dilarang keras** menggunakan tool ini di luar sistem yang Anda miliki izin eksplisit.
> Penggunaan tanpa otorisasi dapat melanggar hukum di yurisdiksi Anda.

---

## 👥 Dikembangkan oleh

**MHL TEAM**

```

---

**Petunjuk Upload `demo.png`:**
- Simpan gambar demo di direktori utama repo (`/fortinet/demo.png`).
- Pastikan `README.md` dan `demo.png` ada di root repo agar tampilan gambar langsung muncul.

Jika Anda butuh versi siap pakai (file `.md` dan `demo.png` dalam satu folder ZIP), beri tahu saya agar saya bantu buatkan.
```
