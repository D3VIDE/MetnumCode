from binerIteration import biner_solver
from taylorTheorem import taylor_series
from bisection import fungsi_parachutist, cari_interval, metode_bisection, tampilkan_hasil_akhir, tampilkan_sejarah_iterasi, tampilkan_perkembangan_interval, metode_bisection_custom
from gaus import print_matrix, gauss_elimination, backward_substitution
from incrementalSearch import incremental_search_multistage
import numpy as np
def show_menu():
    print("\n" + "="*40)
    print("           PROGRAM NUMERIK")
    print("="*40)
    print("1. Metode Binary Iteration")
    print("2. Metode Deret Taylor")
    print("3. Metode Drag - Bisection")
    print("4. Metode Bisection - PENENTUAN TITIK")
    print("5. Manual Input - Increment ")
    print("6. Metode Drag - Increment")
    print("7. Manual input - Bisection")
    print("-. Gaus Elimination")
    print("100. Keluar (q)")
    print("-"*40)
    return input("Pilih opsi (1-6): ")

def metode_1():
   print("\n=== METODE BINARY ITERATION ===")
   try:
      angka = float(input("Masukan angka desimal: "))
      # Presisi langsung 10, tidak perlu input dari user
      hasil = biner_solver(angka, 10)
      print(f"Hasil konversi: {angka} = {hasil}₂")
      
      # Tampilkan verifikasi (hanya untuk bilangan bulat)
      if "." not in hasil:
          verif = int(hasil, 2)
          print(f"Verifikasi: {hasil}₂ = {verif}₁₀")
          
   except ValueError:
      print("Error: Input harus berupa angka!")
   except Exception as e:
      print(f"Error: {e}")

def metode_2():
   print("\n=== METODE DERET TAYLOR ===")
   taylor_series()
   

def metode_3():
    print("METODE BISECTION - DRAG COEFFICIENT PARACHUTIST")
    print("=" * 70)
    
    try:
        print("\n📝 MASUKKAN PARAMETER:")
        m = float(input("Massa parachutist (kg) [default: 68.1]: ") or "68.1")
        g = float(input("Percepatan gravitasi (m/s²) [default: 9.8]: ") or "9.8")
        t = float(input("Waktu free-fall (s) [default: 10]: ") or "10")
        v = float(input("Kecepatan yang diinginkan (m/s) [default: 40]: ") or "40")
        
        print("\n📊 PARAMETER YANG DIGUNAKAN:")
        param_table = [
            ["Parameter", "Nilai", "Satuan"],
            ["-"*15, "-"*10, "-"*10],
            ["Massa (m)", f"{m}", "kg"],
            ["Gravitasi (g)", f"{g}", "m/s²"],
            ["Waktu (t)", f"{t}", "s"],
            ["Kecepatan (v)", f"{v}", "m/s"]
        ]
        
        for row in param_table:
            print(f"{row[0]:15} {row[1]:10} {row[2]:10}")
        
    except ValueError:
        print("❌ ERROR: Input harus berupa angka!")
        return
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return
    
    # Cari interval tanpa plot
    intervals = cari_interval(m, g, t, v)
    
    if not intervals:
        print("❌ Tidak ditemukan interval yang memuat akar!")
        return
    
    # Pilih interval
    if len(intervals) == 1:
        a, b, fa, fb = intervals[0]
        print(f"\n✅ Interval dipilih: [{a:.2f}, {b:.2f}]")
    else:
        print("\n📝 PILIH INTERVAL:")
        for i, (c1, c2, fc1, fc2) in enumerate(intervals):
            print(f"{i+1}. [{c1:.2f}, {c2:.2f}] - f({c1:.2f}) = {fc1:.4f}, f({c2:.2f}) = {fc2:.4f}")
        choice = int(input("Pilih interval (1, 2, ...): ")) - 1
        a, b, fa, fb = intervals[choice]
    
    # Input parameter metode
    print("\n⚙️  PARAMETER METODE:")
    toleransi = float(input("Toleransi error [default: 0.000001]: ") or "0.000001")
    max_iter = int(input("Maksimum iterasi [default: 100]: ") or "100")
    
    # Parameter untuk fungsi
    params = (m, g, t, v)
    
    # Jalankan metode bisection dengan ε_a dan ε_t
    result = metode_bisection(fungsi_parachutist, a, b, params, toleransi, max_iter)
    
    if result[0] is not None:
        akar, iterasi, history, true_root = result
        # Tampilkan semua hasil dalam bentuk tabel
        tampilkan_hasil_akhir(akar, iterasi, history, params, true_root)
        tampilkan_sejarah_iterasi(history, akar)
        tampilkan_perkembangan_interval(history)

