import random
from sympy import isprime, gcd, mod_inverse

def generate_prime_candidate(length):
    """Generate an odd prime candidate."""
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1  # Ensure it's odd and the right bit length
    return p

def generate_prime_number(length):
    """Generate a prime number of the specified bit length."""
    p = 4  # Not prime
    while not isprime(p):
        p = generate_prime_candidate(length)
    return p

def generate_keypair(bits):
    """Generate a public and private key pair."""
    p = generate_prime_number(bits)
    q = generate_prime_number(bits)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e
    e = 65537  # Common choice for e
    # Calculate d
    d = mod_inverse(e, phi)

    return ((e, n), (d, n))  # Public and private keys

def sign(private_key, message):
    """Sign the message with the private key."""
    d, n = private_key
    hash_value = sum(ord(char) for char in message)  # Simple hash function
    signature = pow(hash_value, d, n)
    return signature

def verify(public_key, message, signature):
    """Verify the signature using the public key."""
    e, n = public_key
    hash_value = sum(ord(char) for char in message)  # Same hash function
    hash_from_signature = pow(signature, e, n)
    return hash_value == hash_from_signature

def main():
    bits = 8  # You can increase this for stronger encryption
    public_key, private_key = generate_keypair(bits)

    message = "Hello"
    print(f"Original Message: {message}")

    # Sign the message
    signature = sign(private_key, message)
    print(f"Signature: {signature}")

    # Verify the signature
    is_valid = verify(public_key, message, signature)
    print(f"Signature Valid: {is_valid}")

if __name__ == "__main__":
    main()
