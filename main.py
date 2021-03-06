from execute_order import execute_order
from fetch_crypto import request, sort_results, save_results, log_results

if __name__ == "__main__":

    results = request()
    key_price_change = "price_change_percentage_1h_in_currency"
    key_ath_percentage = "ath_change_percentage"
    key_market_cap = "market_cap"
    key_current_price = "current_price"
    sorted_res = sort_results(results, key_price_change, key_ath_percentage, key_market_cap)
    save_results(sorted_res[:10])
    log_results()

    #Buying coin
    buyer = execute_order()
    counter = len(buyer.orders)
    while (counter < 5):
        print("here")
        status = buyer.buy_coin()
        if status or status == 0:
            counter += status
            continue
        else:
            print("breaking")
            break

    # buyer.sell_coins()
