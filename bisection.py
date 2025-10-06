import math

def fungsi_parachutist(c, m, g, t, v):
    """
    Fungsi untuk menghitung drag coefficient parachutist
    f(c) = (g * m / c) * (1 - exp(-c * t / m)) - v
    """
    return (g * m / c) * (1 - math.exp(-c * t / m)) - v

def cari_interval(m, g, t, v, c_min=1, c_max=20, step=1):
    """
    Mencari interval dimana fungsi berubah tanda (tanpa plot)
    """
    print("\n" + "="*70)
    print("PENCARIAN INTERVAL AWAL")
    print("="*70)
    print("c\t\tf(c)\t\tTanda")
    print("-"*70)
    
    intervals = []
    prev_c = None
    prev_fc = None
    
    c_values = []
    for c in range(int(c_min), int(c_max) + 1, step):
        if c == 0:
            continue
            
        fc = fungsi_parachutist(c, m, g, t, v)
        tanda = "+" if fc > 0 else "-" if fc < 0 else "0"
        
        print(f"{c}\t\t{fc:10.6f}\t\t{tanda}")
        c_values.append((c, fc, tanda))
        
        # Cek perubahan tanda
        if prev_fc is not None:
            if prev_fc * fc <= 0:
                intervals.append((prev_c, c, prev_fc, fc))
        
        prev_c = c
        prev_fc = fc
    
    # Tambahkan titik-titik antara untuk akurasi lebih baik
    print("\n" + "="*70)
    print("PENCARIAN INTERVAL DETAIL (antara titik-titik perubahan tanda)")
    print("="*70)
    print("c\t\tf(c)\t\tTanda")
    print("-"*70)
    
    detailed_intervals = []
    for interval in intervals:
        c1, c2, fc1, fc2 = interval
        # Cek titik tengah
        c_mid = (c1 + c2) / 2
        fc_mid = fungsi_parachutist(c_mid, m, g, t, v)
        tanda_mid = "+" if fc_mid > 0 else "-" if fc_mid < 0 else "0"
        
        print(f"{c_mid:.2f}\t\t{fc_mid:10.6f}\t\t{tanda_mid}")
        
        # Tentukan interval yang lebih tepat
        if fc1 * fc_mid <= 0:
            detailed_intervals.append((c1, c_mid, fc1, fc_mid))
        else:
            detailed_intervals.append((c_mid, c2, fc_mid, fc2))
    
    return detailed_intervals if detailed_intervals else intervals

