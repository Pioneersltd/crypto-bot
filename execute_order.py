import json
from datetime import datetime


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
            "price": coin["current_price"],
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "1hr_price_change_at_purchase": coin['price_change_percentage_1h_in_currency'],
            "ath_change_percentage_at_purchase": coin['ath_change_percentage'],
            "status": "executed"
        }
        self.orders.append(obj)
        print(f"purchasing {coin['name']}")
        print(self.orders)
        with open('orders.json', 'w+') as f_obj:
            json.dump(self.orders, f_obj)

        return 1


if __name__ == "__main__":
    a = execute_order()
    a.buy_coin()
