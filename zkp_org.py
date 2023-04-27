import random
import hashlib

class ZKP_Para:
    """Generates global/ pubic parameters for ZKP using discrete logarithm problem
    """
    def __init__(self) -> None:
        self.p = Prime.generateLargePrime(32)
        self.g = Prime.find_primitive_root(self.p)
        # self.p = 997
        # self.g = 5

class ZKP_Signature:
    """Generates and stores signature for ZKP using discrete logarithm problem
    """
    def __init__(self, zkp_para, secretInfo) -> None:
        """Initialises signature for secretInfo based on zkp_para

        Args:
            zkp_para (ZKP_Para): Instance of ZKP_Para agreed between prover and verifier
            secretInfo (str or int): secret information to be proved to verifier
        """
        secretInfo = int(hashlib.sha256(secretInfo.encode()).hexdigest(), 16)
        self.y = pow(zkp_para.g, secretInfo, zkp_para.p)
        
        self.r = random.randrange(0, zkp_para.p)
        self.h = pow(zkp_para.g, self.r, zkp_para.p)
        
        preHash = "{}{}{}".format(zkp_para.g, self.y, self.h)
        self.challenge = int(hashlib.sha256(preHash.encode()).hexdigest(), 16)
        
        self.sig = (self.r + (self.challenge * secretInfo)) % (zkp_para.p-1)

class ZKP_Verifier:
    """Class to store proof/verify procedure for ZKP using discrete logarithm problem
    """
    def __init__(self, zkp_para, zkp_sig) -> None:
        self.zkp_para = zkp_para
        self.zkp_sig = zkp_sig
        
    def verify(self):
        """Verifies the signature of the user using ZKP

        y=g**x mod (p)   s =(r+b*x) mod(p-1)    h =g**r mod(p)
        g**s mod(p) ?= hy**b mod(p)

        Returns:
            bool: Returns True if signature is verified, otherwise False
        """
        preHash = "{}{}{}".format(self.zkp_para.g, self.zkp_sig.y, self.zkp_sig.h)
        ver_challenge = int(hashlib.sha256(preHash.encode()).hexdigest(), 16)
        
        temp1 = pow(self.zkp_para.g, self.zkp_sig.sig, self.zkp_para.p)
        temp2 = (self.zkp_sig.h * pow(self.zkp_sig.y, ver_challenge, self.zkp_para.p)) % self.zkp_para.p
        
        return (temp1 == temp2) and (ver_challenge == self.zkp_sig.challenge)


class Prime:
    """Class to generate large prime numbers and other utility functions
    """
    @classmethod
    def miller_rabin(cls, num):
        """Checks Primality using Miller Rabin Primality Test

        Args:
            num (int): Checks Primality of this number

        Returns:
            bool: False if number is composite, True otherwise
        """
        s = num-1
        t = 0

        while s % 2 == 0:
            s = s//2
            t += 1

        for iter in range(40):
            a = random.randrange(2, num-1)
            v = pow(a, s, num)
            if v != 1:
                i = 0
                while v != (num-1):
                    if i == t-1:
                        return False
                    else:
                        i += 1
                        v = (pow(v, 2, num))
        return True

    @classmethod
    def generateLargePrime(cls, k):
        """Generates prime of length k bits     

        Args:
            k (int): bit length of the prime number to be generated

        Returns:
            int: Returns the prime number of length k bits
        """
        num = random.randrange(2**k, 2**(k+1))
        while(not cls.isPrime(num)):
            # print(num)
            # num = random.randrange(2**k, 2**(k+1))
            num += 1
        return num
    
    @classmethod
    def isPrime(cls, num):
        """Checks if number is divisible by lower Primes

        Args:
            num (int): Primality of the number is checked

        Returns:
            int: Returns true if the number is divisible by lowerPrimes else MillerRabin is called
        """

        if (num < 2):
            return False 

        lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

        if num in lowPrimes:
            return True

        for prime in lowPrimes:
            if (num % prime == 0):
                return False

        return cls.miller_rabin(num)

    @classmethod
    def find_primitive_root(cls,p):
        """Returns smallest primitive root of prime number p using Euler's Totient Theorem
        
        This is also generator for finite field Zp

        Args:
            p (int): smallest primitive root of this number is returned

        Returns:
            int: Returns smallest primitive root of prime number p
        """
        phi = p - 1
        factors = cls.factorize(phi)
        for g in range(2, p):
            if all(pow(g, phi // f, p) != 1 for f in factors):
                return g


    def factorize(n):
        """Factorizes n into its prime factors

        Args:
            n (int): Prime factors of the number are returned

        Returns:
            list[int]: Returns list of prime factors of n 
        """
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

    
z = ZKP_Para()
print(z.g,z.p)
        