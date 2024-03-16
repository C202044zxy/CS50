import numpy as np

batch = 1
rows = 3
cols = 3

a = np.zeros((batch, rows, cols), dtype = int)

print(type(a))
print(a.tolist())

a = 1.0
A = int(a)
print(A)