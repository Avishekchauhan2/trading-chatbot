# trading_bot_project/bot.py
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
import argparse

api_key='f414a4a210251a39bf8e030990ebf43bd23b45ed90449e60729c363f694cbc53'
secret='5e09fee50e2c2b5d07c99bea8e156f99fec12630e97038d6bc18a4434d1cec1b'

class BasicBot:

    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
        logging.basicConfig(filename='trading_bot.log', level=logging.INFO,
                            format='%(asctime)s %(levelname)s:%(message)s')

    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )
            logging.info(f"Market Order placed: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"Market Order failed: {e}")
            return {"error": str(e)}

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce="GTC",
                quantity=quantity,
                price=price
            )
            logging.info(f"Limit Order placed: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"Limit Order failed: {e}")
            return {"error": str(e)}

# trading_bot_project/cli.py
# import argparse
# from bot import BasicBot

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crypto Trading Bot CLI')
    parser.add_argument('--api_key', required=True, help='Binance API Key')
    parser.add_argument('--api_secret', required=True, help='Binance API Secret')
    parser.add_argument('--symbol', required=True, help='Trading pair symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', required=True, choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('--type', required=True, choices=['MARKET', 'LIMIT'], help='Order type')
    parser.add_argument('--quantity', type=float, required=True, help='Order quantity')
    parser.add_argument('--price', type=float, help='Limit order price')

    args = parser.parse_args()
    # bot = BasicBot(args.api_key, args.api_secret)
    bot = BasicBot(api_key, secret)

    if args.type == 'MARKET':
        response = bot.place_market_order(args.symbol, args.side, args.quantity)
    elif args.type == 'LIMIT':
        if args.price is None:
            print("Limit price required for LIMIT order")
            exit(1)
        response = bot.place_limit_order(args.symbol, args.side, args.quantity, args.price)

    print(response)

# trading_bot_project/requirements.txt
# python-binance

# trading_bot_project/README.md
# Simplified Crypto Trading Bot

## Features
# - Place MARKET and LIMIT orders
# - Binance Futures Testnet compatible
# - Command-line interface
# - Logs all activity to `trading_bot.log`

## Setup
# 1. Clone the repo
# 2. Install dependencies:
# ```bash
# pip install -r requirements.txt
# ```

# 3. Run CLI:
# ```bash
# python cli.py --api_key YOUR_KEY --api_secret YOUR_SECRET --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
# ```
