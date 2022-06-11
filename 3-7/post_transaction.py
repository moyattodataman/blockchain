import requests
import json
import datetime
from ecdsa import SigningKey
from ecdsa import SECP256k1
import binascii

def main(secret_key_str, sender_pub_key_str, receiver_pub_key_str, amount, description, url):
    time = datetime.datetime.now().isoformat()
    
    transaction_unsigned = {
        "time": time,
        "sender": sender_pub_key_str,
        "receiver": receiver_pub_key_str,
        "amount": amount,
        "description": description
    }

    secret_key = SigningKey.from_string(binascii.unhexlify(secret_key_str), curve=SECP256k1)
    signature_str = signature(transaction_unsigned, secret_key)

    transaction = {
        "time": time,
        "sender": sender_pub_key_str,
        "receiver": receiver_pub_key_str,
        "amount": amount,
        "description": description, 
        "signature": signature_str
    }

    res = requests.post(url, json.dumps(transaction))
    print(res.json())

def signature(transaction_unsigned, secret_key):
    transaction_json = json.dumps(transaction_unsigned)
    transaction_bytes = bytes(transaction_json, encoding = "utf-8")
    signature = secret_key.sign(transaction_bytes)
    signature_str = signature.hex()
    return signature_str

if __name__ == "__main__":
    # url = "http://127.0.0.1:8002/transaction_pool/" 
    # ap1_1 
    # url = "https://dgnsub.deta.dev/transaction_pool/"
    # api_2
    # url = "https://j7bizt.deta.dev/transaction_pool/"
    # api_3
    url = "https://1ydi3z.deta.dev/transaction_pool/"
    # Bさんの秘密鍵
    secret_key_str = "65067954df7ee9cbc94c9d60907c0bc36e2a9a33541b032777f77550fc172308"
    # Bさんの公開鍵
    sender_pub_key_str = "c5e0cb5f5d91475682c8ec2669077484eab9e2d41e2dd2cdb82fe2ce09e042c59c4a3d0c61d2e93697237a3957d68000fb0d10fc977516492e776fdd01a6d362"
    # Aさんの公開鍵
    receiver_pub_key_str = "cebcf84ae3126e82f46f34b0419ecad67decac23e8d0b5cdcee9397b3235a402a519146b29e8e247a5cd51a3ddfe9efdeee68cf406a8fa39e67bc0193d757959"
    amount = 222
    description = "Fee from B-san to A-san"
    
    main(secret_key_str, sender_pub_key_str, receiver_pub_key_str, amount, description, url)
