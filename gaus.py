import numpy as np

def print_matrix(M):
    """Tampilkan matriks augmented dengan format 2 desimal"""
    rows, cols = M.shape
    for i in range(rows):
        row_str = " ".join(f"{M[i][j]:10.2f}" for j in range(cols))
        print(row_str)
    print("-" * 60)


def gauss_elimination(A, b):
    n = len(b)
    aug = np.hstack((A, b.reshape(-1, 1)))

    print("\n==================== PROSES ELIMINASI GAUSS ====================")
    for i in range(n):
        if aug[i][i] == 0:
            for j in range(i+1, n):
                if aug[j][i] != 0:
                    aug[[i, j]] = aug[[j, i]]
                    print(f"\nTukar baris {i+1} dengan baris {j+1} untuk menghindari pivot 0")
                    break

        pivot = aug[i][i]
        print(f"\nLangkah {i+1}: Eliminasi kolom {i+1}")
        print(f"Pivot = {pivot:8.2f}")

        aug[i] = aug[i] / pivot  # Normalisasi baris pivot

        for j in range(i+1, n):
            faktor = aug[j][i]
            aug[j] = aug[j] - faktor * aug[i]
            print(f"  Baris {j+1} = Baris {j+1} - ({faktor:6.2f}) × Baris {i+1}")

        print("\nMatriks setelah langkah ini:")
        print_matrix(aug)

    return aug


def backward_substitution(aug):
    n = len(aug)
    x = np.zeros(n)
    print("\n==================== PROSES SUBSTITUSI BALIK ====================")

    for i in reversed(range(n)):
        total = sum(aug[i][j] * x[j] for j in range(i+1, n))
        eq = " + ".join([f"({aug[i][j]:6.2f})x{j+1}" for j in range(n)])
        print(f"\nPersamaan {i+1}: {eq} = {aug[i][-1]:8.2f}")
        print(f"Hitung x{i+1}: x{i+1} = ({aug[i][-1]:8.2f} - {total:8.2f}) / {aug[i][i]:6.2f}")
        x[i] = (aug[i][-1] - total) / aug[i][i]
        print(f"→ x{i+1} = {x[i]:8.2f}")

    return x
