def euclid_ext(a, b):
    if b == 0:
        return (1, 0, a)
    x, y, d = euclid_ext(b, a % b)
    return (y, x - (a//b)*y, d)

# print(gcd_factor(210, 588))
# print(gcd_euclid(25, 11))

def rsa(p, q, N, e, M):
    a = e
    b = (p - 1) * (q - 1)
    y, _, _ = euclid_ext(a,b)
    if y < 0:
        y = b + y
    d = y

    encryption = M**3 % N
    print("d =",d)
    print("y =", encryption)

rsa(17, 23, 391, 3, 41)
