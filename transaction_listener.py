import requests
import time
from solathon import PublicKey

# URL для подключения к Solana RPC
SOLANA_RPC_URL = 'https://api.mainnet-beta.solana.com'

# Публичный ключ кошелька, который вы хотите отслеживать
PUBLIC_KEY = 'PUBLIC_KEY'
pubkey = PublicKey(PUBLIC_KEY)

# Хранилище для уже просмотренных подписей транзакций
seen_signatures = set()


def get_signatures_for_address(pubkey, before=None, limit=1):
    headers = {'Content-Type': 'application/json'}
    params = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [str(pubkey), {"limit": limit, "before": before}]
    }
    try:
        response = requests.post(SOLANA_RPC_URL, headers=headers, json=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {}
    except Exception as err:
        print(f"Other error occurred: {err}")
        return {}


def get_transaction_info(tx_signature):
    headers = {'Content-Type': 'application/json'}
    params = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [tx_signature, {"encoding": "jsonParsed"}]
    }
    try:
        response = requests.post(SOLANA_RPC_URL, headers=headers, json=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {}
    except Exception as err:
        print(f"Other error occurred: {err}")
        return {}


def fetch_new_transaction(pubkey):
    while True:
        try:
            # Запрос на получение одной новой транзакции
            response = get_signatures_for_address(pubkey)
            result = response.get('result', [])

            if result:
                signature_info = result[0]
                signature = signature_info['signature']

                if signature not in seen_signatures:
                    seen_signatures.add(signature)
                    tx_info = get_transaction_info(signature)

                    if 'error' in tx_info:
                        print(f"Error fetching transaction info: {tx_info['error']}")
                    else:
                        try:
                            # Получение данных о транзакции
                            transaction = tx_info['result']['transaction']
                            print(transaction)

                        except KeyError as e:
                            print(f"Key error while parsing transaction info: {e}")

            else:
                print("No new signatures. Waiting before retrying...")

            # Ожидание перед следующим запросом
            time.sleep(5)

        except Exception as e:
            print(f"Error fetching transactions: {e}")
            time.sleep(5)


if __name__ == "__main__":
    fetch_new_transaction(pubkey)