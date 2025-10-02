def biner_solver(angka, precission=10):
    """
    Mengkonversi bilangan desimal ke biner
    sambil menampilkan langkah pengerjaan.
    """
    # Handle input negatif
    if angka < 0:
        print(f"Angka negatif, ubah jadi positif dulu: {angka} → {-angka}")
        return "-" + biner_solver(-angka, precission)
    
    print(f"\n=== Konversi {angka} ke Biner ===")

    integer_part = int(angka)
    fractional_part = angka - integer_part
    print(f"Pisahkan: integer = {integer_part}, pecahan = {fractional_part}\n")

    # Konversi bagian bulat
    if integer_part == 0:
        binary_int = "0"
        print("-- Bagian Bulat --")
        print("Integer = 0 → langsung 0")
    else:
        binary_int = ""
        temp_int = integer_part
        print("-- Bagian Bulat --")
        langkah = 1
        while temp_int > 0:
            sisa = temp_int % 2
            print(f"Langkah {langkah}: {temp_int} ÷ 2 = {temp_int // 2}, sisa = {sisa}")
            binary_int = str(sisa) + binary_int
            temp_int //= 2
            langkah += 1
    print(f"Hasil bagian bulat: {binary_int}\n")

    # Konversi bagian pecahan
    binary_frac = ""
    if fractional_part > 0:
        binary_frac = "."
        temp_frac = fractional_part
        print("-- Bagian Pecahan --")
        for i in range(precission):
            temp_frac *= 2
            bit = int(temp_frac)
            print(f"Langkah {i+1}: {temp_frac:.10f} → bit = {bit}")
            binary_frac += str(bit)
            temp_frac -= bit
            if temp_frac == 0:
                break
        print(f"Hasil bagian pecahan: {binary_frac}")
    else:
        print("-- Tidak ada bagian pecahan --")

    hasil = binary_int + binary_frac
    print(f"\n=== Hasil akhir: {hasil} ===\n")
    return hasil
