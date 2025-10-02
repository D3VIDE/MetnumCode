from binerIteration import biner_solver
from taylorTheorem import taylor_solver
def show_menu():
    print("\n" + "="*40)
    print("           PROGRAM NUMERIK")
    print("="*40)
    print("1. Metode Binary Iteration")
    print("2. Metode Deret Taylor")
    print("3. Fungsi 3")
    print("4. Metode Gauss-Seidel")
    print("5. Fungsi 5")
    print("6. Keluar")
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
   
   taylor_solver()
   

def metode_3():
   print("\n=== FUNGSI 3 ===")
   # Implementasi di sini
   pass

def metode_4():
   print("\n=== METODE GAUSS-SEIDEL ===")
   # Implementasi di sini
   pass

def metode_5():
   print("\n=== FUNGSI 5 ===")
   # Implementasi di sini
   pass

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