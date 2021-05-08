
import requests
import json
from pprint import pprint


API = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&price_change_percentage=1h&per_page=250"
results = []


def request():
    page = 1
    try:
        while True: 
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

def sort_results(data):
    key = "price_change_percentage_1h_in_currency"
    results = []
    for item in data:
        if item[key]:
            results.append(item)
        
    sorted_list = sorted(results, key=lambda k: k[key], reverse=True)

    return sorted_list

def save_results(results):
    with open('results.json', 'w+') as f_obj:
        json.dump(results, f_obj)


if __name__ == "__main__":
    results = request()

    sorted_res = sort_results(results)
    save_results(sorted_res[:10])

    name = "id"
    key = "price_change_percentage_1h_in_currency"

    for item in sorted_res[:10]:
        print("Printing Top 10 risers in 1h...")
        print(f"{item['name']} has increased to {item[key]}% in the past 1hour.")