def metode_bisection(f, a, b, params, toleransi=1e-6, max_iter=100):
    """
    Metode Bisection untuk mencari akar persamaan dengan ε_a dan ε_t
    + menampilkan rumus dan hasil secara lengkap setiap iterasi
    """
    fa = f(a, *params)
    fb = f(b, *params)
    m, g, t, v = params

    print(f"\n" + "="*70)
    print("INFORMASI INTERVAL AWAL")
    print("="*70)
    print(f"a = {a:.6f}, f(a) = {fa:.6f}")
    print(f"b = {b:.6f}, f(b) = {fb:.6f}")
    print(f"f(a) × f(b) = {fa * fb:.6f}")

    if fa * fb >= 0:
        print("❌ ERROR: f(a) dan f(b) harus memiliki tanda yang berbeda!")
        return None, 0, []

    # Cari true root (referensi) untuk perhitungan ε_t
    a_temp, b_temp = a, b
    for _ in range(100):
        c_temp = (a_temp + b_temp) / 2
        fc_temp = f(c_temp, *params)
        if f(a_temp, *params) * fc_temp < 0:
            b_temp = c_temp
        else:
            a_temp = c_temp
    true_root = c_temp
    print(f"\nTrue root (referensi): {true_root:.8f}")

    print(f"\n{'='*100}")
    print("PROSES ITERASI BISECTION (dengan rumus + hasil lengkap)")
    print("="*100)

    iterasi = 0
    c_prev = None
    history = []

    for i in range(max_iter):
        iterasi += 1
        c = (a + b) / 2
        fc = f(c, *params)

        # Hitung ε_a dan ε_t
        ε_a = abs((c - c_prev) / c) * 100 if c_prev else float('inf')
        ε_t = abs((true_root - c) / true_root) * 100

        history.append({
            'iterasi': iterasi,
            'a': a, 'b': b, 'c': c,
            'f(c)': fc,
            'ε_a': ε_a,
            'ε_t': ε_t,
            'lebar_interval': abs(b - a)
        })

        # ==================== PRINT DETAIL PER ITERASI ====================
        print(f"\n🔹 Iterasi {iterasi}")
        print(f"   Rumus c = (a + b) / 2")
        print(f"   c = ({a:.6f} + {b:.6f}) / 2 = {c:.6f}")

        print(f"\n   Rumus f(c) = (g*m/c) * (1 - exp(-c*t/m)) - v")
        print(f"   f({c:.6f}) = ({g} * {m} / {c:.6f}) * (1 - exp(-{c:.6f} * {t} / {m})) - {v}")
        print(f"             = {fc:.10f}")

        if c_prev:
            print(f"\n   Rumus ε_a = |(c_new - c_old) / c_new| * 100%")
            print(f"   ε_a = |({c:.6f} - {c_prev:.6f}) / {c:.6f}| * 100% = {ε_a:.6f}%")

        print(f"\n   Rumus ε_t = |(true_root - c) / true_root| * 100%")
        print(f"   ε_t = |({true_root:.8f} - {c:.6f}) / {true_root:.8f}| * 100% = {ε_t:.6f}%")

        # Tentukan interval baru
        if fa * fc < 0:
            print(f"\n   Karena f(a)*f(c) < 0 → akar di kiri → interval baru = [{a:.6f}, {c:.6f}]")
            b = c
            fb = fc
        else:
            print(f"\n   Karena f(a)*f(c) ≥ 0 → akar di kanan → interval baru = [{c:.6f}, {b:.6f}]")
            a = c
            fa = fc

        # Kriteria berhenti
        if abs(fc) < toleransi:
            print(f"\n✅ KONVERGEN: |f(c)| < toleransi setelah {iterasi} iterasi")
            break
        elif c_prev and ε_a < toleransi:
            print(f"\n✅ KONVERGEN: ε_a < toleransi setelah {iterasi} iterasi")
            break

        c_prev = c
    else:
        print(f"\n⚠️  Tidak konvergen setelah {max_iter} iterasi")

    return c, iterasi, history, true_root


def tampilkan_hasil_akhir(akar, iterasi, history, params, true_root):
    """
    Menampilkan hasil akhir dalam bentuk tabel
    """
    m, g, t, v = params
    
    print("\n" + "="*70)
    print("HASIL AKHIR")
    print("="*70)
    
    hasil_table = [
        ["Parameter", "Nilai", "Keterangan"],
        ["-"*50, "-"*20, "-"*30],
        ["Drag coefficient (c)", f"{akar:.8f}", "Akar persamaan"],
        ["f(c*)", f"{fungsi_parachutist(akar, *params):.10f}", "Nilai fungsi di akar"],
        ["True root (referensi)", f"{true_root:.8f}", "Untuk perhitungan ε_t"],
        ["Jumlah iterasi", f"{iterasi}", "Iterasi yang dilakukan"],
        ["Massa (m)", f"{m} kg", "Massa parachutist"],
        ["Gravitasi (g)", f"{g} m/s²", "Percepatan gravitasi"],
        ["Waktu (t)", f"{t} s", "Waktu free-fall"],
        ["Kecepatan (v)", f"{v} m/s", "Target kecepatan"]
    ]
    
    for row in hasil_table:
        print(f"{row[0]:25} {row[1]:20} {row[2]:30}")
    
    # Verifikasi hasil
    print("\n" + "="*70)
    print("VERIFIKASI HASIL")
    print("="*70)
    v_actual = (g * m / akar) * (1 - math.exp(-akar * t / m))
    verifikasi_table = [
        ["Parameter", "Nilai", "Selisih"],
        ["-"*25, "-"*15, "-"*15],
        ["Kecepatan target", f"{v:.6f} m/s", "-"],
        ["Kecepatan aktual", f"{v_actual:.6f} m/s", f"{abs(v_actual - v):.8f} m/s"]
    ]
    
    for row in verifikasi_table:
        print(f"{row[0]:25} {row[1]:15} {row[2]:15}")
    
    # Analisis error akhir
    print("\n" + "="*70)
    print("ANALISIS ERROR AKHIR")
    print("="*70)
    if len(history) > 1:
        final_ε_a = history[-1]['ε_a']
        final_ε_t = history[-1]['ε_t']
        print(f"ε_a (Approximate Error) akhir: {final_ε_a:.8f}%")
        print(f"ε_t (True Error) akhir: {final_ε_t:.8f}%")
        print(f"Selisih |akar - true_root|: {abs(akar - true_root):.10f}")

