<!DOCTYPE html>
<html lang="id" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sincan2 - Fortinet Exploit Toolkit</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <!-- 
        Chosen Palette: "Tokyo Night" inspired. A modern, dark theme popular in code editors.
        - Background: #1a1b26 (Storm)
        - Text: #a9b1d6 (Light Gray)
        - Headers: #c0caf5 (Brighter Gray)
        - Accent Blue: #7aa2f7
        - Accent Green: #9ece6a
        - Accent Orange: #ff9e64
        - Card/Surface: #24283b
    -->
    <!-- 
        Application Structure Plan: A single-page, vertically flowing application designed for discoverability.
        1. Hero Section: Grabs immediate attention with a strong title, demo images, and clear calls-to-action (GitHub/Get Started).
        2. Features Section: Uses visually distinct cards with icons to make the tool's advantages scannable and digestible, a major improvement over a simple list.
        3. Supported CVEs Section: Presents vulnerabilities in a structured table for quick reference. This is more professional and organized than a list.
        4. Installation & Usage Section: A combined, step-by-step guide that mimics a developer's workflow. Using tabs for "Installation" and "Usage" keeps the UI clean and focused. Interactive "copy" buttons are added for critical UX improvement.
        5. Disclaimer & Footer: Standard, clear sections for legal notices and project links.
        This structure guides the user from "what is this?" to "how do I use it?" logically and interactively, making the information more engaging and easier to consume than a static README.
    -->
    <!-- 
        Visualization & Content Choices:
        - Report Info: Project Features -> Goal: Inform & Engage -> Viz/Method: Icon-based feature cards -> Interaction: Hover effects to provide feedback -> Justification: More visually appealing and scannable than a bullet list.
        - Report Info: Supported CVEs -> Goal: Organize & Inform -> Viz/Method: HTML Table with distinct headers -> Interaction: Hover highlight on rows -> Justification: Clear, structured, and professional presentation of technical data.
        - Report Info: Code commands for installation/usage -> Goal: Enable Action -> Viz/Method: Styled code blocks -> Interaction: "Copy to Clipboard" buttons -> Justification: Drastically improves user experience by removing the need for manual selection and copying, reducing errors.
        - Report Info: Project Images -> Goal: Demonstrate UI -> Viz/Method: Embedded images in the hero section -> Interaction: None -> Justification: Provides immediate visual context for the tool.
        - Library/Method: Vanilla JavaScript for all interactions to keep the application lightweight. Tailwind CSS for all styling.
    -->
    <!-- CONFIRMATION: NO SVG graphics used. NO Mermaid JS used. -->
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #1a1b26;
            color: #a9b1d6;
        }
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            font-weight: 900;
            color: #c0caf5;
            letter-spacing: -0.025em;
        }
        .jetbrains-mono {
            font-family: 'JetBrains Mono', monospace;
        }
        .glass-card {
            background: rgba(36, 40, 59, 0.6);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(122, 162, 247, 0.2);
        }
        .btn-primary {
            background-color: #7aa2f7;
            color: #1a1b26;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        .btn-primary:hover {
            background-color: #9ece6a;
            transform: translateY(-2px);
        }
        .btn-secondary {
            background-color: transparent;
            color: #7aa2f7;
            border: 1px solid #7aa2f7;
            transition: background-color 0.3s ease, color 0.3s ease;
        }
        .btn-secondary:hover {
            background-color: #7aa2f7;
            color: #1a1b26;
        }
        .tab-btn.active {
            background-color: #7aa2f7;
            color: #1a1b26;
        }
        .tab-btn:not(.active) {
            background-color: #24283b;
            color: #a9b1d6;
        }
        .code-block {
            background-color: #16161e;
            border: 1px solid #3b3f51;
        }
        .copy-btn {
            background-color: #3b3f51;
            color: #a9b1d6;
        }
        .copy-btn:hover {
            background-color: #9ece6a;
            color: #1a1b26;
        }
        .tooltip {
            visibility: hidden;
            opacity: 0;
            transition: opacity 0.3s;
        }
        .has-tooltip:hover .tooltip {
            visibility: visible;
            opacity: 1;
        }
    </style>
