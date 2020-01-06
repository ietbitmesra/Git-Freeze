import time
import smtplib
import requests
from bs4 import BeautifulSoup

#launch price of devices
iphone_price = 0.0
oneplus_price = 0.0

#set the prices of both the devices
def setPrice():
    iphpage = requests.get("https://www.flipkart.com/search?q=iphone%2011%2064gb&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
    oppage = requests.get("https://www.flipkart.com/search?q=one%20plus%207t%20pro&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
    ipage = BeautifulSoup(iphpage.content, 'html.parser')
    opage = BeautifulSoup(oppage.content, 'html.parser')
    priceo = opage.find("div", {"class": "_1vC4OE _2rQ-NK"}).get_text()
    pricei = ipage.find("div", {"class": "_1vC4OE _2rQ-NK"}).get_text()
    #converting string to float
    conv_iprice = pricei[1:7]
    conv_iprice = float(conv_iprice[0:2] + conv_iprice[3:7])
    conv_oprice = priceo[1:7]
    conv_oprice = float(conv_oprice[0:2] + conv_oprice[3:7])
    #setting the prices
    iphone_price= conv_iprice
    oneplus_price= conv_oprice

def sendMail():
  try:
      s = smtplib.SMTP('smtp.gmail.com', 587)
      s.ehlo()
      # start TLS for security
      s.starttls()

      # Authentication
      s.login("tm132631@gmail.com", "hello@123")

      # message to be sent
      message = "Prices have Changed!"

      # sending the mail  sender's mail    reciever's mail   message
      s.sendmail("tm132631@gmail.com", "tm132631@gmail.com", message)

      # terminating the session
      s.quit()
      print("Email Sent!")
  except:
      print("Failed to send Mail!")

def updateJson():

    # for spec compare table using gadgetsnow website
    result = requests.get("https://www.gadgetsnow.com/compare-mobile-phones/Apple-iPhone-11-vs-OnePlus-7T-Pro")
    # for dynamic prices, requesting prices from flipkart
    iphone_price = requests.get(
        "https://www.flipkart.com/search?q=iphone%2011%2064%20gb&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off")
    oneplus_price = requests.get(
        "https://www.flipkart.com/search?q=oneplus+7t+pro+mobile&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_11_na_na_pr&otracker1=AS_QueryStore_OrganicAutoSuggest_2_11_na_na_pr&as-pos=2&as-type=RECENT&suggestionId=oneplus+7t+pro+mobile%7Cin+Mobiles&requestId=47fd111f-b36e-4c09-ad4d-47e11c391fac&as-searchtext=oneplus%207t%20")

    i_price = BeautifulSoup(iphone_price.content, 'html.parser')
    o_price = BeautifulSoup(oneplus_price.content, 'html.parser')

    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    compare_list = [['Feature', 'Iphone 11', 'OnePlus 7t Pro']]

    # price
    prices_i = i_price.find("div", {"class": "_1vC4OE _2rQ-NK"})
    prices_o = o_price.find("div", {"class": "_1vC4OE _2rQ-NK"})
    price_list = ['Price', prices_i.text, prices_o.text]
    print(price_list)
    compare_list.append(price_list)
    print(compare_list)

    # storage
    table = soup.find("table", {"class": "compare_tbl"})
    table_rows = table.find_all("tr", {"data-nd": "storage"})
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        storage_list = list(filter(None, row))
        storage_list[0] = 'Storage'
        print(storage_list)
        compare_list.append(storage_list)
        print(compare_list)

    # os
    table = soup.find("table", {"class": "compare_tbl"})
    table_rows = table.find_all("tr", {"data-nd": "operating_system"})
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        os_list = list(filter(None, row))
        os_list[0] = 'Operating System'
        print(os_list)
        compare_list.append(os_list)
        print(compare_list)

    # front cam
    table = soup.find("table", {"class": "compare_tbl"})
    table_rows = table.find_all("tr", {"data-nd": "resolution"})
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        ccam_list = list(filter(None, row))
        ccam_list[0] = 'Front Camera'
        print(ccam_list)
        compare_list.append(ccam_list)
        print(compare_list)

    # rear cam
    table = soup.find("table", {"class": "compare_tbl"})
    table_rows = table.find_all("tr", {"data-nd": "rear_camera"})
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        rcam_list = list(filter(None, row))
        rcam_list[0] = 'Rear Camera'
        print(rcam_list)
        compare_list.append(rcam_list)
        print(compare_list)

    # network
    table = soup.find("table", {"class": "compare_tbl"})
    table_rows = table.find_all("tr", {"data-nd": "network_support"})
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        net_list = list(filter(None, row))
        net_list[0] = 'Network Support'
        print(net_list)
        compare_list.append(net_list)
        print(compare_list)

    # wifi
    table = soup.find("table", {"class": "compare_tbl"})
    table_rows = table.find_all("tr", {"data-nd": "wifi"})
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        wifi_list = list(filter(None, row))
        wifi_list[0] = 'Wifi'
        print(wifi_list)
        compare_list.append(wifi_list)
        print(compare_list)

    # import pandas as pd
    import pandas as pd
    # Calling DataFrame constructor on list
    df = pd.DataFrame(compare_list)
    print(df)

    # creating a json file
    with open('data.json', 'w') as f:
        f.write(df.to_json())

print("Creating Json...")
updateJson()

print("Checking Prices...")
setPrice()

def comparePrices():
    #getting the current prices
    iphpage = requests.get("https://www.flipkart.com/search?q=iphone%2011%2064gb&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
    oppage = requests.get("https://www.flipkart.com/search?q=one%20plus%207t%20pro&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
    ipage = BeautifulSoup(iphpage.content, 'html.parser')
    opage = BeautifulSoup(oppage.content, 'html.parser')
    priceo = opage.find("div", {"class": "_1vC4OE _2rQ-NK"}).get_text()
    pricei = ipage.find("div", {"class": "_1vC4OE _2rQ-NK"}).get_text()
    conv_iprice = pricei[1:7]
    conv_iprice = float(conv_iprice[0:2] + conv_iprice[3:7])
    conv_oprice = priceo[1:7]
    conv_oprice = float(conv_oprice[0:2] + conv_oprice[3:7])
    #comapring with current prices
    if conv_iprice != iphone_price:
        print("Price Difference Found!\nSending Mail...")
        sendMail()
        print("Updating Json...")
        updateJson()
        print("Resetting Price...")
        setPrice()
    elif conv_oprice != oneplus_price:
        print("Price Difference Found!\nSending Mail...")
        sendMail()
        print("Updating Json...")
        updateJson()
        print("Resetting Price...")
        setPrice()
    else:
        print("Prices are same!")
#refreshes every 20s to and if prices have changed, updates the json file, and sends an email
while True:
    print("Updating Prices...")
    setPrice()
    comparePrices()
    print("Prices Updated!\nRechecking in 20s...")
    time.sleep(20)