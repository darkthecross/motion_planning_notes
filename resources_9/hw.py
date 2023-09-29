import numpy as np

x = np.array([1, 1], dtype=np.float64)
A = np.array([[2, 1], [1, 2]], dtype=np.float64)
b = np.array([0, 1], dtype=np.float64)

print(x)
print(np.matmul(A, x))
print(np.matmul(np.transpose(x), A))

def tar_val(xx):
    return np.matmul(np.matmul(np.transpose(xx), A), xx) + np.matmul(np.transpose(b), xx)

print(tar_val(x))

for i in range(20):
    grad = 2 * np.matmul(np.transpose(x), A) + b
    x = x - 0.1 * grad
    print(f"step: {i}, x: {x}")
    print(tar_val(x))