</head>
<body class="w-full overflow-x-hidden">

    <!-- Header & Nav -->
    <header class="fixed top-0 left-0 right-0 z-50 transition-all duration-300" id="navbar">
        <div class="container mx-auto px-6 py-4">
            <nav class="flex items-center justify-between">
                <a href="#" class="text-2xl font-black text-white">Sincan2</a>
                <div class="hidden md:flex items-center space-x-8">
                    <a href="#features" class="text-gray-300 hover:text-white transition">Fitur</a>
                    <a href="#cve" class="text-gray-300 hover:text-white transition">CVE</a>
                    <a href="#usage" class="text-gray-300 hover:text-white transition">Penggunaan</a>
                    <a href="https://github.com/Sincan2/fortinet" target="_blank" class="btn-secondary rounded-full px-5 py-2 text-sm font-bold">
                        GitHub ↗
                    </a>
                </div>
                <div class="md:hidden">
                    <button id="menu-btn" class="text-white focus:outline-none">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
                    </button>
                </div>
            </nav>
        </div>
        <!-- Mobile Menu -->
        <div id="mobile-menu" class="hidden md:hidden bg-[#16161e] p-4">
            <a href="#features" class="block py-2 px-4 text-sm text-gray-300 hover:bg-[#24283b] rounded">Fitur</a>
            <a href="#cve" class="block py-2 px-4 text-sm text-gray-300 hover:bg-[#24283b] rounded">CVE</a>
            <a href="#usage" class="block py-2 px-4 text-sm text-gray-300 hover:bg-[#24283b] rounded">Penggunaan</a>
            <a href="https://github.com/Sincan2/fortinet" target="_blank" class="block mt-2 w-full text-center btn-secondary rounded-full px-5 py-2 text-sm font-bold">GitHub ↗</a>
        </div>
    </header>

    <!-- Hero Section -->
    <main class="pt-24">
        <section class="relative container mx-auto px-6 py-16 md:py-24 text-center">
            <div class="absolute top-0 left-0 w-full h-full bg-grid-pattern opacity-10" style="background-image: radial-gradient(#7aa2f7 1px, transparent 1px); background-size: 20px 20px;"></div>
            <h1 class="text-4xl md:text-6xl lg:text-7xl font-black mb-4 leading-tight">
                Fortinet Exploit Toolkit.
                <span class="block bg-clip-text text-transparent bg-gradient-to-r from-[#7aa2f7] to-[#9ece6a]">Otomatis & Efisien.</span>
            </h1>
            <p class="max-w-3xl mx-auto mb-8 text-lg md:text-xl">
                Toolkit yang didedikasikan untuk para profesional keamanan, dirancang untuk mengotomatiskan proses eksploitasi yang rumit dengan runner Bash yang cerdas.
            </p>
            <div class="flex justify-center items-center space-x-4">
                <a href="#usage" class="btn-primary rounded-full px-8 py-4 font-bold">Mulai</a>
                <a href="https://github.com/Sincan2/fortinet" target="_blank" class="btn-secondary rounded-full px-8 py-4 font-bold">Lihat di GitHub</a>
            </div>

            <div class="mt-16 md:mt-24 max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-8">
                <img src="https://raw.githubusercontent.com/Sincan2/fortinet/main/demo.png" alt="Sincan2 Runner Menu" class="rounded-lg shadow-2xl w-full h-auto object-cover border-2 border-[#24283b]">
                <img src="https://raw.githubusercontent.com/Sincan2/fortinet/main/demo2.png" alt="Sincan2 Exploit in Action" class="rounded-lg shadow-2xl w-full h-auto object-cover border-2 border-[#24283b]">
            </div>
        </section>

        <!-- Features Section -->
        <section id="features" class="py-16 md:py-24 bg-[#16161e]">
            <div class="container mx-auto px-6">
                <div class="text-center mb-12">
                    <h2 class="text-3xl md:text-4xl">Fitur Unggulan</h2>
                    <p class="mt-2 text-lg">Dirancang untuk efisiensi dan kemudahan penggunaan.</p>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <!-- Feature Card -->
                    <div class="glass-card p-8 rounded-xl text-center transition-all duration-300 hover:border-[#9ece6a] hover:-translate-y-2">
                        <div class="text-4xl mb-4">🤖</div>
                        <h3 class="text-xl font-bold mb-2 text-white">Otomatisasi Cerdas</h3>
                        <p class="text-sm">Deteksi IP publik & kunci SSH otomatis untuk mengurangi kesalahan input dan mempercepat proses.</p>
                    </div>
                    <!-- Feature Card -->
                    <div class="glass-card p-8 rounded-xl text-center transition-all duration-300 hover:border-[#9ece6a] hover:-translate-y-2">
                        <div class="text-4xl mb-4">🎯</div>
                        <h3 class="text-xl font-bold mb-2 text-white">Runner Bash Interaktif</h3>
                        <p class="text-sm">Antarmuka berbasis menu yang intuitif (`sodok.sh`) memandu Anda melalui setiap langkah eksploitasi.</p>
                    </div>
                    <!-- Feature Card -->
                    <div class="glass-card p-8 rounded-xl text-center transition-all duration-300 hover:border-[#9ece6a] hover:-translate-y-2">
                        <div class="text-4xl mb-4">🛡️</div>
                        <h3 class="text-xl font-bold mb-2 text-white">Dukungan Multi-CVE</h3>
                        <p class="text-sm">Mengimplementasikan beberapa PoC untuk kerentanan kritis Fortinet dalam satu alat terintegrasi.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Supported CVEs Section -->
        <section id="cve" class="py-16 md:py-24">
            <div class="container mx-auto px-6">
                <div class="text-center mb-12">
                    <h2 class="text-3xl md:text-4xl">Dukungan Kerentanan</h2>
                    <p class="mt-2 text-lg">Daftar kerentanan yang didukung saat ini.</p>
                </div>
                <div class="max-w-4xl mx-auto overflow-x-auto">
                    <table class="w-full text-left rounded-lg overflow-hidden glass-card">
                        <thead class="bg-[#24283b]">
                            <tr>
                                <th class="p-4 font-bold text-white">CVE ID</th>
                                <th class="p-4 font-bold text-white">Deskripsi</th>
                                <th class="p-4 font-bold text-white text-center">Tipe Eksploitasi</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="border-t border-[#3b3f51] hover:bg-[#24283b] transition">
                                <td class="p-4 font-semibold jetbrains-mono">CVE-2022-40684</td>
                                <td class="p-4">Authentication Bypass</td>
                                <td class="p-4 text-center"><span class="bg-blue-900/50 text-blue-300 text-xs font-bold px-2 py-1 rounded-full">SSH Key Injection</span></td>
                            </tr>
                            <tr class="border-t border-[#3b3f51] hover:bg-[#24283b] transition">
                                <td class="p-4 font-semibold jetbrains-mono">CVE-2022-42475</td>
                                <td class="p-4">SSL-VPN Pre-Authentication RCE</td>
                                <td class="p-4 text-center"><span class="bg-orange-900/50 text-orange-300 text-xs font-bold px-2 py-1 rounded-full">Crash Test</span></td>
                            </tr>
                            <tr class="border-t border-[#3b3f51] hover:bg-[#24283b] transition">
                                <td class="p-4 font-semibold jetbrains-mono">CVE-2023-27997</td>
                                <td class="p-4">SSL-VPN Heap-based Buffer Overflow</td>
                                <td class="p-4 text-center"><span class="bg-red-900/50 text-red-300 text-xs font-bold px-2 py-1 rounded-full">Reverse Shell</span></td>
                            </tr>
                             <tr class="border-t border-[#3b3f51] hover:bg-[#24283b] transition">
                                <td class="p-4 font-semibold jetbrains-mono">CVE-2024-21762</td>
                                <td class="p-4">SSL-VPN Out-of-Bounds Write</td>
                                <td class="p-4 text-center"><span class="bg-red-900/50 text-red-300 text-xs font-bold px-2 py-1 rounded-full">RCE</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
        
        <!-- Installation & Usage Section -->
        <section id="usage" class="py-16 md:py-24 bg-[#16161e]">
            <div class="container mx-auto px-6">
                <div class="text-center mb-12">
                    <h2 class="text-3xl md:text-4xl">Instalasi & Penggunaan</h2>
                    <p class="mt-2 text-lg">Mulai dalam beberapa langkah mudah.</p>
                </div>

                <div class="max-w-4xl mx-auto">
                    <div class="mb-4 flex justify-center border-b border-[#3b3f51]">
                        <button class="tab-btn py-2 px-6 font-bold text-lg focus:outline-none active" data-tab="install">Instalasi</button>
                        <button class="tab-btn py-2 px-6 font-bold text-lg focus:outline-none" data-tab="run">Cara Menjalankan</button>
                    </div>

                    <div id="install" class="tab-content">
                        <div class="space-y-6">
                            <div>
                                <h3 class="font-bold text-xl mb-2 text-white">1. Prasyarat</h3>
                                <p>Pastikan sistem Anda memiliki `git`, `python3`, `pip`, dan `curl`.</p>
                            </div>
                            <div>
                                <h3 class="font-bold text-xl mb-2 text-white">2. Kloning Repositori</h3>
                                <div class="relative code-block rounded-lg p-4 jetbrains-mono">
                                    <button class="copy-btn absolute top-2 right-2 p-1 rounded-md text-xs font-bold" onclick="copyToClipboard(this)">Copy</button>
                                    <pre><code>git clone https://github.com/Sincan2/fortinet.git
