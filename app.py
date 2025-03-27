print("A3ti zebbi ra9m")
n = int(input())

isPrime = True

for i in range(2,n):
    if n%i == 0:
        isPrime = False

if isPrime:
    print("Behy he4a primaire")
else:
    print("Tet9ou7eb, mosh primaire he4a")
