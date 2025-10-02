import numpy as np

def gauss_seidel_solver(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Menyelesaikan sistem persamaan linear Ax = b menggunakan metode Gauss-Seidel
    
    Parameters:
    A : matriks koefisien (n x n)
    b : vektor hasil (n x 1)
    x0 : tebakan awal (default: vektor nol)
    tol : toleransi error
    max_iter : maksimum iterasi
    
    Returns:
    x : solusi
    iterations : data iterasi
    """
    
    n = len(b)
    if x0 is None:
        x = np.zeros(n)
    else:
        x = x0.copy()
    
    iterations = []
    
    # Iterasi 1
    iterations.append({
        'iterasi': 1,
        'x1': x[0],
        'x2': x[1], 
        'x3': x[2],
        'εa x1': '-',
        'εa x2': '-',
        'εa x3': '-'
    })
    
    for k in range(1, max_iter):
        x_old = x.copy()
        
        # Iterasi Gauss-Seidel
        for i in range(n):
            sigma = 0
            for j in range(n):
                if j != i:
                    sigma += A[i, j] * x[j]
            x[i] = (b[i] - sigma) / A[i, i]
        
        # Hitung error aproksimasi
        errors = []
        for i in range(n):
            if x_old[i] != 0:
                error = abs((x[i] - x_old[i]) / x[i]) * 100
            else:
                error = 100.0
            errors.append(error)
        
        # Simpan data iterasi
        iterations.append({
            'iterasi': k + 1,
            'x1': x[0],
            'x2': x[1],
            'x3': x[2],
            'εa x1': errors[0],
            'εa x2': errors[1],
            'εa x3': errors[2]
        })
        
        # Cek konvergensi
        if max(errors) < tol:
            break
    
    return x, iterations

def print_iteration_table(iterations):
    """Mencetak tabel iterasi dalam format yang rapi"""
    print(f"{'Iterasi':<8} {'x1':<15} {'x2':<15} {'x3':<15} {'εa x1':<12} {'εa x2':<12} {'εa x3':<12}")
    print("-" * 80)
    
    for it in iterations:
        print(f"{it['iterasi']:<8} {it['x1']:<15.9f} {it['x2']:<15.9f} {it['x3']:<15.9f} ", end="")
        
        if isinstance(it['εa x1'], str):
            print(f"{it['εa x1']:<12} {it['εa x2']:<12} {it['εa x3']:<12}")
        else:
            print(f"{it['εa x1']:<12.6f} {it['εa x2']:<12.6f} {it['εa x3']:<12.6f}")

# Contoh penggunaan berdasarkan data Anda
def main():
    # Matriks koefisien A dan vektor b
    A = np.array([
        [3, -0.1, -0.2],
        [0.1, 7, -0.3],
        [0.3, -0.2, 10]
    ], dtype=float)
    
    b = np.array([7.85, -19.3, 71.4], dtype=float)
    """
    | 1    0  0|
    |0.1   1  0|
    |0.3 -0.2 1|
    """
    print("Sistem Persamaan Linear:")
    print("3x1 - 0.1x2 - 0.2x3 = 7.85")
    print("0.1x1 + 7x2 - 0.3x3 = -19.3")
    print("0.3x1 - 0.2x2 + 10x3 = 71.4")
    print("\n" + "="*80)
    
    # Menyelesaikan dengan Gauss-Seidel
    solusi, iterations = gauss_seidel_solver(A, b, tol=1e-12, max_iter=12)
    
    print("Hasil Iterasi Gauss-Seidel:")
    print_iteration_table(iterations)
    
    print(f"\nSolusi akhir: x1 = {solusi[0]:.10f}, x2 = {solusi[1]:.10f}, x3 = {solusi[2]:.10f}")

if __name__ == "__main__":
    main()