def metode_4():
    print("\n=== METODE BISECTION - PENENTUAN TITIK BERIKUTNYA ===")
    print("=" * 60)

    try:
        print("\n📝 MASUKKAN TITIK AWAL:")
        a = float(input("Titik a (contoh: 0): ") or "0")
        b = float(input("Titik b (contoh: -1.5): ") or "-1.5")
        
        print("\n⚙️  PARAMETER METODE:")
        jumlah_iterasi = int(input("Jumlah iterasi [default: 5]: ") or "5")
        
    except ValueError:
        print("❌ ERROR: Input harus berupa angka!")
        return
    
    def fungsiTitik(x):
        return x**3 - x + 1
    
    print("\n" + "="*80)
    print("PROSES METODE BISECTION - PENENTUAN TITIK BERIKUTNYA")
    print("="*80)
    print("Iter\t   a\t\t   b\t\t   c\t\t  f(a)\t\t  f(b)\t\t  f(c)")
    print("-"*80)

    # Simpan sejarah titik-titik
    titik_sejarah = []

    a_current = a
    b_current = b
    fa = fungsiTitik(a_current)
    fb = fungsiTitik(b_current)

    # Tampilkan titik awal
    print(f"{0:3d}\t{a_current:8.4f}\t{b_current:8.4f}\t{'':8}\t{fa:10.6f}\t{fb:10.6f}\t{'':10}")
    titik_sejarah.append({'iterasi': 0, 'a': a_current, 'b': b_current, 'c': None, 'fa': fa, 'fb': fb, 'fc': None})

    # Proses iterasi bisection
    for i in range(1, jumlah_iterasi + 1):
        # Hitung titik tengah
        c = (a_current + b_current) / 2
        fc = fungsiTitik(c)

        # Tampilkan hasil iterasi
        print(f"{i:3d}\t{a_current:8.4f}\t{b_current:8.4f}\t{c:8.4f}\t{fa:10.6f}\t{fb:10.6f}\t{fc:10.6f}")

        # Simpan sejarah
        titik_sejarah.append({
            'iterasi': i, 
            'a': a_current, 
            'b': b_current, 
            'c': c, 
            'fa': fa, 
            'fb': fb, 
            'fc': fc
        })

        # Tentukan interval baru berdasarkan tanda fungsi
        if fa * fc < 0:
            # Akar berada di interval kiri [a, c]
            b_current = c
            fb = fc
        else:
            # Akar berada di interval kanan [c, b]
            a_current = c
            fa = fc

    # Tampilkan ringkasan perkembangan titik
    print("\n" + "="*70)
    print("RINGKASAN PERKEMBANGAN TITIK")
    print("="*70)
    print("Iterasi\tTitik a\t\tTitik b\t\tTitik c (tengah)")
    print("-"*70)

    for titik in titik_sejarah:
        if titik['iterasi'] == 0:
            print(f"{titik['iterasi']:3d}\t{titik['a']:8.4f}\t{titik['b']:8.4f}\t{'Awal':15}")
        else:
            print(f"{titik['iterasi']:3d}\t{titik['a']:8.4f}\t{titik['b']:8.4f}\t{titik['c']:8.4f}")

    # Tampilkan pola titik-titik
    print("\n" + "="*50)
    print("POLA TITIK-TITIK YANG DIHASILKAN")
    print("="*50)

    # Hitung selisih antara titik-titik berurutan
    print("Urutan titik tengah (c) yang dihasilkan:")
    titik_tengah = [titik['c'] for titik in titik_sejarah if titik['c'] is not None]

    for j, titik_c in enumerate(titik_tengah, 1):
        print(f"Iterasi {j}: c = {titik_c:.4f}")

    # Analisis pola
    print("\n📊 ANALISIS POLA:")
    if len(titik_tengah) >= 2:
        print("Selisih antara titik-titik berurutan:")
        for k in range(1, len(titik_tengah)):
            selisih = abs(titik_tengah[k] - titik_tengah[k-1])
            print(f"c[{k}] - c[{k-1}] = {selisih:.4f}")

    # Tampilkan perkembangan interval
    print("\n" + "="*60)
    print("PERKEMBANGAN LEBAR INTERVAL")
    print("="*60)
    print("Iterasi\t  Lebar Interval\t  Rasio")
    print("-"*60)

    for titik in titik_sejarah:
        lebar = abs(titik['b'] - titik['a'])
        if titik['iterasi'] == 0:
            print(f"{titik['iterasi']:3d}\t{lebar:12.6f}\t{'Awal':10}")
        else:
            lebar_sebelumnya = abs(titik_sejarah[titik['iterasi']-1]['b'] - titik_sejarah[titik['iterasi']-1]['a'])
            rasio = lebar / lebar_sebelumnya
            print(f"{titik['iterasi']:3d}\t{lebar:12.6f}\t{rasio:10.4f}")

