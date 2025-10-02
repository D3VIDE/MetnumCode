import math
def taylor_series(fungsi, base_point, x_value, n_terms):

    results = []
    
    for n in range(n_terms + 1):
        if fungsi == 'cos':
            # Turunan cos(x): cos(x), -sin(x), -cos(x), sin(x), cos(x), ...
            turunan_cycle = [math.cos, lambda x: -math.sin(x), 
                           lambda x: -math.cos(x), math.sin]
            f_deriv = turunan_cycle[n % 4](base_point)
        elif fungsi == 'sin':
            # Turunan sin(x): sin(x), cos(x), -sin(x), -cos(x), sin(x), ...
            turunan_cycle = [math.sin, math.cos, 
                           lambda x: -math.sin(x), lambda x: -math.cos(x)]
            f_deriv = turunan_cycle[n % 4](base_point)
        elif fungsi == 'exp':
            # Turunan e^x selalu e^x
            f_deriv = math.exp(base_point)
        elif fungsi == 'tan':
            # Turunan tan(x) lebih kompleks
            if n == 0:
                f_deriv = math.tan(base_point)
            elif n == 1:
                f_deriv = 1 / (math.cos(base_point) ** 2)
            elif n == 2:
                f_deriv = (2 * math.sin(base_point)) / (math.cos(base_point) ** 3)
            elif n == 3:
                f_deriv = (2 * (2 * math.sin(base_point)**2 + 1)) / (math.cos(base_point) ** 4)
            else:
                # Untuk n > 3, menggunakan aproksimasi numerik
                # Ini penyederhanaan, untuk implementasi lengkap perlu rumus turunan tan yang tepat
                f_deriv = 0  # Bisa dikembangkan lebih lanjut
        else:
            raise ValueError("Fungsi tidak didukung")
        
        term = (f_deriv / factorial(n)) * ((x_value - base_point) ** n)
        
        if n == 0:
            results.append(term)
        else:
            results.append(results[-1] + term)
    
    return results

def metode_2():
    print("\n=== DERET TAYLOR ===")
    print("Pilih fungsi:")
    print("1. cos(x)")
    print("2. sin(x)")
    print("3. exp(x)")
    print("4. tan(x)")
    
    try:
        pilihan_fungsi = input("Pilih fungsi (1-4): ")
        
        if pilihan_fungsi == "1":
            fungsi = "cos"
            fungsi_str = "cos(x)"
        elif pilihan_fungsi == "2":
            fungsi = "sin"
            fungsi_str = "sin(x)"
        elif pilihan_fungsi == "3":
            fungsi = "exp"
            fungsi_str = "exp(x)"
        elif pilihan_fungsi == "4":
            fungsi = "tan"
            fungsi_str = "tan(x)"
        else:
            print("Pilihan tidak valid!")
            return
        
        # Input dari user
        base_point = float(input(f"Masukkan base-point (a) untuk {fungsi_str}: "))
        x_value = float(input(f"Masukkan nilai x yang ingin dihitung: "))
        n_terms = int(input("Masukkan jumlah suku maksimal (n): "))
        
        # Validasi untuk tan(x) - hindari titik singularitas
        if fungsi == "tan":
            # Hindari π/2 + kπ
            if abs(math.cos(x_value)) < 1e-10:
                print("Error: tan(x) tidak terdefinisi pada x = π/2 + kπ")
                return
            if abs(math.cos(base_point)) < 1e-10:
                print("Error: base-point tidak boleh pada titik singularitas tan(x)")
                return
        
        # Hitung deret Taylor
        results = taylor_series(fungsi, base_point, x_value, n_terms)
        
        # Hitung nilai eksak
        if fungsi == "cos":
            exact_value = math.cos(x_value)
        elif fungsi == "sin":
            exact_value = math.sin(x_value)
        elif fungsi == "exp":
            exact_value = math.exp(x_value)
        elif fungsi == "tan":
            exact_value = math.tan(x_value)
        
        # Tampilkan hasil
        print(f"\nHasil perhitungan {fungsi_str}")
        print(f"Base-point (a) = {base_point}")
        print(f"x = {x_value}")
        print(f"Nilai eksak = {exact_value:.10f}")
        print("\n" + "="*70)
        print(f"{'n':<5} {'Nilai Taylor':<20} {'Error':<20} {'Error Relatif (%)':<15}")
        print("-"*70)
        
        for n, result in enumerate(results):
            error = abs(exact_value - result)
            # Handle division by zero untuk error relatif
            if abs(exact_value) < 1e-10:
                error_relatif = float('inf')
            else:
                error_relatif = (error / abs(exact_value)) * 100
            
            print(f"{n:<5} {result:<20.10f} {error:<20.10f} {error_relatif:<15.10f}")
        
        print("="*70)
        
        # Contoh khusus untuk tugas 1 no 2
        if fungsi == "cos" and abs(base_point - math.pi/4) < 1e-10 and abs(x_value - math.pi/6) < 1e-10:
            print("\n=== CONTOH TUGAS 1 NO 2 ===")
            print("f(x) = cos(x), a = π/4, x = π/6")
            for n, result in enumerate(results):
                print(f"n={n}: {result:.10f}")
                
    except ValueError:
        print("Error: Input harus berupa angka!")
    except Exception as e:
        print(f"Error: {e}")