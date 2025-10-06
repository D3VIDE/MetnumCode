import math

def incremental_search_multistage():
    print("=== METODE INCREMENTAL SEARCH - LANGKAH DEMI LANGKAH ===")
    
    # Input dari user
    print("\nMasukkan fungsi f(x) dalam format Python:")
    print("Contoh: (9.8*68.1/x)*(1 - math.exp(-x/68.1*10)) - 40")
    func_str = input("f(x) = ").strip() or "(9.8*68.1/x)*(1 - math.exp(-x/68.1*10)) - 40"
    
    def f(x):
        return eval(func_str)
    
    print("\nMasukkan parameter pencarian:")
    x_start = float(input("Nilai x awal [default: 1]: ") or "1")
    x_end = float(input("Nilai x akhir [default: 15]: ") or "15")
    dx = float(input("Step size (dx) [default: 1]: ") or "1")
    
    print(f"\n{'='*80}")
    print(f"PENCARIAN AKAR: f(x) = 0")
    print(f"Range: x = {x_start} sampai {x_end}, Step: {dx}")
    print(f"{'='*80}")
    
    iteration = 0
    x_current = x_start
    roots_found = []
    
    while x_current <= x_end:
        x_next = x_current + dx
        if x_next > x_end:
            break
        
        print(f"\n--- Iterasi {iteration} ---")
        print(f"x₁ = {x_current:.6f}")
        print(f"x₂ = {x_next:.6f}")
        
        # Hitung nilai fungsi
        f1 = f(x_current)
        f2 = f(x_next)
        
        print(f"f(x₁) = f({x_current:.6f}) = {f1:.6f}")
        print(f"f(x₂) = f({x_next:.6f}) = {f2:.6f}")
        
        # Cek tanda
        print(f"Tanda: f(x₁) = {'+' if f1 >= 0 else '-'}, f(x₂) = {'+' if f2 >= 0 else '-'}")
        
        # Analisis
        if f1 == 0:
            print(f"→ DITEMUKAN AKAR TEPAT di x = {x_current:.6f} (f(x) = 0)")
            roots_found.append({'x': x_current, 'type': 'exact'})
        elif f2 == 0:
            print(f"→ DITEMUKAN AKAR TEPAT di x = {x_next:.6f} (f(x) = 0)")
            roots_found.append({'x': x_next, 'type': 'exact'})
        elif f1 * f2 < 0:
            print(f"→ AKAR DITEMUKAN antara {x_current:.6f} dan {x_next:.6f}")
            print(f"  Alasan: f(x₁) × f(x₂) = {f1:.6f} × {f2:.6f} = {f1*f2:.6f} < 0")
            print(f"  (Tanda berbeda → ada akar di interval ini)")
            roots_found.append({
                'x1': x_current, 
                'x2': x_next, 
                'f1': f1, 
                'f2': f2,
                'type': 'bracket'
            })
        else:
            print(f"→ Tidak ada akar antara {x_current:.6f} dan {x_next:.6f}")
            print(f"  Alasan: f(x₁) × f(x₂) = {f1:.6f} × {f2:.6f} = {f1*f2:.6f} ≥ 0")
            print(f"  (Tanda sama → tidak ada akar di interval ini)")
        
        iteration += 1
        x_current = x_next
    
    print(f"\n{'='*80}")
    print("HASIL PENCARIAN")
    print(f"{'='*80}")
    
    if roots_found:
        print(f"Ditemukan {len(roots_found)} hasil:")
        for i, root in enumerate(roots_found, 1):
            if root['type'] == 'exact':
                print(f"{i}. Akar tepat di x = {root['x']:.6f}")
            else:
                print(f"{i}. Akar berada antara:")
                print(f"   x = {root['x1']:.6f} (f(x) = {root['f1']:.6f})")
                print(f"   x = {root['x2']:.6f} (f(x) = {root['f2']:.6f})")
                # Estimasi akar
                x_est = (root['x1'] + root['x2']) / 2
                print(f"   Estimasi akar ≈ {x_est:.6f}")
    else:
        print("Tidak ditemukan akar dalam range yang diberikan")
    
    return roots_found
    

