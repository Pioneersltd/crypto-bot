import requests
import json
from pprint import pprint

from thresholds import lowest_threshold, highest_threshold, unwanted_market_cap

API = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&price_change_percentage=1h&per_page=250"
results = []


def request():
    page = 1
    try:
        while True:
            print(f"Checking page {page}...")
            URL = f"{API}&page={page}"
            req = requests.get(URL)

            resp = req.json()

            if not resp:
                break

            results.extend(resp)
            page += 1

            if req.status_code != 200:
                print(f"ERROR: unable to retrieve response due to status code being {req.status_code}")
    except Exception as e:
        print("ERROR: unable to fetch crypto prices", e)

    return results


def sort_results(data, key1, key2, key3):
    print("sorting results")
    results = []

    for item in data:
        if item[key1] and item[key2] and item[key3]:
            if lowest_threshold < item[key1] < highest_threshold and key3 != unwanted_market_cap:
                results.append(item)

    sorted_list = sorted(results, key=lambda k: k[key1], reverse=False)

    return sorted_list


def save_results(results):
    with open('results.json', 'w+') as f_obj:
        json.dump(results, f_obj)


def log_results():
    key_price_change = "price_change_percentage_1h_in_currency"
    key_ath_percentage = "ath_change_percentage"
    key_market_cap = "market_cap"
    key_current_price = "current_price"
    sorted_res = sort_results(results, key_price_change, key_ath_percentage, key_market_cap)

    for count, item in enumerate(sorted_res[:10]):
        print(f"-----------Result {count}--------")
        print(
            f"{item['name']} increased {item[key_price_change]}% in last 1hr...ATH = {item[key_ath_percentage]}...MarketCap = {item[key_market_cap]}")
        print(f"Executing order at {item[key_current_price]}")