import json
from datetime import datetime

import requests as requests

from telegram import telegram_bot_sendtext
from thresholds import sell_threshold


class execute_order:

    def __init__(self):
        with open("results.json") as results, open("orders.json") as orders:
            self.coins = json.load(results)
            self.orders = json.load(orders)
            self.iter = iter(self.coins)

    def is_coin_already_purchased(self, coin):
        try:
            return coin['name'] in str(self.orders)
        except Exception as e:
            print(e)

    def buy_coin(self):
        coin = next(self.iter, None)
        if not coin: return None
        if self.is_coin_already_purchased(coin):
            print(f"{coin['name']} already purchased")
            return 0

        obj = {
            "Name": coin['name'],
            "id": coin['id'],
            "price": coin["current_price"],
            "date": str(datetime.utcnow()),
            "1hr_price_change_at_purchase": coin['price_change_percentage_1h_in_currency'],
            "ath_change_percentage_at_purchase": coin['ath_change_percentage'],
            "status": "executed"
        }
        self.orders.append(obj)
        print(f"purchasing {coin['name']}")
        with open('orders.json', 'w+') as f_obj:
            json.dump(self.orders, f_obj)

        return 1

    def is_coin_over_48_hours_old(self, coin):
        formatted_date = datetime.strptime(coin['date'], "%Y-%m-%d %H:%M:%S.%f")
        difference = (datetime.utcnow() - formatted_date).total_seconds()
        two_days_in_seconds = 172800
        print(f"{coin['Name']} {difference} seconds elapsed since purchased")
        return difference >= two_days_in_seconds

    def is_equal_or_lower_than_initial_cost_or_has_reached_threshold(self, coin):
        coin_api = "https://api.coingecko.com/api/v3/coins/%s" % coin["id"]
        req = requests.get(coin_api)
        resp = req.json()
        if not resp:
            return True

        current_price = resp['market_data']['current_price']['usd']

        price_difference = current_price - coin['price']
        percentage = price_difference / coin['price'] * 100
        print(f" {coin['Name']} percentage is {percentage} and current price is {current_price} and paid price is {coin['price']}")
        return coin['price'] >= resp['market_data']['current_price']['usd'] or percentage >= sell_threshold


    def sell_coins(self):
        coin_api = "https://api.coingecko.com/api/v3/coins/%s"
        for coin in self.orders:
            time_limit_exceeded = self.is_coin_over_48_hours_old(coin)
            price_dropped = self.is_equal_or_lower_than_initial_cost_or_has_reached_threshold(coin)

            if time_limit_exceeded or price_dropped:
                print("time to sell")
            else:
                print("not time to sell")


if __name__ == "__main__":
    a = execute_order()
    a.buy_coin()
