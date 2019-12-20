import csv
import json
import smtplib
from urllib.request import urlopen
import time

from bs4 import BeautifulSoup


def mail_send():
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("holidaywalasoldier@gmail.com", "JaiHind1947")
    # message to be sent
    message = "Your preferred Phone Prices have changed... Wanna Take a look???"
    # sending the mail
    s.sendmail("holidaywalasoldier@gmail.com", "be10053.18@bitmesra.ac.in", message)
    # terminating the session
    print("Mail sent....")
    s.quit()


def setting_up_dataframe():
    data1 = {}
    quote_page = 'https://www.flipkart.com/apple-iphone-11-black-64-gb/p/itm0f37c2240b217?pid=MOBFKCTSVZAXUHGR&lid=LSTMOBFKCTSVZAXUHGREPBFGI&marketplace=FLIPKART&srno=s_1_2&otracker=AS_QueryStore_OrganicAutoSuggest_0_7_na_na_pr&otracker1=AS_QueryStore_OrganicAutoSuggest_0_7_na_na_pr&fm=SEARCH&iid=6ee1ccc2-e93d-4cbf-968b-b0c0f6cf0331.MOBFKCTSVZAXUHGR.SEARCH&ppt=HomePage&ppn=Home&ssid=am886o5w7k0000001576832575801&qH=3422ffa2c9fac114'
    fields = ['Price', 'OS', 'RAM', 'Camera', 'Size', 'Connectivity', 'Storage', 'Processor']
    html = urlopen(quote_page).read()
    soup = BeautifulSoup(html, 'html.parser')
    price_box = soup.find('div', attrs={'class': '_1vC4OE _3qQ9m1'})
    price_str = price_box.text.strip()
    price_str = price_str[1:3] + price_str[4:]
    price = float(price_str)
    os_box = soup.findAll('li', attrs={'class': '_3YhLQA'})
    os = os_box[14].text.strip()
    ram = "4 GB"  # kyunki nhi mila
    camera_box = soup.findAll('li', attrs={'class': '_2-riNZ'})
    camera = camera_box[2].text.strip()
    size_box = soup.findAll('li', attrs={'class': '_2-riNZ'})
    size = size_box[1].text.strip()
    connectivity_box = soup.findAll('li', attrs={'class': '_3YhLQA'})
    connectivity = connectivity_box[34].text.strip()
    storage_box = soup.findAll('li', attrs={'class': '_3YhLQA'})
    storage = storage_box[16].text.strip()
    processor_box = soup.findAll('li', attrs={'class': '_3YhLQA'})
    processor = processor_box[15].text.strip()
    quantities = [price, os, ram, camera, size, connectivity, storage, processor]
    data1['iPhone 11'] = []
    for i in range(0, len(fields)):
        data1['iPhone 11'].append({fields[i]: quantities[i]})
    quote_page1 = 'https://www.flipkart.com/oneplus-7t-pro-haze-blue-256-gb/p/itm0ce470755470d?pid=MOBFHC8GY8XRXJPF&lid=LSTMOBFHC8GY8XRXJPFR8XK6R&marketplace=FLIPKART&srno=s_1_1&otracker=AS_Query_OrganicAutoSuggest_2_10_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_2_10_na_na_na&fm=SEARCH&iid=83ad12f7-0cd7-4cdd-a55d-d406d05a3fd6.MOBFHC8GY8XRXJPF.SEARCH&ppt=sp&ppn=sp&ssid=vd1q1fc32o0000001576840877214&qH=cbe63fd794ac7f32'
    html1 = urlopen(quote_page1).read()
    soup1 = BeautifulSoup(html1, 'html.parser')
    price_box1 = soup1.find('div', attrs={'class': '_1vC4OE _3qQ9m1'})
    price1_str = price_box1.text.strip()
    price1_str = price1_str[1:3] + price1_str[4:]
    price1 = float(price1_str)
    os_box1 = soup1.findAll('li', attrs={'class': '_3YhLQA'})
    os1 = os_box1[14].text.strip()
    ram_box1 = soup1.findAll('li', attrs={'class': '_3YhLQA'})
    ram1 = ram_box1[19].text.strip()
    camera_box1 = soup1.findAll('li', attrs={'class': '_2-riNZ'})
    camera1 = camera_box1[2].text.strip()
    size_box1 = soup1.findAll('li', attrs={'class': '_2-riNZ'})
    size1 = size_box1[1].text.strip()
    connectivity_box1 = soup1.findAll('li', attrs={'class': '_3YhLQA'})
    connectivity1 = connectivity_box1[34].text.strip()
    storage_box1 = soup1.findAll('li', attrs={'class': '_3YhLQA'})
    storage1 = storage_box1[18].text.strip()
    processor_box1 = soup1.findAll('li', attrs={'class': '_3YhLQA'})
    processor1 = processor_box1[15].text.strip()
    quantities1 = [price1, os1, ram1, camera1, size1, connectivity1, storage1, processor1]
    data1['OnePlus 7T Pro'] = []
    for i in range(0, len(fields)):
        data1['OnePlus 7T Pro'].append({fields[i]: quantities1[i]})
    with open('data.json', 'w') as outfile:
        json.dump(data1, outfile, indent=2)
    with open('index.csv', 'w', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Specifications", "iPhone 11", "OnePlus 7T Pro"])
        for i in range(0, len(fields)):
            writer.writerow([fields[i], quantities[i], quantities1[i]])
    prices = [price, price1]
    return prices


def compare_both_prices(prices2):
    quote_page = 'https://www.flipkart.com/apple-iphone-11-black-64-gb/p/itm0f37c2240b217?pid=MOBFKCTSVZAXUHGR&lid=LSTMOBFKCTSVZAXUHGREPBFGI&marketplace=FLIPKART&srno=s_1_2&otracker=AS_QueryStore_OrganicAutoSuggest_0_7_na_na_pr&otracker1=AS_QueryStore_OrganicAutoSuggest_0_7_na_na_pr&fm=SEARCH&iid=6ee1ccc2-e93d-4cbf-968b-b0c0f6cf0331.MOBFKCTSVZAXUHGR.SEARCH&ppt=HomePage&ppn=Home&ssid=am886o5w7k0000001576832575801&qH=3422ffa2c9fac114'
    html = urlopen(quote_page).read()
    soup = BeautifulSoup(html, 'html.parser')
    price_box = soup.find('div', attrs={'class': '_1vC4OE _3qQ9m1'})
    price_temp_str = price_box.text.strip()
    price_temp_str = price_temp_str[1:3] + price_temp_str[4:]
    price_temp = float(price_temp_str)
    if price_temp < prices2[0]:
        print("Price of iPhone has Changed.. Sending Mail....")
        prices2[0] = price_temp
        mail_send()
        print("Updating the JSONs....")
        setting_up_dataframe()
        print("JSONs and CSV updated....")
    quote_page1 = 'https://www.flipkart.com/oneplus-7t-pro-haze-blue-256-gb/p/itm0ce470755470d?pid=MOBFHC8GY8XRXJPF&lid=LSTMOBFHC8GY8XRXJPFR8XK6R&marketplace=FLIPKART&srno=s_1_1&otracker=AS_Query_OrganicAutoSuggest_2_10_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_2_10_na_na_na&fm=SEARCH&iid=83ad12f7-0cd7-4cdd-a55d-d406d05a3fd6.MOBFHC8GY8XRXJPF.SEARCH&ppt=sp&ppn=sp&ssid=vd1q1fc32o0000001576840877214&qH=cbe63fd794ac7f32'
    html1 = urlopen(quote_page1).read()
    soup1 = BeautifulSoup(html1, 'html.parser')
    price_box1 = soup1.find('div', attrs={'class': '_1vC4OE _3qQ9m1'})
    price_temp1_str = price_box1.text.strip()
    price_temp1_str = price_temp1_str[1:3] + price_temp1_str[4:]
    price_temp1 = float(price_temp1_str)
    if price_temp1 < prices2[1]:
        print("Price of One Plus 7T Pro has changed.. Sending Mail....")
        prices2[1] = price_temp1
        mail_send()
        print("Updating the JSONs....")
        setting_up_dataframe()
        print("JSONs and CSV updated....")


print("Creating JSON and CSV File.......")
prices1 = setting_up_dataframe()
while True:
    print("Checking for Price Changes....")
    compare_both_prices(prices1)
    time.sleep(1800)
