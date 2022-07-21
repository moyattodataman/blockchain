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
        "description": "YYY Project Expenses",
        "signature": "signature_sample"
    }

    url = "http://127.0.0.1:8002/transaction_pool/" 
    res = requests.post(url, json.dumps(transaction))
    print(res.json())

if __name__ == "__main__":
    main()