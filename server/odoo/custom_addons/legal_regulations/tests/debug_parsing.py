#!/usr/bin/env python3
"""
Debug script to test penjelasan parsing
"""
import re

txt = """
Pasal 13
(1) Setiap orang berhak menggunakan jasa Penyelenggara Sertifikasi Elektronik untuk pembuatan Tanda Tangan Elektronik.
(2) Penyelenggara Sertifikasi Elektronik harus memastikan keterkaitan suatu Tanda Tangan Elektronik dengan pemiliknya.
(3) Penyelenggara Sertifikasi Elektronik terdiri atas:
    a. Penyelenggara Sertifikasi Elektronik Indonesia; dan
    b. Penyelenggara Sertifikasi Elektronik asing.

Penjelasan

Penjelasan Pasal 13

Penjelasan Ayat (2)
Yang dimaksud dengan "perjanjian kerja sama" antara lain adalah perjanjian antarpenyelenggara sertifikasi elektronik atau antar pemerintah.

Penjelasan Ayat (3)
Ketentuan lebih lanjut mengenai Penyelenggara Sertifikasi Elektronik sebagaimana dimaksud pada ayat (3) diatur dengan Peraturan Pemerintah.

Pasal 14
(1) Penyelenggara Sertifikasi Elektronik sebagaimana dimaksud dalam Pasal 13 ayat (1) dan ayat (2) harus menyediakan informasi yang akurat.
"""

lines = txt.strip().split('\n')
penjelasan_mode = False
penjelasan_target = None
penjelasan_buffer = []

penjelasan_pasal_pat = re.compile(r'^Penjelasan Pasal\s+(\d+)$')
penjelasan_ayat_pat = re.compile(r'^Penjelasan Ayat\s+\((\d+)\)$')
pasal_pat = re.compile(r'^Pasal\s+(\d+)$')

current_pasal = None

for i, line in enumerate(lines):
    stripped = line.strip()
    print(f"Line {i}: '{stripped}' | penjelasan_mode={penjelasan_mode} | target={penjelasan_target}")
    
    if stripped == "Penjelasan":
        print("  -> ENTERING PENJELASAN MODE")
        penjelasan_mode = True
        if current_pasal:
            penjelasan_target = {'type': 'pasal', 'pasal': current_pasal}
            print(f"  -> Set target to pasal {current_pasal}")
        continue
    
    if penjelasan_mode:
        penjelasan_pasal_match = penjelasan_pasal_pat.match(stripped)
        penjelasan_ayat_match = penjelasan_ayat_pat.match(stripped)
        pasal_match = pasal_pat.match(stripped)
        
        if penjelasan_pasal_match:
            print(f"  -> PENJELASAN PASAL {penjelasan_pasal_match.group(1)} detected")
            if penjelasan_buffer:
                print(f"     Saving previous buffer: {' '.join(penjelasan_buffer[:50])}")
            penjelasan_buffer = []
            penjelasan_target = {'type': 'pasal', 'pasal': penjelasan_pasal_match.group(1)}
            
        elif penjelasan_ayat_match:
            print(f"  -> PENJELASAN AYAT {penjelasan_ayat_match.group(1)} detected")
            if penjelasan_buffer:
                print(f"     Saving previous buffer: {' '.join(penjelasan_buffer[:50])}")
            penjelasan_buffer = []
            if penjelasan_target:
                penjelasan_target = {
                    'type': 'ayat',
                    'pasal': penjelasan_target.get('pasal'),
                    'ayat': penjelasan_ayat_match.group(1)
                }
                print(f"     New target: {penjelasan_target}")
        
        elif pasal_match:
            print(f"  -> NEW PASAL {pasal_match.group(1)} - EXIT PENJELASAN MODE")
            print(f"     Final buffer: {' '.join(penjelasan_buffer)}")
            penjelasan_mode = False
            current_pasal = pasal_match.group(1)
            penjelasan_target = None
            penjelasan_buffer = []
        
        else:
            if stripped and stripped != "Penjelasan":
                penjelasan_buffer.append(stripped)
                print(f"     Buffer now: {len(penjelasan_buffer)} items")
    
    else:
        pasal_match = pasal_pat.match(stripped)
        if pasal_match:
            current_pasal = pasal_match.group(1)
            print(f"  -> PASAL {current_pasal} detected")
