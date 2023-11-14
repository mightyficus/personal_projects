# This program currently only checks if two numbers are prime.

# Eventually, this program aims to generate an RSA keypair, given p, q, and e
# I may update it later so that it's able to generate a keypair when only given p and q
# Because in RSA encryption e is usually 35537, I will use that as the default.
# I will also check p and q to make sure they are prime numbers. The algorithm for that 
# is interesting, so I will also add a description for that function. 


import sys
import math
import os
from random import randint


#simple function for least common multiple
def lcm(x,y):
    return abs(x * y) // math.gcd(x, y)

# This method determines if a number is prime using trial division
# If a number n is evenly divisible by any prime number between 2 and sqrt(n),
# It's composite. Otherwise, it's prime.
# There are further optimisations we can make.
# For example, all even numbers > 2 can be eliminated, because if a number is
# divisible by an even number, it is also divisible by 2.
# In addition, all primes > 3 come in the form 6k +/- 1, where K is any integer > 0:
# All integers can be expressed as 6k + i, where i is -1, 0, 1, 2, 3, or 4
# We can eliminate 4 because it is even. 2 divides (6k+0), (6k+2), and (6k+4).
# 3 divides (6k+3). Therefore, it is most efficient to try to divide n by 2, 3, and
# then each number (6k +/- 1) <= root(n). This is 3x faster than testing all ints < sqrt(n).

# Tests primality with 6k +/- 1 optimisation
def isPrime(n):
    # the 6k+/- 1 optimisation only works for primes > 3
    if n <= 3:
        return n > 1
    if not (n % 2) or not (n % 3):
        return False

    for i in range(5, int(n**0.5) + 1, 6):
        if not (n % i) or not (n % (i + 2)):
            return False
    return True

'''
1. Choose 2 large prime numbers, p and q (these will be provided by the user)
2. compute n = pq 
3. Compute gamma(n) using charmichael's totient function
    a. since n = pq, gamma(n) = lcm(gamma(p), gamma(q)), and since pa and q are
       prime, gamma(p) = p-1, and likewise gamma(q) = q-1. Hence, gamma(n) = lcm(p-1, q-1)
4. Coose an integer e such that 1 < e < gamma(n) and gcd(e, gamma(n)) = 1; that is, e and n
   are coprime (e should b provided by user, else e = 35537)
5. Determine d as d == e**-1(mod(gamma(n))); that is, d is the modular multiplicative inverse
   of e (mod gamma(n))
    a. This is normally solved using the extended Euclidian algorithm, but python has a built
       in function for this: d = pow(e, -1, gamma(n))
The public key  consists of the the modulus n and the public exponent e. The private key consists
of the private exponent d (this is calculated using p, q, and gamma(n))
'''
#generates the integers needed for the keys
def RSAInts(p, q, e):
    n = q * q                           # p and q are 2 large prime numbers
    gamma_n = math.lcm(p-1, q-1)        # gamma(n) is calculated using carmichael's totient function
    d = pow(e, -1, gamma_n)

    publicKey = (n, e)
    privateKey = (n, d)

    print('Public key:', publicKey)
    print('Private key:', privateKey)

    return (publicKey, privateKey)

def makeKeyFile(name, keySize, p, q, e=35537):
    #safety check, make sure we aren't overwriting an existing key
    if os.path.exists('%s_pubkey.txt' % (name)) or os.path.exists('%s_privkey.txt' % (name)):
        sys.exit('WARNING: The file %s_pubkey.txt or %s_privkey.txt already exists! Use a different name or delete these files and re-run this program.' % (name, name))

    publicKey, privateKey = RSAInts(p, q, e)

    print()
    print('The public key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Writing public key to file %s_pubkey.txt...' % (name))

    with open('%s_pubkey.txt' % (name), 'w') as of:
        of.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
    
    print()
    print('The private key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Writing private key to file %s_privkey.txt...' % (name))
    with open('%s_privkey.txt' % (name), 'w') as of:
        of.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))

def check_prime():
    try:
        prime_1 = int(float(input("Enter the first number: ")) // 1)
        prime_2 = int(float(input("Enter the second number: ")) // 1)
    except ValueError:
        print("Input not a number!")
    primeness = isPrime(int(prime_1))
    if primeness:
        print(prime_1, "is prime!")
    else:
        print(prime_1, "is composite!")
        
    primeness = isPrime(int(prime_2))
    if primeness:
        print(prime_2, "is prime!")
    else:
        print(prime_2, "is composite!")
    
if __name__ == "__main__":
    print("This program will test two number and determine if they are prime.")
    print("If a float is entered, it will be truncated to a string.")
    check_prime()
    
    