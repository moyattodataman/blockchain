from ecdsa import SigningKey
from ecdsa import SECP256k1

def main():
    secret_key = SigningKey.generate(curve=SECP256k1)
    public_key = secret_key.verifying_key
    secret_key_str = secret_key.to_string().hex()
    public_key_str = public_key.to_string().hex()
    key = {"secret_key_str": secret_key_str, "public_key_str": public_key_str}
    print(key)

if __name__ == "__main__":
    main()