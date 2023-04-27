import random
import hashlib
import math


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

        for iter in range(10):
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
    def generateLargePrime(cls, x):
        # k = int(math.log2(x))
        k = x
        print(k)
        num = random.randrange(2**k, 2**(k+1))
        while(not cls.miller_rabin(num)):
            print(num)
            num = random.randrange(k, k*2)
            # num += 1
        return num
    
    @classmethod
    def isPrime(cls, num):

        if (num < 2):
            return False 

        lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

        if num in lowPrimes:
            return True

        for prime in lowPrimes:
            if (num % prime == 0):
                return False

        return cls.miller_rabin(num)


class ZKP_Para:
    """Generates global parameters p, g, q for ZKP system for Schnorr's protocol
    """
    def __init__(self) -> None:
        self.p, self.q, self.g = self.generatepqg()
    
    def generatepqg(self):
        k = random.randrange(2**10, 2**11)
        q = Prime.generateLargePrime(6)
        p = (k*q)+1
        while not Prime.isPrime(p):
            k = random.randrange(2**10, 2**11)
            q = Prime.generateLargePrime(6)
            p = (k*q)+1
        
        t = random.randrange(1, p-1)
        g = pow(t, int((p-1)//q), p)
        return p, q, g
    
class ZKP_Signature:
    """Generates and Stores signature for ZKP system for Schnorr's protocol
    """
    def __init__(self, zkp_para, secretInfo, proverID) -> None:
        secretInfo = int(hashlib.sha256(preHash.encode()).hexdigest(), 16)
        self.apu = pow(zkp_para.g, secretInfo, zkp_para.p)
        
        v = random.randrange(0, zkp_para.q)
        self.vpu = pow(zkp_para.g, v, zkp_para.p)
        
        preHash = "{}{}{}{}".format(zkp_para.g, self.vpu, self.apu, proverID)
        self.challenge = int(hashlib.sha256(preHash.encode()).hexdigest(), 16)
        
        self.r = (v - secretInfo*self.challenge) % zkp_para.q
            


class ZK_Verifier:
    """Class to store proof/verify procedure for ZKP system for Schnorr's protocol
    """
    def __init__(self, zkp_para, zkp_signature) -> None:
        self.zkp_para = zkp_para
        self.zkp_signature = zkp_signature

    def verify(self):
        temp1 = pow(self.zkp_signature.apu, self.zkp_para.q, self.zkp_para.p)
        temp_vpu = (pow(self.zkp_para.g, self.zkp_signature.r, self.zkp_para.p)
                    * pow(self.zkp_signature.apu, self.zkp_signature.challenge, self.zkp_para.p)) % self.zkp_para.p
        
        if ((self.zkp_signature.apu > 1 and self.zkp_signature.apu < self.zkp_para.p-1) 
            and temp1 == 1 
            and temp_vpu == self.zkp_signature.vpu):
            return True
        
        return False
        
        
       
# z = ZKP("102830")

# print(generateLargePrime(2**10))