import json
import requests
from bs4 import BeautifulSoup as soup

class mobile_features():
    """Class to create and return a dictionary of features of a phone from flipkart"""
    def __init__(self, phone_type, phone_url):
        self.phone_type = phone_type
        self.phone_url = phone_url
        self.phone_price = ""
        self.phone = dict()
        self.phone_features = ""
        self.phone_page = ""
        self.phone_soup = ""

    def get_response(self):
        self.phone_page = requests.get(self.phone_url)

    def parse(self):
        self.phone_soup = soup(self.phone_page.content, 'html.parser')

    def get_features(self):
        self.phone_price = self.phone_soup.select('div._1vC4OE')[0].get_text()
        print(self.phone_type +" - "+ self.phone_price)
        self.phone_price = self.phone_price[1:]
        self.phone_features = self.phone_soup.select('#container table._3ENrHu')

    def create_dictionary(self):
        self.phone['Price'] = self.phone_price
        for category in self.phone_features:
            for features in category.select('tr._3_6Uyw'):
                Type = features.select('td._3-wDH3')[0].get_text()
                feature = features.select('td._2k4JXJ li._3YhLQA')[0].get_text()
                self.phone.update({Type : feature})

    def call_functions(self):
        self.get_response()
        self.parse()
        self.get_features()
        self.create_dictionary()
        return self.phone

def main():
    iphone_url = 'https://www.flipkart.com/apple-iphone-11-black-64-gb/p/itm0f37c2240b217?pid=MOBFKCTSVZAXUHGR&lid=LSTMOBFKCTSVZAXUHGREPBFGI&marketplace=FLIPKART&srno=s_1_2&otracker=search&otracker1=search&fm=SEARCH&iid=4ec7cfd9-9360-4726-89a1-6d4723f4124d.MOBFKCTSVZAXUHGR.SEARCH&ppt=sp&ppn=sp&ssid=3bqcgs0jj827icqo1576479418646&qH=d6db477051465f9a'
    oneplus_url = 'https://www.flipkart.com/oneplus-7t-pro-haze-blue-256-gb/p/itm0ce470755470d?pid=MOBFHC8GY8XRXJPF&lid=LSTMOBFHC8GY8XRXJPFPLKHLS&marketplace=FLIPKART&srno=s_1_1&otracker=AS_Query_OrganicAutoSuggest_2_10_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_2_10_na_na_na&fm=SEARCH&iid=f5a682fd-8c7b-4e2a-8395-ec360dc65349.MOBFHC8GY8XRXJPF.SEARCH&ppt=sp&ppn=sp&ssid=u84mk0yrvpvkmtq81576479448004&qH=cbe63fd794ac7f32'

    iphone = mobile_features("Iphone 11", iphone_url)
    Iphone = iphone.call_functions()
    oneplus = mobile_features("Oneplus 7t pro", oneplus_url)
    Oneplus = oneplus.call_functions()

    file_iphone = open('iphone.txt', 'w',)
    json.dump(Iphone, file_iphone, separators=('\n\n', ':'))
    file_iphone.close()

    file_oneplus = open('oneplus.txt', 'w')
    json.dump(Oneplus, file_oneplus, separators=('\n\n', ':'))
    file_oneplus.close()

if __name__ == '__main__':
    main()
