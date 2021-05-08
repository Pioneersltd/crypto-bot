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
            "date": datetime.utcnow().isoformat(),
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

    def is_coin_over_48_hours_old(self, coin):
        difference = (datetime.utcnow() - coin['date']).total_seconds()
        two_days_in_seconds = 172800
        return difference >= two_days_in_seconds
    def sell_coins(self):
        coin_api = "https://api.coingecko.com/api/v3/coins/%s"
        for coin in self.orders:
            if self.is_coin_over_48_hours_old(coin) or self.has_coin_reached_threshold(coin) or self.is_equal_or_lower_than_initial_cost(coin):



if __name__ == "__main__":
    a = execute_order()
    a.buy_coin()
