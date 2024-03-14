import numpy as np
import galois

# Define the finite field
GF = galois.GF(5)  # For example, using GF(5) for finite field with 5 elements

# Define the coefficient matrix and the constant vector
A = GF([
    [1, 2, 3],
    [4, 3, 2],
    [2, 0, 4]
])
b = GF([3, 4, 1])

# Concatenate A and b to form the augmented matrix
augmented_matrix = np.concatenate((A, b[:, np.newaxis]), axis=1)

# Perform row reduction to transform the matrix to row-echelon form
row_echelon_form = galois.GF2Matrix(augmented_matrix).row_reduce()

# Back-substitute to find the solutions
solutions = galois.GF2Matrix.backsubstitute(row_echelon_form)

print("Solutions:", solutions)
