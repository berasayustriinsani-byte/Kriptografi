import tkinter as tk
from tkinter import messagebox

# === Fungsi Perhitungan ===
def hitung_hybrid():
    ekspresi1 = entry1.get()
    ekspresi2 = entry2.get()

    try:
        hasil1 = eval(ekspresi1)
    except Exception as e:
        hasil1 = f"Error: {e}"

    try:
        hasil2 = eval(ekspresi2)
    except Exception as e:
        hasil2 = f"Error: {e}"

    label_hasil1.config(text=f"Hasil Ekspresi 1: {hasil1}")
    label_hasil2.config(text=f"Hasil Ekspresi 2: {hasil2}")

# === GUI Tkinter ===
root = tk.Tk()
root.title("KALKULATOR HYBRID")
root.geometry("480x400")
root.config(bg="#2b2b2b")

# === Judul ===
judul = tk.Label(root, text="KALKULATOR HYBRID", font=("Segoe UI", 20, "bold"), fg="white", bg="#2b2b2b")
judul.pack(pady=20)

# === Frame Input ===
frame = tk.Frame(root, bg="#2b2b2b")
frame.pack(pady=10)

# Ekspresi 1 (tanpa spasi)
label1 = tk.Label(frame, text="Ekspresi Tanpa Spasi:", font=("Segoe UI", 12), fg="white", bg="#2b2b2b")
label1.grid(row=0, column=0, sticky="w", pady=5)
entry1 = tk.Entry(frame, font=("Consolas", 14), width=25, justify="center")
entry1.grid(row=0, column=1, padx=10)

# Ekspresi 2 (dengan spasi)
label2 = tk.Label(frame, text="Ekspresi Dengan Spasi:", font=("Segoe UI", 12), fg="white", bg="#2b2b2b")
label2.grid(row=1, column=0, sticky="w", pady=5)
entry2 = tk.Entry(frame, font=("Consolas", 14), width=25, justify="center")
entry2.grid(row=1, column=1, padx=10)

# Tombol Hitung
btn_hitung = tk.Button(root, text="HITUNG", font=("Segoe UI", 12, "bold"),
                       bg="#4CAF50", fg="white", activebackground="#66BB6A",
                       padx=20, pady=10, border=0, command=hitung_hybrid)
btn_hitung.pack(pady=20)

# === Label Hasil ===
label_hasil1 = tk.Label(root, text="Hasil Ekspresi 1: -", font=("Consolas", 13), fg="#FFD700", bg="#2b2b2b")
label_hasil1.pack()
label_hasil2 = tk.Label(root, text="Hasil Ekspresi 2: -", font=("Consolas", 13), fg="#00FFFF", bg="#2b2b2b")
label_hasil2.pack(pady=5)

# Footer
footer = tk.Label(root, text="© 2025 | Tugas Pratikum 2 - Kalkulator Hybrid",
                  font=("Segoe UI", 9), fg="#aaaaaa", bg="#2b2b2b")
footer.pack(side="bottom", pady=10)

root.mainloop()
