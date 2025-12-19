import random

def mod_inverse(a, p):
    return pow(a, -1, p)

def text_to_numbers(text):
    return [ord(c) - 64 for c in text]   # A=1 ... Z=26

def numbers_to_text(nums):
    return ''.join(chr(n + 64) for n in nums)

# ===============================
# PROSES 1 : PEMBANGKITAN KUNCI
# ===============================

def proses_1_key_generation(p, g):
    print("\n===============================")
    print("PROSES 1 : PEMBANGKITAN KUNCI")
    print("===============================")

    print("\nRumus:")
    print("1. Pilih bilangan prima p")
    print("2. Pilih bilangan acak x, dengan 1 ≤ x ≤ p-2")
    print("3. Hitung y = g^x mod p")

    x = random.randint(2, p - 2)
    y = pow(g, x, p)

    print("\nSubstitusi:")
    print(f"x = {x}")
    print(f"y = {g}^{x} mod {p}")
    print(f"y = {y}")

    print("\nHasil:")
    print("Kunci Publik  (y, g, p) :", (y, g, p))
    print("Kunci Privat  (x, p)    :", (x, p))

    return (p, g, y), x

# ===============================
# PROSES 2 : ENKRIPSI
# ===============================

def proses_2_enkripsi(plaintext, public_key):
    print("\n===============================")
    print("PROSES 2 : ENKRIPSI")
    print("===============================")

    p, g, y = public_key

    print("\nRumus:")
    print("1. Bagi plaintext menjadi blok m1, m2, ..., mn")
    print("2. Pilih bilangan acak k, dengan 1 ≤ k ≤ p-2")
    print("3. Hitung:")
    print("   a = g^k mod p")
    print("   b = y^k · m mod p")

    m_blocks = text_to_numbers(plaintext)
    k = random.randint(2, p - 2)
    a = pow(g, k, p)

    print("\nPlaintext            :", plaintext)
    print("Blok plaintext (m)   :", m_blocks)
    print(f"Nilai k              : {k}")
    print(f"a = {g}^{k} mod {p} = {a}")

    cipher = []
    print("\nPerhitungan setiap blok:")
    for m in m_blocks:
        b = (pow(y, k, p) * m) % p
        print(f"b = {y}^{k} × {m} mod {p} = {b}")
        cipher.append((a, b))

    print("\nCiphertext (a, b):")
    print(cipher)

    return cipher

# ===============================
# PROSES 3 : DEKRIPSI
# ===============================

def proses_3_dekripsi(ciphertext, private_key, p):
    print("\n===============================")
    print("PROSES 3 : DEKRIPSI")
    print("===============================")

    print("\nRumus:")
    print("1. Hitung s = a^x mod p")
    print("2. Hitung s⁻¹ = (a^x)⁻¹ mod p")
    print("3. Hitung m = b × s⁻¹ mod p")

    hasil = []
    print("\nPerhitungan setiap blok:")
    for a, b in ciphertext:
        s = pow(a, private_key, p)
        s_inv = mod_inverse(s, p)
        m = (b * s_inv) % p

        print(f"s   = {a}^{private_key} mod {p} = {s}")
        print(f"s⁻¹ = {s_inv}")
        print(f"m   = {b} × {s_inv} mod {p} = {m}\n")

        hasil.append(m)

    plaintext = numbers_to_text(hasil)

    print("Hasil blok angka :", hasil)
    print("Plaintext hasil  :", plaintext)


print("=== PROGRAM ELGAMAL ===")

# INPUT USER (HANYA p dan g)
p = int(input("Masukkan bilangan prima p : "))
g = int(input("Masukkan generator g      : "))

plaintext = "YUSTRIINSANI"

# PROSES 1
public_key, private_key = proses_1_key_generation(p, g)

# PROSES 2
ciphertext = proses_2_enkripsi(plaintext, public_key)

# PROSES 3
proses_3_dekripsi(ciphertext, private_key, p)
