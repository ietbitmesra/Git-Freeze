import time,json
import smtplib
import requests
from datetime import datetime,timedelta
from api import Api
dateIndex=datetime.now()
with open("user_config.json","r") as f:
    conf=json.load(f)
    if(conf["sender_email"]=="" or conf["sender_password"]=="" or len(conf["receiver_email"])==0):
        print("Please Make sure to Enter Sender_Email, Receiver_Email and Sender_Password for Gmail before continuing")
        exit(0)
def keeptrack():
    with open("data.json","r") as f:
        obj=json.load(f)
    #print(obj)
    for mobile in obj:
        name=mobile['name']
        oldPrice=mobile['Best Price']
        newPrice=get_current_price(mobile['Code'])
        print(oldPrice,newPrice)
        if(newPrice<oldPrice):
            message=f"Best Price of {name} has changed from {oldPrice} to {newPrice} at {time.ctime(time.time())}"
            sendEmail(message)
            telegram_alert(message)
            with open("logs.txt","w") as f:
                print(message,file=f)
def get_current_price(mob):
    x=Api().get_data(mob)
    return Api().name_data(x,mob)['Best Price']
def sendEmail(msg):
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(conf["sender_email"], conf["sender_password"])
        list=conf["receiver_email"]
        message = "Subject:Price Updates\n\n"+msg
        print(f"Message is {message}")
        for lines in list:
            s.sendmail(conf['sender_email'], lines, message)
        s.quit()
    except:
        print("Email Credentials not avilable or they are not valid please allow less secure apps from your gmail if your credentials are correct")
def telegram_alert(bot_message):
    try:
        bot_token=conf['telegram_bot_token']
        bot_chatID=conf['telegram_chatID']
        url="https://api.telegram.org/bot"+bot_token+'/sendMessage?chat_id'+bot_chatID+'&parse_mode=Markdown&text='+bot_message
    except:
        print("Telegram Credentials not avilable or they are not valid")
    res=requests.get(url)
def checkserver():
    msg="Daily Server Check"
    #telegram_alert(msg)
    sendEmail(msg)
if __name__ == "__main__":
    updation_time=60*60*3 #3 hour updates
    c=0
    while(1):
        c=c+1
        keeptrack()
        if(c%8==1):
            checkserver()    #1day updates
        time.sleep(updation_time)
