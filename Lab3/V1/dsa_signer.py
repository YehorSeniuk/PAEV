from random import randrange, randint
from hashlib import sha1
from gmpy2 import xmpz, to_binary, invert, is_prime



class DSASigner:

    @staticmethod
    def sign(m, params, x):
        if not DSASigner.validate_params(params):
            raise Exception("Invalid params")
        while True:
            k = randrange(2, params.q)
            r = pow(params.g, k, params.p) % params.q
            m = int(sha1(m).hexdigest(), 16)
            try:
                s = (invert(k, params.q) * (m + x * r)) % params.q
                return DSASignature(r, s)
            except ZeroDivisionError:
                pass

    @staticmethod
    def generate_p_q(L, N):
        g = N
        n = (L - 1) // g
        b = (L - 1) % g
        while True:
            while True:
                s = xmpz(randrange(1, 2 ** (g)))
                a = sha1(to_binary(s)).hexdigest()
                zz = xmpz((s + 1) % (2 ** g))
                z = sha1(to_binary(zz)).hexdigest()
                U = int(a, 16) ^ int(z, 16)
                mask = 2 ** (N - 1) + 1
                q = U | mask
                if is_prime(q, 20):
                    break

            i = 0
            j = 2
            while i < 4096:
                V = []
                for k in range(n + 1):
                    arg = xmpz((s + j + k) % (2 ** g))
                    zzv = sha1(to_binary(arg)).hexdigest()
                    V.append(int(zzv, 16))
                W = 0
                for qq in range(0, n):
                    W += V[qq] * 2 ** (160 * qq)
                W += (V[n] % 2 ** b) * 2 ** (160 * n)
                X = W + 2 ** (L - 1)
                c = X % (2 * q)
                p = X - c + 1  # p = X - (c - 1)
                if p >= 2 ** (L - 1):
                    if is_prime(p, 10):
                        return p, q
                i += 1
                j += n + 1
    @staticmethod
    def generate_g(p, q):
        while True:
            h = randrange(2, p - 1)
            exp = xmpz((p - 1) // q)
            g = pow(h, exp, p)
            if g > 1:
                break
        return g
    @staticmethod
    def generate_params_and_keys():
        params = DSASigner.generate_params()
        x = randrange(2, params.q)  # x < q
        y = pow(params.g, x, params.p)
        return params, DSAPrivateKey(x), DSAPublicKey(y)

    @staticmethod
    def generate_params():
        L = randint(1024, 2048)
        N = randint(160, 320)
        p, q = DSASigner.generate_p_q(L, N)
        g = DSASigner.generate_g(p, q)
        return DSAParams(p, q, g)

    @staticmethod
    def validate_params(params):
        if is_prime(params.p) and is_prime(params.q):
            return True
        if pow(params.g, params.q, params.p) == 1 and params.g > 1 and (params.p - 1) % params.q:
            return True
        return False

    @staticmethod
    def validate_sign(r, s, q):
        if 0 > r > q:
            return False
        if 0 > s > q:
            return False
        return True

    @staticmethod
    def verify(M, signature, params, y):
        if not DSASigner.validate_params(params):
            raise Exception("Invalid params")
        if not DSASigner.validate_sign(signature.r, signature.s, params.q):
            return False
        try:
            w = invert(signature.s, params.q)
        except ZeroDivisionError:
            return False
        m = int(sha1(M).hexdigest(), 16)
        u1 = (m * w) % params.q
        u2 = (signature.r * w) % params.q
        v = (pow(params.g, u1, params.p) * pow(y, u2, params.p)) % params.p % params.q
        if v == signature.r:
            return True
        return False

class DSASignature:

    def __init__(self, r, s):
        self.__r = r
        self.__s = s

    @property
    def s(self):
        return self.__s

    @property
    def r(self):
        return self.__r

class DSAPublicKey:

    def __init__(self, y):
        self.__y = y

    @property
    def y(self):
        return self.__y

    def __add__(self, other):
        return self.y + other

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        return self.y * other

    def __rmul__(self, other):
        return self * other

    def __mod__(self, other):
        return self.y % other

    def __rmod__(self, other):
        return self * other

    def __pow__(self, power, modulo=None):
        return pow(self.y, power, modulo)

    def __repr__(self):
        return f'DSAPublicKey({self.y})'

class DSAPrivateKey:

    def __init__(self, x: int):
        self.__x = x

    @property
    def x(self):
        return self.__x

    def __add__(self, other):
        return self.x + other

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        return self.x * other

    def __rmul__(self, other):
        return self * other

    def __mod__(self, other):
        return self.x % other

    def __rmod__(self, other):
        return self * other

    def __pow__(self, power, modulo=None):
        return pow(self.x, power, modulo)

    def __repr__(self):
        return f'DSAPrivateKey({self.x})'

class DSAParams:

    def __init__(self, p, q, g):
        self.__p = p
        self.__q = q
        self.__g = g

    @property
    def p(self):
        return self.__p

    @property
    def q(self):
        return self.__q

    @property
    def g(self):
        return self.__g

