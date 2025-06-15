<h1 align="center">Sincan2 - Fortinet Exploit Toolkit</h1>

<p align="center">
  Sebuah toolkit yang sangat efisien, dirancang untuk mengotomatiskan proses eksploitasi yang seringkali rumit. Dilengkapi dengan runner Bash yang cerdas.
</p>

---

### 🚀 Fitur Unggulan

* **Runner Bash Cerdas (`sodok.sh`)**: Antarmuka berbasis menu yang intuitif untuk memandu Anda melalui setiap langkah, dari pengaturan parameter hingga eksekusi.
* **Deteksi IP Publik Otomatis**: Secara otomatis mendeteksi dan mengurangi kesalahan input dengan menyarankan IP publik Anda untuk *callback* dan *reverse shell*.
* **Deteksi Kunci SSH Otomatis**: Mencari kunci SSH (`id_rsa.pub` / `id_ed25519.pub`) di direktori `~/.ssh/` untuk mempercepat proses eksploitasi CVE-2022-40684.
* **Mode Pindai Fleksibel**: Mendukung pemindaian pada target tunggal maupun massal dari sebuah file, cocok untuk audit skala kecil hingga besar.
* **Konfirmasi Pra-Eksploitasi**: Memberikan jeda konfirmasi sebelum meluncurkan eksploitasi yang memerlukan *listener*, memastikan Anda siap menerima koneksi masuk.

### 🛡️ Dukungan Kerentanan (CVE)

Saat ini, Sincan2 mendukung pengujian dan eksploitasi untuk kerentanan berikut:

-   CVE-2022-40684 (Authentication Bypass)
-   CVE-2022-42475 (SSL-VPN Pre-Authentication RCE)
-   CVE-2023-27997 (SSL-VPN Heap-based Buffer Overflow)
-   CVE-2024-21762 (SSL-VPN Out-of-Bounds Write)

---

### 🛠️ Instalasi

**1. Prasyarat**

Pastikan sistem Anda memiliki:
-   `git`
-   `python3`
-   `pip`
-   `curl` (direkomendasikan untuk deteksi IP otomatis)

**2. Kloning Repositori**

```bash
git clone [https://github.com/Sincan2/fortinet.git](https://github.com/Sincan2/fortinet.git)
cd fortinet
3. Instal DependensiJalankan perintah berikut untuk menginstal pustaka Python yang diperlukan.pip install -r requirements.txt
Jika file requirements.txt belum ada, buat file tersebut dengan isi di bawah ini:# requirements.txt
requests
pwntools
pycryptodome
urllib3
🏃‍♂️ Cara MenjalankanSeluruh operasi dijalankan melalui skrip runner sodok.sh.bash sodok.sh
Anda akan disambut dengan menu utama:==================== SINCAN2 FORTINET RUNNER ====================

  [1] Mulai Pindai Target Tunggal
  [2] Mulai Pindai Massal dari File

  [3] Keluar

================================================================
Contoh Skenario: Eksploitasi Target TunggalPilih opsi [1] dari menu.Masukkan URL Target: Masukkan URL lengkap target (misal: https://192.168.10.50:10443).Pengaturan Parameter: Skrip akan memandu Anda melalui serangkaian pertanyaan cerdas.Kunci SSH: Skrip akan menawarkan kunci yang ditemukan di ~/.ssh/. Cukup tekan y untuk konfirmasi.IP Publik: IP publik Anda akan disarankan sebagai default. Cukup tekan [ENTER] untuk menggunakannya.Listener: Masukkan port yang Anda gunakan pada nc. Jika Anda mengisi parameter ini, skrip akan berhenti sejenak dan meminta Anda memastikan nc -lnvp <port> sudah berjalan sebelum melanjutkan.Eksekusi: Skrip akan secara otomatis menjalankan semua tes CVE yang relevan berdasarkan parameter yang Anda berikan.⚠️ DisclaimerAlat ini dibuat untuk tujuan pendidikan dan pengujian keamanan yang sah. Pengguna bertanggung jawab penuh atas tindakan mereka. Jangan pernah menggunakan alat ini pada sistem yang tidak Anda miliki izin eksplisit untuk mengujinya. Penulis dan kontributor tidak bertanggung jawab atas penyalahgunaan atau kerusakan yang disebabkan oleh program ini.