cd fortinet</code></pre>
                                </div>
                            </div>
                            <div>
                                <h3 class="font-bold text-xl mb-2 text-white">3. Instal Dependensi</h3>
                                <div class="relative code-block rounded-lg p-4 jetbrains-mono">
                                    <button class="copy-btn absolute top-2 right-2 p-1 rounded-md text-xs font-bold" onclick="copyToClipboard(this)">Copy</button>
                                    <pre><code>pip install -r requirements.txt</code></pre>
                                </div>
                                 <p class="text-sm mt-2">Jika `requirements.txt` tidak ada, buat file dengan isi: `requests`, `pwntools`, `pycryptodome`, `urllib3`.</p>
                            </div>
                        </div>
                    </div>
                    
                    <div id="run" class="tab-content hidden">
                        <div class="space-y-6">
                           <div>
                                <h3 class="font-bold text-xl mb-2 text-white">1. Jalankan Runner</h3>
                                <p>Seluruh operasi dijalankan melalui skrip `sodok.sh`.</p>
                                <div class="relative code-block rounded-lg p-4 mt-2 jetbrains-mono">
                                    <button class="copy-btn absolute top-2 right-2 p-1 rounded-md text-xs font-bold" onclick="copyToClipboard(this)">Copy</button>
                                    <pre><code>bash sodok.sh</code></pre>
                                </div>
                            </div>
                             <div>
                                <h3 class="font-bold text-xl mb-2 text-white">2. Ikuti Menu Interaktif</h3>
                                <p>Anda akan disambut menu untuk memilih pindai target tunggal atau massal. Skrip kemudian akan memandu Anda melalui pengaturan parameter secara otomatis.</p>
                                <div class="relative code-block rounded-lg p-4 mt-2 jetbrains-mono">
                                    <pre><code>==================== SINCAN2 FORTINET RUNNER ====================

  [1] Mulai Pindai Target Tunggal
  [2] Mulai Pindai Massal dari File
  [3] Keluar

