def konversi_biner():
    try:
        biner = input("Masukkan bilangan biner: ")
        desimal = int(biner, 2)
        heksa = hex(desimal)[2:].upper()
        print(f"\nHasil Konversi:")
        print(f"Desimal     : {desimal}")
        print(f"Hexadesimal : {heksa}")
    except Exception:
        print("❌ Error: Input bukan bilangan biner yang valid!")

# Jalankan program
konversi_biner()