def tampilkan_sejarah_iterasi(history, akar):
    """
    Menampilkan sejarah iterasi dan jarak dari akar
    """
    print("\n" + "="*90)
    print("SEJARAH ITERASI DAN ERROR")
    print("="*90)
    print("Iter\t  c\t\t  f(c)\t\t  ε_a (%)\t  ε_t (%)\t  Jarak dari c*")
    print("-"*90)
    
    for h in history:
        jarak = abs(h['c'] - akar)
        print(f"{h['iterasi']:3d}\t{h['c']:8.6f}\t{h['f(c)']:10.6f}\t{h['ε_a']:8.4f}\t{h['ε_t']:8.4f}\t{jarak:.8f}")

def tampilkan_perkembangan_interval(history):
    """
    Menampilkan perkembangan interval
    """
    print("\n" + "="*60)
    print("PERKEMBANGAN INTERVAL")
    print("="*60)
    print("Iter\t  a\t\t  b\t\t  Lebar Interval")
    print("-"*60)
    
    for h in history:
        print(f"{h['iterasi']:3d}\t{h['a']:8.6f}\t{h['b']:8.6f}\t{h['lebar_interval']:.8f}")



def cari_interval_akar(f, x_min, x_max, step=1):
    """
    Mencari semua interval yang mengandung akar
    """
    print(f"\n🔍 MENCARI INTERVAL DENGAN PERUBAHAN TANDA")
    print(f"Range: {x_min} sampai {x_max}, Step: {step}")
    print("-" * 60)
    print("x\t\tf(x)\t\tTanda")
    print("-" * 60)
    
    intervals = []
    x_prev = x_min
    f_prev = f(x_prev)
    
    print(f"{x_prev:.2f}\t\t{f_prev:10.6f}\t\t{'+' if f_prev >= 0 else '-'}")
    
    x_current = x_prev + step
    while x_current <= x_max:
        f_current = f(x_current)
        print(f"{x_current:.2f}\t\t{f_current:10.6f}\t\t{'+' if f_current >= 0 else '-'}")
        
        # Cek perubahan tanda
        if f_prev * f_current <= 0:
            intervals.append((x_prev, x_current, f_prev, f_current))
            print(f"  → PERUBAHAN TANDA: akar antara [{x_prev:.2f}, {x_current:.2f}]")
        
        x_prev = x_current
        f_prev = f_current
        x_current += step
    
    return intervals

