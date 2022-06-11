import requests
import json
import datetime

def main():
    time = datetime.datetime.now().isoformat()

    transaction = {
        "time": time,
        "sender": "C-san",
        "receiver": "D-san",
        "amount": 222,
        "description": "Project YYY Expences",
        "signature": "signature_sample"
    }

    url = "https://yyyyyy.deta.dev/transaction_pool/" 
    res = requests.post(url, json.dumps(transaction))
    print(res.json())

if __name__ == "__main__":
    main()