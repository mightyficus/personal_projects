"""
Notes on Elliptic curve cryptology

Projective planes:
    Projective planes are an extension of the Euclidean plane - it essentially involves
    adding a "horizon line," or a line that represents infinity. Using this, we can extend
    the Fundamental Theorem of Algebra to generalize elliptic curves.
Fundamental Theorem of Algebra:
    A polynomial of degree n can have, at most, n roots (Where the polynomial intersects
    y=0), and has *exactly* n roots when counting complex numbers and multiplicities
Bezouts Theorem:
    Two algebraic curves of degrees m and n that have no common components can have, at
    most, mn points of intersection, and it has *exactly* mn points when including complex
    numbers, multiplicities, and points at infinity
Homogeneous coordinates:
    Embed a n-dimensional plane on a n+1-dimensional plane (like a line on a 2-d plane).
    Every point on that line, called the point range, can be paired with a line through the 
    origin. If the point (a,1) on the line y=1, then the equation of the line is x=ay.
    This gives us a 1:1 correspondance with the range of points with the set of all lines
    passing through the origin, called a pencil of lines.   
    Any line that goes through the point (a,1) can be scaled by an arbitrary value k, and 
    still be on the same line. The ratio between the x and y coordinates remain invariant,
    as long as the point remains on the same line: x:y = kx:ky (except on the origin).
    Therefore, we use the notation (x:y) to refer to points on the line, with the 
    understanding that for any non-zero value of k, the points (x:y) and (kx:ky) really
    represent the same point, because they are connected to the same line through the origin.
    As a result, the line at y=0, which corresponds to the point at infinity, will always have 
    a y-value of 0, so the notation for the point at infinity is (x:0).
    The only invalid coordinate is (0:0), because the origin is on every line, and cannot be 
    used to describe any one line.
    This also maps to higher degree planes, such as a 2D plane in 3D space. For any line in 3D
    space, it can be mapped to a projected coordinate of (x:y:z). However, any horizontal line on the 
    Projectively extended real line
        There is only one line that cannot be reached this way, which is y=0. However, we can 
        let the horizontal line through the origin correspond to the point at infinity.
        An important distinction between the extended real line and the projectively extended
        real line is that the projectively extended real line has a neutral infinity, as opposed 
        to signed infinities.

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

def lenstra_curve_algorithm(n, limit):
    """Lentstra's Elliptic-curve algoritm for factoring. Limit is max work permitted
    
    Lenstra's Elliptic curve factorization algorithm (ECM). ECM has a sub-exponential
    factoring time, and is specialized for factoring divisors not exceeding 60 digits, 
    as its running time is determined by the size of the smallest factor p, and not the
    size of the number to be factored. ECM is often used to remove small factors from 
    very large composite integers
    """
    # Pick a random Elliptic curve over Z/Zn (the integer's modulo n), with equation
    # of the form y**2 = x**3 + a*x + b (mod n) together with a non-trivial point P(x0, y0)
    g = n
    while g == n:
        # randomized x, y
        q = randint(0, n-1), randint(0, n-1), 1
        # randomize the curve coefficient a and compute b with equation
        # b = y0**2 - x0**3 - a*x0
        a = randint(0, n-1)
        b = (q[1]**2 - q[0]**3 - a*q[0])
        # Check that curve is non-singular, meaning the curve has no cusps, self-intersections, 
        # or isolated points. This can be done by checking that the discriminant d computed by 
        # 4a**3 + 27b**2 != 0
        g = gcd(4 * a**3 + 27 * b**2, n)