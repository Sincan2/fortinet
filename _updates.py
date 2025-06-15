# File: _updates.py
# -*- coding: utf-8 -*-
"""
Modul dummy untuk memenuhi dependensi dari sincan2.py.
Fungsi di dalam file ini tidak melakukan apa-apa selain
memastikan skrip utama dapat berjalan tanpa error.
"""

global gl_http_pool

def set_http_pool(pool):
    """
    Fungsi dummy untuk menerima konfigurasi http pool.
    """
    global gl_http_pool
    gl_http_pool = pool

def check_updates():
    """
    Fungsi dummy. Selalu mengindikasikan tidak ada pembaruan.
    """
    return False

def auto_update():
    """
    Fungsi dummy. Selalu mengindikasikan tidak ada pembaruan yang terjadi.
    """
    return False
