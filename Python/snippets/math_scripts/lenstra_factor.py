"""
Factor an integer using the lenstra curve algorithm
"""

from random import randint
from fractions import gcd


def prime_list(limit):
    """Calculates a list of prime up to int limit
    
    Calculates a list of primes using the Seive of Eratosthenes. This algorithm
    iteratively marks all multiples of a prime as composite in a given range 
    starting at 2.
    """

    # A list with value True as long as int limit (the max int we want to 
    # compute the primes for)
    seive = [True] * limit
    # Prime numbers found
    primes = []

    for i in range(2, limit+1):
        # iterates through list until a prime (true in list seives) is found
        # The prime is represented as the index of the list
        if seive[i]:
            # add prime (index) to list of primes
            primes.append(i)
            # Set all multiples of the prime (up to limit) to False to 
            # indicate that number is composite
            for prime_mult in range(i, limit+1, i):
                seive[prime_mult] = False
    return primes

def modular_inv(a,b):
    """Finds modular inverse
    Only numbers coprime to b have a modular inverse (mod c)
    
    Returns inverse, unused helper and gcd
    """
    if b == 0:
        return 1, 0, a
    q,r = divmod(a, b)
    x,y,g = modular_inv(b,r)
    return y, x - q * y, g

# def lenstra_curve_algorithm(n, limit):
#     """Lentstra's Elliptic-curve algoritm for factoring. Limit is max work permitted
    
#     Lenstra's Elliptic curve factorization algorithm (ECM). ECM has a sub-exponential
#     factoring time, and is specialized for factoring divisors not exceeding 60 digits, 
#     as its running time is determined by the size of the smallest factor p, and not the
#     size of the number to be factored. ECM is often used to remove small factors from 
#     very large composite integers
#     """
#     # Pick a random Elliptic curve over Z/Zn (the integer's modulo n), with equation
#     # of the form y**2 = x**3 + a*x + b (mod n) together with a non-trivial point P(x0, y0)
#     g = n
#     while g == n:
#         # randomized x, y
#         q = randint(0, n-1), randint(0, n-1), 1
#         # randomize the curve coefficient a and compute b with equation
#         # b = y0**2 - x0**3 - a*x0
#         a = randint(0, n-1)
#         b = (q[1]**2 - q[0]**3 - a*q[0])
#         # Check that curve is non-singular, meaning the curve has no cusps, self-intersections, 
#         # or isolated points. This can be done by checking that the discriminant d computed by 
#         # 4a**3 + 27b**2 != 0
#         g = gcd(4 * a**3 + 27 * b**2, n)

