import math
import numpy as np

def newton_raphson_complete():
    output_log = []  # tempat simpan semua output
    
    def log(text=""):
        """Helper untuk simpan dan print baris"""
        output_log.append(text)
        print(text)
    
    log("=== METODE NEWTON-RAPHSON (COMPLETE ERROR ANALYSIS) ===\n")
    
    try:
        # Input fungsi dari user
        log("Masukkan fungsi f(x) dalam format Python:")
        log("Contoh: x**3 - 2*x - 5")
        log("        np.exp(-x) - x")
        log("        math.sin(x) - x/2")
        func_str = input("f(x) = ")
        
        # Input turunan fungsi
        log("\nMasukkan turunan fungsi f'(x) dalam format Python:")
        log("Contoh: 3*x**2 - 2")
        log("        -np.exp(-x) - 1")
        log("        math.cos(x) - 0.5")
        deriv_str = input("f'(x) = ")
        
        # Tebakan awal & parameter
        x0 = float(input("\nMasukkan tebakan awal (x0): "))
        tolerance = float(input("Masukkan toleransi error (contoh: 0.0001): "))
        max_iter = int(input("Masukkan maksimum iterasi (contoh: 20): "))
        
        # Tanya user apakah ingin detail
        show_details = input("\nTampilkan detail perhitungan setiap iterasi? (y/n): ").strip().lower() == 'y'
        
        # Definisikan fungsi
        def f(x): return eval(func_str)
        def f_prime(x): return eval(deriv_str)
        
        # Cari true root approx
        log("\n🔍 Mencari nilai akar sebenarnya...")
        x_temp = x0
        for _ in range(100):
            if abs(f_prime(x_temp)) < 1e-15:
                break
            x_next_temp = x_temp - f(x_temp) / f_prime(x_temp)
            if abs(x_next_temp - x_temp) < 1e-15:
                break
            x_temp = x_next_temp
        true_root = x_temp
        
        log(f"✅ Nilai akar sebenarnya (estimasi) = {true_root:.8f}\n")
        
        # Tabel header
        log("="*110)
        log("HASIL ITERASI NEWTON-RAPHSON - ANALISIS ERROR")
        log("="*110)
        log(f"{'i':<3} {'x_i':<15} {'x_i+1':<15} {'f(x_i)':<15} {'f\'(x_i)':<15} {'e_a (%)':<12} {'e_t (%)':<12}")
        log("-"*110)
        
        # Iterasi
        x_current = x0
        konvergen = False
        final_x = x0
        final_e_t = 0.0
        e_a = None
        all_iterations = []
        
        for i in range(max_iter + 1):
            f_current = f(x_current)
            fp_current = f_prime(x_current)
            
            if i == 0:
                e_t = abs((true_root - x_current) / true_root) * 100
                log(f"{i:<3} {x_current:<15.8f} {'-':<15} {f_current:<15.8f} {fp_current:<15.8f} {'-':<12} {e_t:<12.6f}")
                all_iterations.append({'i': i, 'x_i': x_current, 'x_i+1': None,
                                       'f(x_i)': f_current, 'f_prime(x_i)': fp_current,
                                       'e_a': None, 'e_t': e_t})
            else:
                if abs(fp_current) < 1e-15:
                    log(f"\n⚠️  f'({x_current:.6f}) ≈ 0, metode gagal.")
                    break
                
                x_next = x_current - f_current / fp_current
                e_a = abs((x_next - x_current) / x_next) * 100 if x_next != 0 else float("inf")
                e_t = abs((true_root - x_current) / true_root) * 100
                e_t_next = abs((true_root - x_next) / true_root) * 100
                
                log(f"{i:<3} {x_current:<15.8f} {x_next:<15.8f} {f_current:<15.8f} {fp_current:<15.8f} {e_a:<12.6f} {e_t:<12.6f}")
                
                all_iterations.append({'i': i, 'x_i': x_current, 'x_i+1': x_next,
                                       'f(x_i)': f_current, 'f_prime(x_i)': fp_current,
                                       'e_a': e_a, 'e_t': e_t, 'e_t_next': e_t_next})
                
                if e_a < tolerance and abs(f(x_next)) < 1e-10:
                    konvergen = True
                    final_x = x_next
                    final_e_t = e_t_next
                    break
                x_current = x_next
        
        log("="*110)
        
        # Detail tambahan
        if show_details and len(all_iterations) > 1:
            log("\n" + "="*80)
            log("DETAIL PERHITUNGAN SETIAP ITERASI")
            log("="*80)
            for iter_data in all_iterations[1:]:
                i = iter_data['i']
                x_i = iter_data['x_i']
                x_i1 = iter_data['x_i+1']
                f_xi = iter_data['f(x_i)']
                fp_xi = iter_data['f_prime(x_i)']
                e_t_next = iter_data.get('e_t_next', 0)
                
                log(f"\n📐 ITERASI {i}:")
                log(f"   Rumus: x_{i+1} = x_{i} - f(x_{i})/f'(x_{i})")
                log(f"   x_{i} = {x_i:.8f}")
                log(f"   f(x_{i}) = {f_xi:.8f}")
                log(f"   f'(x_{i}) = {fp_xi:.8f}")
                log(f"   x_{i+1} = {x_i:.8f} - ({f_xi:.8f})/({fp_xi:.8f})")
                log(f"   x_{i+1} = {x_i:.8f} - {f_xi/fp_xi:.8f}")
                log(f"   x_{i+1} = {x_i1:.8f}")
                log(f"   e_t,i+1 = |({true_root:.8f} - {x_i1:.8f}) / {true_root:.8f}| × 100% = {e_t_next:.8f}%")
            log("="*80)
        
        # Hasil akhir
        if konvergen:
            log(f"\n✅ KONVERGEN pada iterasi ke-{i}")
            log(f"Akar yang ditemukan: x = {final_x:.8f}")
            log(f"Akar sebenarnya (estimasi): {true_root:.8f}")
            log(f"f({final_x:.8f}) = {f(final_x):.2e}")
            log(f"Error aproksimasi (e_a): {e_a:.8f} %")
            log(f"Error sebenarnya (e_t): {final_e_t:.8f} %")
        else:
            log(f"\n❌ Tidak konvergen setelah {max_iter} iterasi.")
            log(f"Nilai terakhir: x = {x_current:.8f}, f(x) = {f(x_current):.2e}")
    
    except Exception as e:
        log(f"\n❌ Error: {str(e)}")
    
    # Simpan ke file
    with open("newton_raphson_output.txt", "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(output_log))
    log("\n📂 Semua output juga disimpan di file 'newton_raphson_output.txt'")

