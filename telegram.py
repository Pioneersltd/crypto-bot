import requests
import json

def telegram_bot_sendtext(bot_message):
    
    bot_token = '1866321485:AAGUYPjFZFHNdMII-tMAoG5xPej1jBK_b1M'
    bot_chatID = '1760050070'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
    

# TODO: Mo to loop through results and send 5 tokens to chatg

with open ("orders.json") as orders:
    orders = json.load(orders)
    telegram_bot_sendtext(str(orders))
