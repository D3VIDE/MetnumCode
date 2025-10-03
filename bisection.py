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
    Metode Bisection untuk mencari akar persamaan
    """
    fa = f(a, *params)
    fb = f(b, *params)
    
    print(f"\n" + "="*70)
    print("INFORMASI INTERVAL AWAL")
    print("="*70)
    print(f"a = {a:.6f}, f(a) = {fa:.6f}")
    print(f"b = {b:.6f}, f(b) = {fb:.6f}")
    print(f"f(a) × f(b) = {fa * fb:.6f}")
    
    if fa * fb >= 0:
        print("❌ ERROR: f(a) dan f(b) harus memiliki tanda yang berbeda!")
        return None, 0, []
    
    print("\n" + "="*90)
    print("PROSES ITERASI BISECTION")
    print("="*90)
    print("Iter\t   a\t\t   b\t\t   c\t\t  f(c)\t\t  Error%\t  Interval")
    print("-"*90)
    
    iterasi = 0
    c_prev = 0
    history = []
    
    for i in range(max_iter):
        iterasi += 1
        c = (a + b) / 2
        fc = f(c, *params)
        
        # Hitung error
        if i > 0:
            error = abs((c - c_prev) / c) * 100
        else:
            error = 100
        
        # Tentukan interval mana yang mengandung akar
        if fa * fc < 0:
            interval_info = "Kiri (I_1a)"
            b_next = c
            a_next = a
        else:
            interval_info = "Kanan (I_1b)"
            a_next = c
            b_next = b
        
        history.append({
            'iterasi': iterasi,
            'a': a, 'b': b, 'c': c,
            'f(c)': fc, 'error': error,
            'interval': interval_info,
            'lebar_interval': abs(b - a)
        })
        
        print(f"{iterasi:3d}\t{a:8.6f}\t{b:8.6f}\t{c:8.6f}\t{fc:10.6f}\t{error:8.4f}%\t{interval_info}")
        
        # Cek kriteria berhenti
        if abs(fc) < toleransi:
            print(f"\n✅ KONVERGEN: f(c) < toleransi setelah {iterasi} iterasi")
            break
        elif i > 0 and error < toleransi:
            print(f"\n✅ KONVERGEN: Error < toleransi setelah {iterasi} iterasi")
            break
        
        # Update interval
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
        
        c_prev = c
    else:
        print(f"\n⚠️  Tidak konvergen setelah {max_iter} iterasi")
    
    return c, iterasi, history

def tampilkan_hasil_akhir(akar, iterasi, history, params):
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

def tampilkan_sejarah_iterasi(history, akar):
    """
    Menampilkan sejarah iterasi dan jarak dari akar
    """
    print("\n" + "="*80)
    print("SEJARAH ITERASI DAN JARAK DARI c*")
    print("="*80)
    print("Iter\t  c\t\t  f(c)\t\t  Error%\t  Interval\t\tJarak dari c*")
    print("-"*80)
    
    for h in history:
        jarak = abs(h['c'] - akar)
        print(f"{h['iterasi']:3d}\t{h['c']:8.6f}\t{h['f(c)']:10.6f}\t{h['error']:7.3f}%\t{h['interval']:15}\t{jarak:.8f}")

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