def metode_5():
    print("\n" + "="*50)
    print("PROGRAM INCREMENTAL SEARCH")
    print("="*50)

    incremental_search_multistage()


def metode_6():
    print("\n" + "="*50)
    print("PROGRAM INCREMENTAL SEARCH")
    print("="*50)

def metode_100():
    print("="*70)
    print("📘 PENYELESAIAN SPL DENGAN METODE GAUSS ELIMINATION")
    print("="*70)

    n = int(input("\nMasukkan ukuran matriks (misal 3 untuk 3x3): "))

    A = np.zeros((n, n))
    print("\nMasukkan elemen matriks A:")
    for i in range(n):
        for j in range(n):
            A[i][j] = float(input(f"  A[{i+1},{j+1}] = "))

    b = np.zeros(n)
    print("\nMasukkan elemen vektor b:")
    for i in range(n):
        b[i] = float(input(f"  b[{i+1}] = "))

    print("\nMatriks A:")
    print_matrix(A)
    print("Vektor b:")
    print(b)

    aug = gauss_elimination(A, b)
    x = backward_substitution(aug)

    print("\n==================== HASIL AKHIR ====================")
    for i in range(n):
        print(f"x{i+1} = {x[i]:8.2f}")

    print("\nVerifikasi: A × x = b →", np.allclose(np.dot(A, x), b))
    print("A × x =", np.round(np.dot(A, x), 2))

def metode_7():
    metode_bisection_custom()

def main():
  while True:
     try:
        pilihan = show_menu()

        if pilihan == "1":
           metode_1()
        elif pilihan == "2":
           metode_2()
        elif pilihan == "3":
           metode_3()
        elif pilihan == "4":
           metode_4()
        elif pilihan == "5":
           metode_5()
        elif pilihan == "6":
            metode_6()
        elif pilihan == "7":
            metode_7()
        elif pilihan == "q":
           print("\nTerima kasih! Program selesai.")
           break
        else:
           print("\nPilihan tidak valid! Silakan pilih 1-6.")
      
     except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh user.")
        break
     except Exception as e:
          print(f"\nTerjadi error: {e}")
          input("Tekan Enter untuk melanjutkan...")

if __name__ == "__main__":
   main()