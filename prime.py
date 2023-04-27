import random
import math

def is_prime(n):
    # Returns True if n is prime, False otherwise.
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def modpow(base, exponent, modulus):
    # Returns (base**exponent) % modulus
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base * base) % modulus
    return result

def find_prime(bits):
    # Returns a random prime number with the specified number of bits.
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p

def find_primitive_root(p):
    # Returns the smallest primitive root of the prime p.
    phi = p - 1
    factors = factorize(phi)
    for g in range(2, p):
        if all(modpow(g, phi // f, p) != 1 for f in factors):
            return g

def factorize(n):
    # Returns a list of the prime factors of n.
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n = n // i
        i += 2
    if n > 1:
        factors.append(n)
    return factors



