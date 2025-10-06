import math

def incremental_search_multistage():
    """
    Metode Incremental Search Multi-Stage untuk mencari akar f(x) = 0.
    Menampilkan tabel lengkap dengan x1, x2, f(x1), f(x2), c=(x1+x2)/2, f(c).
    Contoh: Untuk f(x) = (9.8*68.1/x)*(1 - math.exp(-x/68.1*10)) - 40,
    f(1) ≈ 51.144. Untuk f(x) = x**2 - x - 1, f(1) = -1.
    """
    print("=== METODE INCREMENTAL SEARCH MULTI-STAGE ===")
    print("Program untuk mencari akar persamaan f(x) = 0 dengan multiple stages")
    print("Tabel mencakup x1, x2, f(x1), f(x2), c=(x1+x2)/2, f(c) secara lengkap.")
    print()
    
    # Input fungsi dari pengguna
    print("Masukkan fungsi f(x) dalam format Python (gunakan 'x' sebagai variabel)")
    print("Contoh default: (9.8*68.1/x)*(1 - math.exp(-x/68.1*10)) - 40")
    print("Contoh lain: x**2 - x - 1")
    func_input = input("f(x) = ").strip()
    
    if func_input == "":
        func_str = "(9.8*68.1/x)*(1 - math.exp(-x/68.1*10)) - 40"
        print(f"Menggunakan fungsi default: {func_str}")
    else:
        func_str = func_input
        print(f"Menggunakan fungsi: {func_str}")
    
    # Definisikan fungsi f(x) dengan eval yang aman
    def f(x):
        try:
            return eval(func_str, {"__builtins__": {}, "math": math, "x": x})
        except Exception as e:
            print(f"Error dalam evaluasi fungsi untuk x={x}: {e}")
            print("Pastikan format benar (gunakan 'x', 'math.exp', dll.).")
            return None  # Kembalikan None jika error, tapi lanjutkan
    
    # Input parameter utama
    print("\nMasukkan parameter pencarian utama:")
    x_start_input = input("Nilai x awal [default: 10]: ").strip() or "10"
    x_end_input = input("Nilai x akhir [default: 20]: ").strip() or "20"
    try:
        x_start = float(x_start_input)
        x_end = float(x_end_input)
    except ValueError:
        print("Error: Input x_start/x_end harus numerik!")
        return []
    
    if x_start >= x_end:
        print("Error: x_start harus < x_end!")
        return []
    
    dx_input = input("Step size awal [default: 1]: ").strip() or "1"
    try:
        dx_initial = float(dx_input)
    except ValueError:
        print("Error: Step size harus numerik!")
        return []
    if dx_initial <= 0:
        print("Error: Step size harus > 0!")
        return []
    
    # Parameter multi-stage
    print("\nMasukkan parameter multi-stage:")
    num_stages_input = input("Jumlah stages [default: 3]: ").strip() or "3"
    try:
        num_stages = int(num_stages_input)
    except ValueError:
        num_stages = 3
        print("Menggunakan default: 3 stages")
    
    refinement_factor_input = input("Faktor penyempurnaan (0 < factor < 1) [default: 0.1]: ").strip() or "0.1"
    try:
        refinement_factor = float(refinement_factor_input)
    except ValueError:
        refinement_factor = 0.1
        print("Menggunakan default: 0.1")
    if not (0 < refinement_factor < 1):
        print("Error: Faktor penyempurnaan harus antara 0 dan 1! Menggunakan default 0.1")
        refinement_factor = 0.1
    
    all_results = []
    current_start = x_start
    current_end = x_end
    current_dx = dx_initial
    epsilon = 1e-10  # Toleransi untuk validasi f(c) ≈ 0
    
    for stage in range(num_stages):
        print(f"\n" + "="*140)
        print(f"PENCARIAN STAGE {stage + 1} (Interval: [{current_start:.6f}, {current_end:.6f}], dx={current_dx:.6f})")
        print("="*140)
        # Header tabel yang lebih rapi
        print(f"{'Stage':<6} {'Iter':<6} {'x1':<12} {'f(x1)/f(c)':<15} {'x2':<12} {'f(x2)':<15} {'c':<12} {'f(c)':<15} {'Keterangan':<20}")
        print("-" * 140)
        
        stage_results = []
        iteration = 0
        x1 = current_start
        min_dx = 1e-12  # Hindari loop infinite
        
        while x1 < current_end and current_dx > min_dx:
            x2 = min(x1 + current_dx, current_end)
            f1 = f(x1)
            f2 = f(x2)
            
            # Tangani None dengan tampilan khusus
            f1_display = f1 if f1 is not None else "Error"
            f2_display = f2 if f2 is not None else "Error"
            
            c = (x1 + x2) / 2
            f_c = f(c)
            f_c_display = f_c if f_c is not None else "Error"
            
            keterangan = "Tidak ada sign change"
            has_root = False
            if f1 is not None and f2 is not None and f1 * f2 < 0:
                keterangan = "AKAR DITEMUKAN (sign change)"
                has_root = True
                if f_c is not None and abs(f_c) < epsilon:
                    keterangan += " & f(c) ≈ 0"
                result = {
                    'stage': stage + 1,
                    'iterasi': iteration,
                    'x1': x1,
                    'x2': x2,
                    'f(x1)': f1,
                    'f(x2)': f2,
                    'c': c,
                    'f(c)': f_c,
                    'keterangan': keterangan
                }
                stage_results.append(result)
                all_results.append(result)
            elif f_c is not None and abs(f_c) < epsilon:
                keterangan = "f(c) ≈ 0 (potensial akar)"
                has_root = True
            
            # Selalu tampilkan baris tabel, bahkan tanpa akar
            print(f"{stage+1:<6} {iteration:<6} {x1:<12.6f} {f1_display:<15.6f} {x2:<12.6f} {f2_display:<15.6f} {c:<12.6f} {f_c_display:<15.6f} {keterangan:<20}")
            
            iteration += 1
            x1 = x2
        
        print("-" * 140)
        if not stage_results:
            print(f"\nTidak ditemukan interval akar pada Stage {stage + 1} dalam interval [{current_start:.6f}, {current_end:.6f}]")
            if stage == 0:  # Jika stage pertama gagal, hentikan
                break
        else:
            print(f"\nStage {stage + 1} selesai. Ditemukan {len(stage_results)} interval potensial.")
        
        # Pilih interval untuk refinement (jika multiple)
        if len(stage_results) > 1:
            print("Interval yang ditemukan:")
            for i, res in enumerate(stage_results):
                print(f"  {i+1}. [{res['x1']:.6f}, {res['x2']:.6f}], f(x1)={res['f(x1)']:.6f}, f(x2)={res['f(x2)']:.6f}, c={res['c']:.6f}, f(c)={res['f(c)']:.6f}")
            choice = input("Pilih interval untuk stage berikutnya (default: 1): ").strip() or "1"
            try:
                idx = int(choice) - 1
                selected_bracket = stage_results[idx]
            except (ValueError, IndexError):
                selected_bracket = stage_results[0]
                print("Pilihan invalid, gunakan interval pertama.")
        elif stage_results:
            selected_bracket = stage_results[0]
        else:
            break  # Tidak ada interval, hentikan stage selanjutnya
        
        # Persempit untuk stage berikutnya
        current_start = selected_bracket['x1']
        current_end = selected_bracket['x2']
        current_dx = (current_end - current_start) * refinement_factor
        
        if stage < num_stages - 1:
            print(f"Interval terpilih untuk Stage {stage + 2}: [{current_start:.6f}, {current_end:.6f}]")
            print(f"dx baru = {current_dx:.6f}")
        else:
            print(f"Interval final: [{current_start:.6f}, {current_end:.6f}]")
    
    # Ringkasan hasil dengan fokus pada f(x)
    print("\n" + "="*140)
    if all_results:
        print("RINGKASAN HASIL:")
        print(f"Ditemukan {len(all_results)} interval yang mengandung akar melalui {len(set(r['stage'] for r in all_results))} stage")
        
        for stage_num in range(1, num_stages + 1):
            stage_results = [r for r in all_results if r['stage'] == stage_num]
            if stage_results:
                print(f"\nStage {stage_num}:")
                for i, result in enumerate(stage_results, 1):
                    print(f"  {i}. Akar antara [{result['x1']:.6f}, {result['x2']:.6f}]")
                    print(f"     f({result['x1']:.6f}) = {result['f(x1)']:.6f}, f({result['x2']:.6f}) = {result['f(x2)']:.6f}")
                    print(f"     c = {result['c']:.6f}, f(c) = {result['f(c)']:.6f}")
                    print(f"     Keterangan: {result['keterangan']}")
        
        # Estimasi akhir dari stage final
        final_stage = max(set(r['stage'] for r in all_results))
        final_results = [r for r in all_results if r['stage'] == final_stage]
        if final_results:
            final_result = final_results[0]  # Ambil yang dipilih/pertama
            estimated_root = final_result['c']
            f_estimated = final_result['f(c)']
            status = "AKAR VALID" if f_estimated is not None and abs(f_estimated) < epsilon else "ESTIMASI (perlu refinement lebih lanjut)"
            print(f"\nESTIMASI AKAR FINAL (dari c terakhir): x ≈ {estimated_root:.10f}")
            print(f"f({estimated_root:.10f}) = {f_estimated:.10f}" if f_estimated is not None else "f(c) = Error evaluasi")
            print(f"Status: {status}")
    else:
        print("TIDAK DITEMUKAN AKAR DALAM INTERVAL YANG DIBERIKAN")
        print("Coba perbesar interval atau periksa fungsi f(x).")
    
    return all_results
