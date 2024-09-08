import random

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime():
    while True:
        num = random.randint(100, 200)
        if is_prime(num):
            return num

def generate_rsa_keys():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = random.randint(2, phi_n - 1)
    while gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)

    d = modinv(e, phi_n)

    return (e, n), (d, n)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def rsa_encrypt(message, pub_key):
    e, n = pub_key
    return [pow(ord(char), e, n) for char in message]

def rsa_decrypt(ciphertext, priv_key):
    d, n = priv_key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])

def xor_cipher(message, key):
    return ''.join(chr(ord(c) ^ key) for c in message)

def vote(voter, candidate, priv_key_cvk, pub_key_cvk, registered_voters, voted):
    if voter not in registered_voters:
        raise KeyError("Voter not registered.")
    if voter in voted:
        raise ValueError("Voter has already voted.")

    key = random.randint(1, 255)
    encrypted_vote = xor_cipher(candidate, key)
    signature = rsa_encrypt(encrypted_vote, priv_key_cvk)
    voted.add(voter)
    return encrypted_vote, signature, key

def count_votes(votes, priv_key_cvk, pub_key_cvk, candidates):
    results = {candidate: 0 for candidate in candidates}

    for vote_data in votes:
        encrypted_vote, signature, key = vote_data
        decrypted_vote = xor_cipher(encrypted_vote, key)
        decrypted_signature = rsa_decrypt(signature, pub_key_cvk)
        if decrypted_signature == encrypted_vote:
            results[decrypted_vote] += 1

    return results
