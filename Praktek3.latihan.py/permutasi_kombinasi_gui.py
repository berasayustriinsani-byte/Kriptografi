import itertools
import math
import tkinter as tk
from tkinter import messagebox, scrolledtext

# === Fungsi matematika dasar ===
def faktorial(n):
    return math.factorial(n)

def permutasi_menyeluruh(elemen):
    return list(itertools.permutations(elemen))

def permutasi_sebagian(elemen, k):
    return list(itertools.permutations(elemen, k))

def kombinasi(elemen, r):
    return list(itertools.combinations(elemen, r))

def buku_di_rak(n, r):
    hasil = []
    def rekursif(temp):
        if len(temp) == n:
            hasil.append(temp.copy())
            return
        for i in range(1, r+1):
            temp.append(i)
            rekursif(temp)
            temp.pop()
    rekursif([])
    return hasil

# === GUI ===
window = tk.Tk()
window.title("PROGRAM PERMUTASI DAN KOMBINASI")
window.geometry("800x600")
window.configure(bg="#eaf0ff")

judul = tk.Label(window, text="PROGRAM PERMUTASI DAN KOMBINASI", font=("Arial Black", 14), bg="#eaf0ff", fg="#0a2a66")
judul.pack(pady=10)

output_box = scrolledtext.ScrolledText(window, width=90, height=20, font=("Consolas", 10))
output_box.pack(pady=10)

# === Input elemen ===
frame_input = tk.Frame(window, bg="#eaf0ff")
frame_input.pack()

tk.Label(frame_input, text="Masukkan elemen (pisahkan spasi):", bg="#eaf0ff").grid(row=0, column=0)
entry_elemen = tk.Entry(frame_input, width=40)
entry_elemen.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_input, text="k:", bg="#eaf0ff").grid(row=1, column=0)
entry_k = tk.Entry(frame_input, width=10)
entry_k.grid(row=1, column=1, sticky="w")

tk.Label(frame_input, text="n (buku):", bg="#eaf0ff").grid(row=2, column=0)
entry_n = tk.Entry(frame_input, width=10)
entry_n.grid(row=2, column=1, sticky="w")

tk.Label(frame_input, text="r (rak/kombinasi):", bg="#eaf0ff").grid(row=3, column=0)
entry_r = tk.Entry(frame_input, width=10)
entry_r.grid(row=3, column=1, sticky="w")

# === Fungsi tombol ===
def tampilkan_hasil(teks):
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, teks)

def aksi_permutasi_menyeluruh():
    data = entry_elemen.get().split()
    hasil = permutasi_menyeluruh(data)
    tampilkan_hasil("\n".join(str(x) for x in hasil))

def aksi_permutasi_sebagian():
    data = entry_elemen.get().split()
    try:
        k = int(entry_k.get())
        hasil = permutasi_sebagian(data, k)
        tampilkan_hasil("\n".join(str(x) for x in hasil))
    except:
        messagebox.showerror("Error", "Masukkan nilai k yang valid!")

def aksi_permutasi_keliling():
    data = entry_elemen.get().split()
    hasil = permutasi_menyeluruh(data)
    hasil_keliling = set()
    for p in hasil:
        keliling = tuple(sorted(p))
        hasil_keliling.add(keliling)
    tampilkan_hasil("\n".join(str(x) for x in hasil_keliling))

def aksi_permutasi_berkelompok():
    data_kelompok = entry_elemen.get().split(";")
    semua = []
    for grup in data_kelompok:
        elemen = grup.strip().split()
        semua.extend(elemen)
    hasil = permutasi_menyeluruh(semua)
    tampilkan_hasil("\n".join(str(x) for x in hasil))

def aksi_buku_di_rak():
    try:
        n = int(entry_n.get())
        r = int(entry_r.get())
        hasil = buku_di_rak(n, r)
        tampilkan_hasil(f"Jumlah cara: {len(hasil)}\n\n" + "\n".join(str(x) for x in hasil))
    except:
        messagebox.showerror("Error", "Masukkan n dan r yang valid!")

def aksi_kombinasi():
    try:
        n = int(entry_n.get())
        r = int(entry_r.get())
        huruf = [chr(65+i) for i in range(n)]
        hasil = kombinasi(huruf, r)
        tampilkan_hasil(f"Jumlah kombinasi: {len(hasil)}\n\n" + "\n".join(str(x) for x in hasil))
    except:
        messagebox.showerror("Error", "Masukkan n dan r yang valid!")

# === Tombol-tombol ===
frame_tombol = tk.Frame(window, bg="#eaf0ff")
frame_tombol.pack(pady=10)

tombol_data = [
    ("A. Permutasi Menyeluruh", aksi_permutasi_menyeluruh),
    ("B. Permutasi Sebagian", aksi_permutasi_sebagian),
    ("C. Permutasi Keliling", aksi_permutasi_keliling),
    ("D. Permutasi Berkelompok", aksi_permutasi_berkelompok),
    ("E. Buku di Rak", aksi_buku_di_rak),
    ("F. Kombinasi Huruf", aksi_kombinasi),
]

for i, (teks, aksi) in enumerate(tombol_data):
    tk.Button(frame_tombol, text=teks, width=25, height=2, bg="#0a2a66", fg="white", font=("Arial", 10, "bold"), command=aksi).grid(row=i//2, column=i%2, padx=10, pady=5)

window.mainloop()
