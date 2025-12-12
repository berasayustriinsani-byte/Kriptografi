# Plaintext default: "YUSTRIINSANI"
import tkinter as tk
from tkinter import scrolledtext
import math
import random

# -------------------------
# Util: primality & random prime
# -------------------------
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r = int(math.isqrt(n))
    for i in range(3, r+1, 2):
        if n % i == 0:
            return False
    return True

def rand_prime(lo, hi):
    primes = [x for x in range(lo, hi+1) if is_prime(x)]
    if not primes:
        raise ValueError("Tidak ada prima di rentang")
    return random.choice(primes)

def extended_gcd_trace(a, b):
    steps = []
    def egcd(a, b):
        if b == 0:
            steps.append(f"gcd({a},{b}) -> {a} = {a}*1 + 0*0")
            return a, 1, 0
        q = a // b
        r = a % b
        steps.append(f"{a} = {b} * {q} + {r}")
        g, x1, y1 = egcd(b, r)
        x = y1
        y = x1 - q * y1
      
        steps.append(f"Back-sub: {g} = {a}*{x} + {b}*{y}")
        return g, x, y
    g, x, y = egcd(a, b)
    return g, x, y, steps

def modular_inverse(e, phi):
    g, x, y, steps = extended_gcd_trace(e, phi)
    if g != 1:
        return None, steps
    d = x % phi
    steps.append(f"Invers modular: d = {x} (mod {phi}) -> d = {d}")
    return d, steps


def rsa_params_from(p, q, e):
    n = p * q
    phi = (p-1)*(q-1)
    d, steps = modular_inverse(e, phi)
    return {'p':p,'q':q,'e':e,'n':n,'phi':phi,'d':d,'steps':steps}

def encrypt_text(text, e, n):
    c = [pow(ord(ch), e, n) for ch in text]
    return c

def decrypt_list(c_list, d, n):
    return ''.join(chr(pow(c, d, n)) for c in c_list)


class RSAPPTApp:
    def __init__(self, root):
        self.root = root
        root.title("RSA sesuai PPT — Latihan (GUI Tkinter)")
        root.geometry("950x650")

        top = tk.Frame(root)
        top.pack(padx=8, pady=6, fill='x')

        self.btn_lat1 = tk.Button(top, text="Jalankan Latihan 1 (p=17,q=11,e=7)", command=self.run_lat1)
        self.btn_lat1.pack(side='left', padx=4)

        self.btn_lat2 = tk.Button(top, text="Jalankan Latihan 2 (acak p,q di 50..200)", command=self.run_lat2)
        self.btn_lat2.pack(side='left', padx=4)


        self.btn_clear = tk.Button(top, text="Clear", command=self.clear)
        self.btn_clear.pack(side='right', padx=4)

        self.text = scrolledtext.ScrolledText(root, wrap='word', font=('Consolas', 11))
        self.text.pack(fill='both', expand=True, padx=8, pady=6)

        # default plaintext (seperti yang Anda minta)
        self.plaintext = "YUSTRIINSANI"

    def clear(self):
        self.text.delete('1.0', tk.END)

    def print_header(self, title):
        self.text.insert(tk.END, f"\n{'='*8} {title} {'='*8}\n")

    def run_lat1(self):
        self.clear()
        p = 17; q = 11; e = 7
        self.print_header("Latihan 1 (tetap)")
        self.text.insert(tk.END, f"Data (dari gambar/PPT): p={p}, q={q}, e={e}\n")
        info = rsa_params_from(p, q, e)
        n = info['n']; phi = info['phi']; d = info['d']
        self.text.insert(tk.END, f"1) Hitung n = p*q = {p}*{q} = {n}\n")
        self.text.insert(tk.END, f"2) Hitung phi(n) = (p-1)*(q-1) = {phi}\n\n")
        self.text.insert(tk.END, "3) Algoritma Euclidean (langkah) dan Back-substitution:\n")
        for s in info['steps']:
            self.text.insert(tk.END, f"   {s}\n")
        self.text.insert(tk.END, f"\n4) Diperoleh kunci privat d = {d}\n")
        self.text.insert(tk.END, f"   Kunci publik: (e,n)=({e},{n})\n   Kunci privat: (d,n)=({d},{n})\n\n")

        # proses enkripsi/dekripsi per PPT (per karakter)
        pt = self.plaintext
        self.text.insert(tk.END, f"5) Plaintext (diminta) = \"{pt}\"\n")
        ascii_list = [ord(ch) for ch in pt]
        self.text.insert(tk.END, f"   ASCII bytes = {ascii_list}\n")
        cipher = encrypt_text(pt, e, n)
        self.text.insert(tk.END, f"   Enkripsi (per char): {cipher}\n")
        dec = decrypt_list(cipher, d, n)
        self.text.insert(tk.END, f"   Dekripsi kembali (per char -> teks): {dec}\n")
        self.text.insert(tk.END, "\nSelesai Latihan 1 (semua langkah tampil seperti di PPT).\n")

    def run_lat2(self):
        self.clear()
        # pilih p,q acak (prima) di rentang 50..200 seperti PPT
        p = rand_prime(50,200)
        q = rand_prime(50,200)
        while q == p:
            q = rand_prime(50,200)
        # pilih e kecil coprime phi
        phi = (p-1)*(q-1)
        e = None
        for cand in [3,5,7,11,13,17,19,23,29,31,37]:
            if 1 < cand < phi and math.gcd(cand, phi) == 1:
                e = cand
                break
        if e is None:
            # fallback brute force
            for cand in range(3, phi, 2):
                if math.gcd(cand, phi) == 1:
                    e = cand
                    break

        self.print_header("Latihan 2 (acak p,q di 50..200)")
        self.text.insert(tk.END, f"Terpilih: p={p}, q={q}\n")
        info = rsa_params_from(p, q, e)
        n = info['n']; phi = info['phi']; d = info['d']
        self.text.insert(tk.END, f"1) n = {p}*{q} = {n}\n")
        self.text.insert(tk.END, f"2) phi(n) = {phi}\n")
        self.text.insert(tk.END, f"3) Dipilih e = {e}\n\n")
        self.text.insert(tk.END, "4) Langkah Euclidean + Back-substitution:\n")
        for s in info['steps']:
            self.text.insert(tk.END, f"   {s}\n")
        self.text.insert(tk.END, f"\n5) Diperoleh d = {d}\n")
        self.text.insert(tk.END, f"   Kunci publik: (e,n)=({e},{n})\n   Kunci privat: (d,n)=({d},{n})\n\n")

        # enkripsi/dekripsi
        pt = self.plaintext
        self.text.insert(tk.END, f"6) Plaintext = \"{pt}\"\n")
        ascii_list = [ord(ch) for ch in pt]
        self.text.insert(tk.END, f"   ASCII bytes = {ascii_list}\n")
        cipher = encrypt_text(pt, e, n)
        self.text.insert(tk.END, f"   Enkripsi (per char): {cipher}\n")
        dec = decrypt_list(cipher, d, n)
        self.text.insert(tk.END, f"   Dekripsi kembali: {dec}\n")
        self.text.insert(tk.END, "\nSelesai Latihan 2.\n")

    def run_both(self):
        # jalankan lat1 lalu lat2, tanpa clear di antaranya
        self.clear()
        self.run_lat1()
        self.run_lat2()

if __name__ == "__main__":
    root = tk.Tk()
    app = RSAPPTApp(root)
    root.mainloop()
