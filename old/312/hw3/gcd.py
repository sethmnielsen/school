def gcd_factor(a, b):
    min = b
    if b > a:
        min = a
    com_factors = []
    for i in range(2,min // 2):
        if a % i == 0 and b % i == 0:
            com_factors.append(i)

    return com_factors[-1]

def gcd_euclid(a, b):
    if b == 0:
        return a

    return gcd_euclid(b, a % b)

def euclid_ext(a, b):
    if b == 0:
        return (1, 0, a)
    x, y, d = euclid_ext(b, a % b)
    return (y, x - (a//b)*y, d)

# print(gcd_factor(210, 588))
# print(gcd_euclid(25, 11))

a = 5
b = 23
y, x, d = euclid_ext(a,b)
if (a * y) % b == 1:
    if y < 0:
        y = b + y
    print(y)
else:
    print("No inverse")
