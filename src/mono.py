import monobank
import os


MONO_TOKEN = os.getenv('MONO_TOKEN')
account = os.getenv('MONO_ACCOUNT')

mono = monobank.Client(MONO_TOKEN)


def get_balance():
    balance = ''
    data = mono.get_client_info()['accounts']
    for item in data:
        if item['id'] == account:
            balance = int(item['balance'] / 100)

    return balance
