def konversi_heksa():
    try:
        heksa = input("Masukkan bilangan hexadesimal: ").strip()
        desimal = int(heksa, 16)
        biner = bin(desimal)[2:]
        oktal = oct(desimal)[2:]

        print("\nHasil Konversi:")
        print(f"Desimal : {desimal}")
        print(f"Biner   : {biner}")
        print(f"Oktal   : {oktal}")
    except Exception:
        print("❌ Error: Input bukan bilangan hexadesimal yang valid!")

# Jalankan program
konversi_heksa()
