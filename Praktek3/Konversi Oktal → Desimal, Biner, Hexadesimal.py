def konversi_oktal():
    try:
        oktal = input("Masukkan bilangan oktal: ").strip()
        desimal = int(oktal, 8)
        biner = bin(desimal)[2:]
        heksa = hex(desimal)[2:].upper()

        print("\nHasil Konversi:")
        print(f"Desimal     : {desimal}")
        print(f"Biner       : {biner}")
        print(f"Hexadesimal : {heksa}")
    except Exception:
        print("❌ Error: Input bukan bilangan oktal yang valid!")

# Jalankan program
konversi_oktal()