def metode_bisection_custom():
    """
    Metode Bisection untuk fungsi custom dari user dengan ε_a dan ε_t
    + menampilkan rumus dan hasil secara lengkap setiap iterasi
    """
    print("=== METODE BISECTION - FUNGSI CUSTOM ===")
    print("=" * 50)
    
    # Input fungsi dari user
    print("\n📝 MASUKKAN FUNGSI f(x) DALAM FORMAT PYTHON:")
    func_str = input("f(x) = ").strip()
    
    if not func_str:
        print("❌ Fungsi tidak boleh kosong!")
        return
    
    def f(x):
        try:
            return eval(func_str)
        except:
            print(f"❌ Error: Fungsi tidak valid untuk x = {x}")
            return None
    
    # Test fungsi
    print("\n🔍 TEST FUNGSI:")
    try:
        test_val = 1.0
        test_result = f(test_val)
        print(f"f({test_val}) = {test_result:.6f} ✓")
    except Exception as e:
        print(f"❌ Fungsi tidak valid: {e}")
        return
    
    # Input range pencarian
    print("\n📝 MASUKKAN RANGE PENCARIAN:")
    try:
        x_min = float(input("Nilai x minimum: "))
        x_max = float(input("Nilai x maksimum: "))
        step = float(input("Step size [default: 1]: ") or "1")
    except ValueError:
        print("❌ Input harus berupa angka!")
        return
    
    # Cari interval dengan perubahan tanda
    print(f"\n🔍 MENCARI INTERVAL DENGAN PERUBAHAN TANDA")
    print(f"Range: {x_min} sampai {x_max}, Step: {step}")
    print("-" * 60)
    print("x\t\tf(x)\t\tTanda")
    print("-" * 60)
    
    intervals = []
    x_prev = x_min
    f_prev = f(x_prev)
    
    print(f"{x_prev:.2f}\t\t{f_prev:10.6f}\t\t{'+' if f_prev >= 0 else '-'}")
    
    x_current = x_prev + step
    while x_current <= x_max:
        f_current = f(x_current)
        print(f"{x_current:.2f}\t\t{f_current:10.6f}\t\t{'+' if f_current >= 0 else '-'}")
        
        # Cek perubahan tanda
        if f_prev * f_current <= 0:
            intervals.append((x_prev, x_current, f_prev, f_current))
            print(f"  → PERUBAHAN TANDA: akar antara [{x_prev:.2f}, {x_current:.2f}]")
        
        x_prev = x_current
        f_prev = f_current
        x_current += step
    
    if not intervals:
        print("\n❌ TIDAK DITEMUKAN AKAR DALAM RANGE INI")
        return
    
    print(f"\n✅ DITEMUKAN {len(intervals)} INTERVAL YANG MENGANDUNG AKAR:")
    for i, (a, b, fa, fb) in enumerate(intervals, 1):
        print(f"{i}. Interval [{a:.2f}, {b:.2f}]")
        print(f"   f({a:.2f}) = {fa:.6f}, f({b:.2f}) = {fb:.6f}")
    
    # Pilih interval
    if len(intervals) == 1:
        a, b, fa, fb = intervals[0]
        print(f"\n✅ Menggunakan interval: [{a:.2f}, {b:.2f}]")
    else:
        print(f"\n📝 PILIH INTERVAL (1-{len(intervals)}):")
        choice = int(input("Pilih interval: ")) - 1
        if 0 <= choice < len(intervals):
            a, b, fa, fb = intervals[choice]
            print(f"✅ Interval dipilih: [{a:.2f}, {b:.2f}]")
        else:
            print("❌ Pilihan tidak valid!")
            return
    
    # Cari true root untuk perhitungan ε_t
    print("\n🔍 MENCARI TRUE ROOT UNTUK PERHITUNGAN ε_t...")
    a_temp, b_temp = a, b
    fa_temp, fb_temp = fa, fb
    
    for i in range(50):  # Iterasi banyak untuk true root
        c_temp = (a_temp + b_temp) / 2
        fc_temp = f(c_temp)
        if fa_temp * fc_temp < 0:
            b_temp = c_temp
            fb_temp = fc_temp
        else:
            a_temp = c_temp
            fa_temp = fc_temp
    
    true_root = c_temp
    print(f"✅ True root (referensi): {true_root:.8f}")
    print(f"   f(true_root) = {f(true_root):.12f}")
    
    # Input parameter metode
    print("\n⚙️  PARAMETER METODE:")
    try:
        toleransi = float(input("Toleransi error [default: 0.0001]: ") or "0.0001")
        max_iter = int(input("Maksimum iterasi [default: 100]: ") or "100")
    except ValueError:
        print("❌ Input harus berupa angka! Menggunakan nilai default.")
        toleransi = 0.0001
        max_iter = 100

    # ============================ TAMPILKAN RUMUS UMUM ============================
    print(f"\n{'='*80}")
    print("📐 RUMUS DAN PERHITUNGAN YANG DIGUNAKAN")
    print("="*80)
    
    print(f"\n🔹 FUNGSI YANG DISELESAIKAN:")
    print(f"   f(x) = {func_str}")
    print(f"   Cari x dimana f(x) = 0")
    
    print(f"\n🔹 RUMUS METODE BISECTION:")
    print(f"   1. c = (a + b) / 2")
    print(f"   2. Jika f(a) × f(c) < 0 → b = c")
    print(f"      Jika f(a) × f(c) ≥ 0 → a = c")
    print(f"   3. Ulangi hingga |f(c)| < toleransi atau ε_a < toleransi")
    
    print(f"\n🔹 RUMUS ERROR:")
    print(f"   ε_a = |(c_new - c_old) / c_new| × 100%")
    print(f"   ε_t = |(true_root - c) / true_root| × 100%")
    
    print(f"\n🔹 PERHITUNGAN AWAL:")
    print(f"   Interval: a = {a:.6f}, b = {b:.6f}")
    print(f"   f(a) = f({a:.6f}) = {fa:.6f}")
    print(f"   f(b) = f({b:.6f}) = {fb:.6f}")
    print(f"   f(a) × f(b) = {fa:.6f} × {fb:.6f} = {fa * fb:.6f}")
    
    if fa * fb < 0:
        print(f"   → f(a) × f(b) < 0 → ADA AKAR DI INTERVAL INI")
    else:
        print(f"   → f(a) × f(b) ≥ 0 → TIDAK ADA AKAR DI INTERVAL INI")
        return
    
    print(f"\n🔹 PARAMETER ITERASI:")
    print(f"   Toleransi: {toleransi}")
    print(f"   Maksimum iterasi: {max_iter}")
    print(f"   True root (referensi): {true_root:.8f}")

    # ============================ JALANKAN ITERASI DENGAN DETAIL ============================
    print(f"\n{'='*100}")
    print("PROSES ITERASI BISECTION (dengan rumus + hasil lengkap)")
    print("="*100)

    iterasi = 0
    c_prev = None
    history = []
    a_current, b_current = a, b
    fa_current, fb_current = fa, fb

    for i in range(max_iter):
        iterasi += 1
        c = (a_current + b_current) / 2
        fc = f(c)
        
        if fc is None:
            return

        # Hitung ε_a dan ε_t
        ε_a = abs((c - c_prev) / c) * 100 if c_prev is not None else float('inf')
        ε_t = abs((true_root - c) / true_root) * 100

        # Tentukan interval baru dan interval_info
        if fa_current * fc < 0:
            interval_info = "Kiri"
            b_next = c
            a_next = a_current
        else:
            interval_info = "Kanan"
            a_next = c
            b_next = b_current

        history.append({
            'iterasi': iterasi,
            'a': a_current, 'b': b_current, 'c': c,
            'f(c)': fc, 
            'ε_a': ε_a,
            'ε_t': ε_t,
            'interval': interval_info,  # PASTIKAN INI ADA!
            'lebar_interval': abs(b_current - a_current)
        })

        # ==================== PRINT DETAIL PER ITERASI ====================
        print(f"\n🎯 ITERASI {iterasi}")
        print("-" * 50)
        
        print(f"📐 Rumus: c = (a + b) / 2")
        print(f"   c = ({a_current:.6f} + {b_current:.6f}) / 2 = {c:.6f}")

        print(f"\n📐 Rumus: f(c) = {func_str}")
        print(f"   f({c:.6f}) = {func_str.replace('x', f'{c:.6f}')}")
        print(f"   Hasil: {fc:.10f}")

        if c_prev is not None:
            print(f"\n📐 Rumus: ε_a = |(c_new - c_old) / c_new| × 100%")
            print(f"   ε_a = |({c:.6f} - {c_prev:.6f}) / {c:.6f}| × 100%")
            print(f"       = |{c - c_prev:.6f} / {c:.6f}| × 100%")
            print(f"       = {abs((c - c_prev) / c):.6f} × 100% = {ε_a:.6f}%")

        print(f"\n📐 Rumus: ε_t = |(true_root - c) / true_root| × 100%")
        print(f"   ε_t = |({true_root:.8f} - {c:.6f}) / {true_root:.8f}| × 100%")
        print(f"       = |{true_root - c:.6f} / {true_root:.8f}| × 100%")
        print(f"       = {abs((true_root - c) / true_root):.6f} × 100% = {ε_t:.6f}%")

        # Tentukan interval baru
        if fa_current * fc < 0:
            print(f"\n🔍 Analisis: f(a) × f(c) = {fa_current:.6f} × {fc:.6f} = {fa_current * fc:.6f} < 0")
            print(f"   → Akar berada di interval kiri")
            print(f"   → Interval baru: [{a_current:.6f}, {c:.6f}]")
            b_current = c
            fb_current = fc
        else:
            print(f"\n🔍 Analisis: f(a) × f(c) = {fa_current:.6f} × {fc:.6f} = {fa_current * fc:.6f} ≥ 0")
            print(f"   → Akar berada di interval kanan")
            print(f"   → Interval baru: [{c:.6f}, {b_current:.6f}]")
            a_current = c
            fa_current = fc

        print(f"\n📊 Ringkasan Iterasi {iterasi}:")
        print(f"   c = {c:.6f}, f(c) = {fc:.10f}, ε_a = {ε_a:.6f}%, ε_t = {ε_t:.6f}%, Interval: {interval_info}")

        # Kriteria berhenti
        if abs(fc) < toleransi:
            print(f"\n✅ KONVERGEN: |f(c)| = {abs(fc):.10f} < toleransi {toleransi}")
            print(f"   setelah {iterasi} iterasi")
            break
        elif c_prev is not None and ε_a < toleransi:
            print(f"\n✅ KONVERGEN: ε_a = {ε_a:.6f}% < toleransi {toleransi}%")
            print(f"   setelah {iterasi} iterasi")
            break

        c_prev = c
    else:
        print(f"\n⚠️  Tidak konvergen setelah {max_iter} iterasi")

    # ============================ TAMPILKAN TABEL RINGKASAN ============================
    print(f"\n{'='*110}")
    print("RINGKASAN ITERASI (Format Tabel)")
    print("="*110)
    print("Iter\t   a\t\t   b\t\t   c\t\t  f(c)\t\t  ε_a (%)\t  ε_t (%)\t  Interval")
    print("-"*110)
    
    for h in history:
        # PASTIKAN SEMUA FIELD ADA SEBELUM DIPAKAI
        a_val = h.get('a', 0)
        b_val = h.get('b', 0)
        c_val = h.get('c', 0)
        fc_val = h.get('f(c)', 0)
        ε_a_val = h.get('ε_a', float('inf'))
        ε_t_val = h.get('ε_t', 0)
        interval_val = h.get('interval', 'N/A')
        
        if h['iterasi'] == 1:
            print(f"{h['iterasi']:3d}\t{a_val:8.6f}\t{b_val:8.6f}\t{c_val:8.6f}\t{fc_val:10.6f}\t{'':12}\t{ε_t_val:8.4f}%\t{interval_val}")
        else:
            print(f"{h['iterasi']:3d}\t{a_val:8.6f}\t{b_val:8.6f}\t{c_val:8.6f}\t{fc_val:10.6f}\t{ε_a_val:8.4f}%\t{ε_t_val:8.4f}%\t{interval_val}")

    # Tampilkan hasil akhir
    print(f"\n{'='*80}")
    print("HASIL AKHIR")
    print("="*80)
    
    # Gunakan nilai akhir dari iterasi
    akar = c
    f_akar = fc
    ε_a_akhir = ε_a
    ε_t_akhir = ε_t
    
    hasil_table = [
        ["Parameter", "Nilai", "Keterangan"],
        ["-"*25, "-"*15, "-"*30],
        ["Akar (x)", f"{akar:.8f}", "Solusi persamaan f(x) = 0"],
        ["f(akar)", f"{f_akar:.10f}", "Nilai fungsi di akar"],
        ["True root", f"{true_root:.8f}", "Referensi untuk ε_t"],
        ["Jumlah iterasi", f"{iterasi}", "Iterasi yang dilakukan"],
        ["ε_a akhir", f"{ε_a_akhir:.6f}%", "Approximate error terakhir"],
        ["ε_t akhir", f"{ε_t_akhir:.6f}%", "True error terakhir"],
        ["Selisih", f"{abs(akar - true_root):.10f}", "|akar - true_root|"]
    ]
    
    for row in hasil_table:
        print(f"{row[0]:20} {row[1]:15} {row[2]:30}")
    
    # Analisis error
    print(f"\n{'='*80}")
    print("ANALISIS ERROR")
    print("="*80)
    print(f"ε_a (Approximate Error): Mengukur perubahan antara iterasi")
    print(f"ε_t (True Error): Mengukur jarak dari solusi sebenarnya")
    print(f"True root dicari dengan 50 iterasi tambahan untuk akurasi maksimal")
    
    if ε_t_akhir < 0.001:
        print("✅ ε_t < 0.001%: Solusi sangat akurat!")
    elif ε_t_akhir < 0.1:
        print("✅ ε_t < 0.1%: Solusi akurat")
    else:
        print("⚠️  ε_t > 0.1%: Solusi masih bisa ditingkatkan")
    
    return akar, iterasi, history, true_root