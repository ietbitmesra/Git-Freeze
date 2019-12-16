import requests
import json
from bs4 import BeautifulSoup as soup

iphone_url = 'https://www.flipkart.com/apple-iphone-11-black-64-gb/p/itm0f37c2240b217?pid=MOBFKCTSVZAXUHGR&lid=LSTMOBFKCTSVZAXUHGREPBFGI&marketplace=FLIPKART&srno=s_1_2&otracker=search&otracker1=search&fm=SEARCH&iid=4ec7cfd9-9360-4726-89a1-6d4723f4124d.MOBFKCTSVZAXUHGR.SEARCH&ppt=sp&ppn=sp&ssid=3bqcgs0jj827icqo1576479418646&qH=d6db477051465f9a'
oneplus_url = 'https://www.flipkart.com/oneplus-7t-pro-haze-blue-256-gb/p/itm0ce470755470d?pid=MOBFHC8GY8XRXJPF&lid=LSTMOBFHC8GY8XRXJPFPLKHLS&marketplace=FLIPKART&srno=s_1_1&otracker=AS_Query_OrganicAutoSuggest_2_10_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_2_10_na_na_na&fm=SEARCH&iid=f5a682fd-8c7b-4e2a-8395-ec360dc65349.MOBFHC8GY8XRXJPF.SEARCH&ppt=sp&ppn=sp&ssid=u84mk0yrvpvkmtq81576479448004&qH=cbe63fd794ac7f32'

iphone_page = requests.get(iphone_url)
oneplus_page = requests.get(oneplus_url)

iphone_soup = soup(iphone_page.content, 'html.parser')
oneplus_soup = soup(oneplus_page.content, 'html.parser')

iphone_price = iphone_soup.select('div._1uv9Cb')
print(iphone_price)
iphone_features = iphone_soup.select('#container table._3ENrHu')
oneplus_features = oneplus_soup.select('#container table._3ENrHu')

iphone = dict()
oneplus = dict()
for category in iphone_features:
    for features in category.select('tr._3_6Uyw'):
        Type = features.select('td._3-wDH3')[0].get_text()
        feature = features.select('td._2k4JXJ li._3YhLQA')[0].get_text()
        iphone.update({Type : feature})

for category in oneplus_features:
    for features in category.select('tr._3_6Uyw'):
        Type = features.select('td._3-wDH3')[0].get_text()
        feature = features.select('td._2k4JXJ li._3YhLQA')[0].get_text()
        oneplus.update({Type : feature})

f1 = open('iphone.txt', 'w')
json.dump(iphone, f1)
f1.close()
f2 = open('oneplus.txt', 'w')
json.dump(oneplus, f2)
f2.close()

