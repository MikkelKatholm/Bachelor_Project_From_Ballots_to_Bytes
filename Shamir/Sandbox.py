import sympy as sp

a = sp.Matrix([[1,2,3],[4,5,6],[7,8,9]])
b = sp.Matrix([[4,5,6],[7,8,9],[1,2,3]])

print(int(a.det()))
print(int(b.det()))