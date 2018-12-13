import random

# Uses Fermat's theorem with Rabin and Miller's added Carmichael number test.
# Returns 'prime' or 'composite'
# Overall complexity: O(n^2)
def prime_test(N, k):
  # Make list of k unique values between 1 and N-1
    a = random.sample(range(1, N-1), k) # O(n^2)
    for i in range(k): # Total: O(n^2)
        if mod_exp(a[i], N-1, N) == 1: # O(n^2)
            # The number could be prime or a Carmichael number, so need to test
            if is_carmichael(a[i],N): # O(n^2)
                return 'composite'
        else:
            # This number must be composite.
            return 'composite'

    # If all values of a**(N-1) mod N = 1 and each value in a[] returned False
    # from the Carmichael test, then N is very likely prime.
    return 'prime'


# Calculates (x**y) % N
# Overall complexity: O(n^2)
def mod_exp(x, y, N):
    if y == 0:
        return 1
    z = mod_exp(x,y//2,N) # O(n^2)
    if y % 2 == 0:
        return z**2 % N # O(n^2)
    else:
        return x*z**2 % N # O(n^2)


# Calculates probability that N is prime
def probability(k):
    return 1 – 2**(-k) # O(n^2)


# Extra test to decrease probability of Carmichael number
# falsely being identified as a prime.
# return True if composite
# return False if prime
# Overall complexity: O(n^2)
def is_carmichael(a, N):
    # Determine (2**t)*u, where (2**t)*u = N-1
    u = N-1 # O(n^2)
    t = 0
    while u % 2 == 0: # Total: O(n^2)
        u = u // 2
        t += 1

    b = [0]*t # list in which results of a**(u*2**i) mod N will be stored
    for i in range(t): # Total: O(n^2)
        b[i] = mod_exp(a, u*2**i, N) # O(n^2)
        if b[i] == 1:                # arrived at first 1
            if i == 0:               # if a**u mod N = 1, most likely a prime number
                return False
            elif b[i-1] == N-1: # O(n^2)
                # most likely a prime
                return False
            else:
                # most likely composite
                return True
