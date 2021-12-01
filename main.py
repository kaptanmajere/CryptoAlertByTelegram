import requests
import pandas as pd
import time
import telepot
import os
from dotenv import load_dotenv


def get_crypto_price(symbol):
    api_key = 'pk_4d7690d345cb415f807ebb84a43ee78d'
    api_url = f'https://cloud.iexapis.com/stable/crypto/{symbol}/price?token={api_key}'
    raw = requests.get(api_url).json()
    price = raw['price']
    return float(price)


def calculate_try_change():
    btc_try = get_crypto_price('btctry')
    eth_try = get_crypto_price('ethtry')
    load_dotenv()

    eth_amount = float(os.getenv('ETH_AMOUNT'))
    btc_amount = float(os.getenv('BTC_AMOUNT'))
    interval = int(os.getenv('INTERVAL'))


    total_amount_try_first = eth_try * eth_amount + btc_try * btc_amount

    while True:
        btc_try = get_crypto_price('btctry')
        eth_try = get_crypto_price('ethtry')
        total_amount_try = eth_try * eth_amount + btc_try * btc_amount
        print(f'TRY: {total_amount_try}')
        print(f'TRY F: {total_amount_try_first}')

        if total_amount_try > total_amount_try_first:
            print(f'You have gained {total_amount_try - total_amount_try_first}')
            send_message_by_telegram(
                f'You have gained {format(total_amount_try - total_amount_try_first, ".2f")} \nYou had {format(total_amount_try_first, ".2f")} before. \nNow you have {format(total_amount_try, ".2f")}')
        elif total_amount_try < total_amount_try_first:
            print(f'You have lost {total_amount_try_first - total_amount_try}')
            send_message_by_telegram(
                f'You have lost {format(total_amount_try_first - total_amount_try, ".2f")} \nYou had {format(total_amount_try, ".2f")} before. \nNow you have {format(total_amount_try, ".2f")}')
        else:
            send_message_by_telegram("No change.")
            print("No change.")
        total_amount_try_first = total_amount_try

        time.sleep(interval)


def send_message_by_telegram(message):
    token = '2144092717:AAFnvnmP4IT4zANnzz6Df355PHGOH_ijf3I'  # telegram token
    receiver_id = 709215741  # https://api.telegram.org/bot<TOKEN>/getUpdates

    bot = telepot.Bot(token)

    bot.sendMessage(receiver_id, message)


if __name__ == '__main__':
    calculate_try_change()
