# ==========================================
# LATIHAN 1 - SUBSTITUSI CIPHER
# ==========================================

def substitusi_cipher(plaintext, aturan):
    hasil = ""
    for char in plaintext.upper():
        hasil += aturan.get(char, char)
    return hasil


print("== LATIHAN 1: SUBSTITUSI CIPHER ==")
plaintext = input("Masukkan plaintext: ").upper()

aturan = {}
jumlah = int(input("Berapa banyak aturan substitusi? "))

for i in range(jumlah):
    huruf_asli = input(f"Masukkan huruf asli ke-{i+1}: ").upper()
    huruf_ganti = input(f"Ganti '{huruf_asli}' dengan: ").upper()
    aturan[huruf_asli] = huruf_ganti

ciphertext = substitusi_cipher(plaintext, aturan)
print("\n=== HASIL SUBSTITUSI CIPHER ===")
print(f"Plaintext  : {plaintext}")
print(f"Ciphertext : {ciphertext}")
print("================================")
