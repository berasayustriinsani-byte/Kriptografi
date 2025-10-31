# Latihan No.2 - Substitusi + Transposisi (4 blok)
from math import ceil

# Aturan substitusi
aturan = {
    'U': 'K',
    'N': 'N',
    'I': 'I',
    'K': 'K',
    'A': 'B'
}

def substitusi(plaintext, aturan):
    """Melakukan substitusi huruf sesuai aturan."""
    hasil = ""
    for ch in plaintext.upper():
        hasil += aturan.get(ch, ch)  # biarkan karakter lain tetap sama
    return hasil

def transposisi_4blok(text):
    """Membagi teks menjadi 4 blok dan melakukan transposisi kolom."""
    # hapus spasi sebelum diproses
    text = text.replace(" ", "")
    n = len(text)
    part_len = max(1, ceil(n / 4))
    parts = [text[i:i + part_len] for i in range(0, n, part_len)]
    maxcol = max(len(p) for p in parts)

    hasil = ""
    for col in range(maxcol):
        for p in parts:
            if col < len(p):
                hasil += p[col]
    return hasil

# === Program utama ===
print("=== LATIHAN 2 - SUBSTITUSI + TRANSPOSISI (4 BLOK) ===")
plaintext = input("Masukkan plaintext: ").upper()

# Proses substitusi
cipher_subs = substitusi(plaintext, aturan)

# Proses transposisi (tanpa spasi)
cipher_trans = transposisi_4blok(cipher_subs)

# Tampilkan hasil
print("\nHasil:")
print(f"Plaintext                     : {plaintext}")
print(f"Ciphertext (Substitusi)       : {cipher_subs}")
print(f"Ciphertext (Substitusi+Trans) : {cipher_trans}")
