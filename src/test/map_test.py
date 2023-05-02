import numpy

A = [[0 for j in range(400)] for i in range(900)]
B = [[0 for j in range(900)] for i in range(400)]

for i in range(900):
    for j in range(400):
        A[i][j] = 2 * i + 3 * j

for i in range(400):
    for j in range(900):
        B[i][j] = 3 * i - 2 * j

AxB = [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]

sum = 0
for i in range(len(AxB)):
    for j in range(len(AxB[0])):
        sum += AxB[i][j]

print(sum)

print(numpy.array(A))
print(numpy.array(B))
print(numpy.array(AxB))
print(numpy.array(AxB).sum())
