import numpy as np

x = np.zeros((4, 4), dtype=np.int)
print(x)

x[0][0] = 1
x[3][3] = 16

print(x)

y = x[:, ::-1]
print(y)
