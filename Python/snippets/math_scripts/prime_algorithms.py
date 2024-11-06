# Checks if two numbers are prime.

import math


#simple function for least common multiple
def lcm(x,y):
    return abs(x * y) // math.gcd(x, y)


def trial_division(n):
    """Return a list of prime factors for a natural number in the form (prime, power),
        e.g. 2^10 is represented as (2,10). Returns all factors.
    
    Systematically tests if n is divisible by any smaller number

    Remember: 
    * A natural number is 50% likely to be even
    * A natural number is 33% likely to be divisible by 3
    * We only need to test up to sqrt(n), because, if n is divisible by some number p,
        then n = p*q, and if q were smaller than p, n would have been detected earlier
        as a being divisible q or by a prime factor of q
    * All ints are in the form 6k + i, where -1 <= i <= 4
    * All ints divisible by 2 or 3 are composite
    * All ints in form (6k+0), (6k+2), (6k+4) are divisible by 2
    * All ints in form (6k+3) are divisible by 3
    * Therefore, primes must be in the form 6k +/- 1 for k > 3

    Time complexity approaches O(sqrt(n)/6)
    """

    # prepare empty list
    factors = []

    # any natural number <= 3 is prime
    if n <= 3:
        return [(n, 1)]
    
    # All even ints > 2 are composite (50% of nat numbers)
    # All ints divisible by 3 are composite (33% natural numbers)
    for factor in [2,3]:
        i = 0
        if n % factor == 0:
            while n % factor == 0:
                i += 1
                n //= factor
            factors.append((factor, i))

    # All primes are in the form 6k +/- 1
    factor = 5
    while factor <= (n**0.5 + 1):
        # factor 6k + 1 first
        if n % (factor + 2) == 0:
            i = 0
            while n % (factor + 2) == 0:
                i += 1
                n //= (factor + 2)
            factors.append((factor + 2, i))
            
        # Then factor 6k - 1
        if n % factor == 0:
            i = 0
            while n % (factor) == 0:
                i += 1
                n //= factor
            factors.append((factor, i))
        factor += 6
    if n != 1:
        factors.append((n,1))
    return factors

def seive_of_eratosthenes(limit):
    """Calculates a list of prime up to int limit using seive of Eratosthenes
    
    Iteratively marks all multiples of a prime as composite in a given range 
    starting at 2.

    Time complexity is O(n log log n)
    """

    # A list with value True as long as int limit (the max int we want to 
    # compute the primes for)
    seive = [True] * limit
    # Prime numbers found
    primes = []

    for i in range(2, limit):
        # iterates through list until a prime (true in list seives) is found
        # The prime is represented as the index of the list
        if seive[i]:
            # add prime (index) to list of primes
            primes.append(i)
            # Set all multiples of the prime (up to limit) to False to 
            # indicate that number is composite
            for prime_mult in range(i, limit, i):
                seive[prime_mult] = False
    return primes

def pollard_rho(n):
    """Used to factorize a number n = p*q, where p is a non-trivial factor. Only returns one factor
    
    * A polynomial modulo n, called g(x), is used to generate a pseudo-random 
        sequence. This must be polynomial, and should have an added arbitrary 
        c value
    * A starting value, say 2, is chosen, and the sequence continues as 
        x_1 = g(2), x_2 = g(g(2)), x_3 = g(g(g(2))), etc. 
    * 2 variables are initialised at the same value. One value T, the tortoise,
        will have g(t) interatively applied to it. A second value H, the hare,
        will have g(g(h)) iteratively applied to it.
    * The greatest common denominator of T - H and n is taken.
        If gcd(T - H, n) > 1, there are two cases.
        * T = H -> gcd(0,n) = n. This is a fail state, and c is changed
        * T != H -> gcd(T - H, n) = d, d|n and is non-trivial
    * One of those two options must occur. The claim us that the and the first 
        result is not likely, and if the second result occurs, it will happen
        quickly
    """
    def trial(g):
        # tortoise and hare values
        t = 2
        h = 2

        # Keep repeating until the greatest common denominator of
        # the difference of t and h and n is > 0
        while True:
            t = g(t)
            h = g(g(h))
            d = math.gcd(t - h, n)

            # When t - h = n, algorithm fails, even if n is composite.
            # If this happens, try again with a different value of c
            if d == n:
                return False
            elif d > 1:
                return d
            
    c = 1
    while True:
        # Polynomial modulus function used to generate 
        # a pseudorandom sequence using a arbitrary c
        def g(x):
            return (x**2 + c) % n
        d = trial(g)
        if d:
            return d
        c += 1

def use_algorithms(input_val):
    print("Use trial division to print the prime factors of the entered number:")
    factors = trial_division(int(input_val))
    print("Factors are: ", end='')
    for factor in factors:
        for prime in range(factor[1]):
            print(factor[0], end=' ')
    print()
    print()

    print("Print a list of all primes less than the entered number using the Seive of Eratosthenes:")
    primes = seive_of_eratosthenes(input_val)

    # Check if user wants to print full list of primes if list is long
    if len(primes) > 100:
        # Defaults to No
        print_all = str(input("The list of primes is longer than 100 primes. Display all of them? [y/N] ") or "No")
        if print_all.strip().lower()[0] == "y":
            limit = len(primes)
        else:
            # If they don't want to print the whole list, see how many they want to print
            try:
                limit = int(input("Enter number of primes to print from end of list (Default 100): ") or "100")
            except ValueError:
                print("Invalid value! Defaulting to 100")
                limit = 100
        if limit > len(primes): limit = len(primes)
    else:
        limit = len(primes)

    print(f"Printing {limit} primes:")
    i = 0
    for x in range( len(primes) - limit, len(primes)):
        if i % 5 == 0:
            print()
        print(f"{primes[x]}\t", end=' ')
        i += 1
 
    print()

    
if __name__ == "__main__":
    """print("This program is practice for prime algorithms.")
    print("If a float is entered, it will be truncated to a string.")
    try:
        input_val = int(float(input("Enter a number: ")) // 1)
        use_algorithms(input_val)
    except ValueError:
        print("Invalid Input!")"""
    from rsa.prime import getprime
    import timeit

    bits = 96

    def test_rho():
        p, q = getprime(bits // 2), getprime(bits // 2)
        n = p*q
        print(f"p={p}, q={q}, n={n}")
        d = pollard_rho(n)

    def test_trial_div():
        p, q = getprime(bits // 2), getprime(bits // 2)
        n = p*q
        print(f"p={p}, q={q}, n={n}")
        d = trial_division(n)

    print("Pollard Rho Algorithm:")
    res = timeit.Timer(test_rho).timeit(number = 100)
    print(f"Pollard Rho: Average of {round(res, 3)}s for {bits} bits")
    print()
    print()

    #print("Trial Division Algorithm")
    #res = timeit.Timer(test_trial_div).timeit(number=100)
    #print(f"Trial Division: Average of {round(res, 3)}s for {bits} bits")

    
    
    