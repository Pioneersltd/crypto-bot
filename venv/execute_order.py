import json
import os



class execute_order:

    def __init__(self):
        print(1)
        with open ("../results.json" ) as results,  open("../orders.json") as orders:
            self.coins = json.load(results)
            self.orders = json.load(orders)

    def is_coin_already_purchased(self, coin):
        try:
            return coin in str(self.coins)
        except Exception as e:
            print(e)

    def buy_coin(self, coin):
        if self.is_coin_already_purchased():
            print(f"{coin} already purchased")
            return
