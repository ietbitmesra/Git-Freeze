import time
import sys
import json
import smtplib
import requests
from termcolor import cprint
from api import Api
with open("user_config.json", "r") as f:
    CONF = json.load(f)
    if (CONF["sender_email"] == "" or CONF["sender_password"] == "" or
            len(CONF["receiver_email"]) == 0):
        cprint(("Please Make sure to Enter Sender_Email, Receiver_Email"
                "and Sender_Password for Gmail before continuing"), 'red')
        sys.exit()


def keeptrack():
    with open("data.json", "r") as f:
        obj = json.load(f)
    # print(obj)
    for mobile in obj:
        name = mobile['name']
        oldPrice = mobile['Best Price']
        newPrice = get_current_price(mobile['Code'])
        print(oldPrice, newPrice)
        if (newPrice < oldPrice):
            message = (f"Best Price of {name} has changed from{oldPrice}"
                       f"to {newPrice} at {time.ctime(time.time())}")
            send_email(message)
            telegram_alert(message)
            with open("logs.txt", "w") as f:
                print(message, file=f)


def get_current_price(mob):
    x = Api().get_data(mob)
    return Api().name_data(x, mob)['Best Price']


def send_email(msg):
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(CONF["sender_email"], CONF["sender_password"])
        myList = CONF["receiver_email"]
        message = "Subject:Price Updates\n\n"+msg
        print(f"message is {message}")
        for lines in myList:
            s.sendmail(CONF['sender_email'], lines, message)
        s.quit()
    except Exception as ex:
        cprint(("Email Credentials not avilable or they are not valid "
                "pleaseallow less secure apps from your "
                " gmail if your credentials are correct"), 'red')
        sys.exit()


def telegram_alert(BotMessage):
    try:
        botToken = CONF['telegram_bot_token']
        botChatId = CONF['telegram_chatID']
        url = ('https://api.telegram.org/bot' + botToken + '/sendMessage'
               '?chat_id'+botChatId+'&parse_mode=Markdown&text='+BotMessage)
    except Exception as ex:
        cprint(f"While logging in Telegram {ex} occured", 'red')
    requests.get(url)


def checkserver():
    msg = "Daily Server Check"
    # telegram_alert(msg)
    send_email(msg)


if __name__ == "__main__":
    updationTime = 60 * 60 * 3  # 3 hour updates
    COUNT = 0
    while(1):
        COUNT = COUNT + 1
        keeptrack()
        if (COUNT % 8 == 1):
            checkserver()    # 1day updates
        time.sleep(updationTime)