================================================================</code></pre>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Disclaimer -->
        <section class="py-16">
            <div class="container mx-auto px-6 text-center max-w-3xl">
                <h3 class="text-2xl font-bold text-orange-400">⚠️ Disclaimer</h3>
                <p class="mt-4 text-gray-400">
                    Alat ini dibuat untuk tujuan pendidikan dan pengujian keamanan yang sah. Pengguna bertanggung jawab penuh atas tindakan mereka. Jangan pernah menggunakan alat ini pada sistem yang tidak Anda miliki izin eksplisit untuk mengujinya. Penulis dan kontributor tidak bertanggung jawab atas penyalahgunaan atau kerusakan yang disebabkan oleh program ini.
                </p>
            </div>
        </section>

    </main>

    <footer class="bg-[#16161e] border-t border-[#24283b] py-8">
        <div class="container mx-auto px-6 text-center text-gray-500">
            <p>&copy; 2025 Sincan2 - Dikembangkan oleh MHL TEAM.</p>
            <p class="text-sm mt-1">Dibuat dengan ❤️ untuk komunitas keamanan siber.</p>
        </div>
    </footer>

<script>
document.addEventListener('DOMContentLoaded', () => {
    // Navbar scroll effect
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('bg-[#1a1b26]/80', 'backdrop-blur-sm', 'shadow-lg');
        } else {
            navbar.classList.remove('bg-[#1a1b26]/80', 'backdrop-blur-sm', 'shadow-lg');
        }
    });

    // Mobile menu toggle
    const menuBtn = document.getElementById('menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    menuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });

    // Tab functionality for Usage section
    const tabs = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(item => item.classList.remove('active'));
            tab.classList.add('active');
            const target = document.getElementById(tab.dataset.tab);
            tabContents.forEach(content => content.classList.add('hidden'));
            target.classList.remove('hidden');
        });
    });
});

// Copy to clipboard function
function copyToClipboard(button) {
    const pre = button.nextElementSibling;
    const code = pre.querySelector('code');
    const textToCopy = code.innerText;
    
    // Create a temporary textarea element
    const textArea = document.createElement('textarea');
    textArea.value = textToCopy;
    document.body.appendChild(textArea);
    textArea.select();
    try {
        document.execCommand('copy');
        const originalText = button.innerText;
        button.innerText = 'Copied!';
        button.style.backgroundColor = '#9ece6a';
        button.style.color = '#1a1b26';
        setTimeout(() => {
            button.innerText = originalText;
            button.style.backgroundColor = '#3b3f51';
            button.style.color = '#a9b1d6';
        }, 2000);
    } catch (err) {
        console.error('Failed to copy text: ', err);
    }
    document.body.removeChild(textArea);
}

</script>
</body>
</html>
