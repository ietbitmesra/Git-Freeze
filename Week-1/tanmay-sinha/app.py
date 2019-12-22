# App for receiving the parameters from GUI_app
# and scraping site and then generating/appending
# to the JSON file.
# Also sends mails and notifications regarding price drops.

import requests
from bs4 import BeautifulSoup
import httplib2
from notify_run import Notify
import smtplib
import time
import os
import subprocess
import sys
from datetime import datetime
import json


with open("config.json", "r") as myfile:
    config = json.load(myfile)


# for generating JSON output and
# sending notification.
class PhoneDetails():

    # checking if URL is correct
    def check_url(self, url):
        if len(url) == 0:
            URL = input(f"Enter the URL from 91mobiles.com only :\n")
        else:
            URL = url
        try:
            page = requests.get(URL)
            if page.status_code == 200:
                print("Correct URL")
                self.URL = URL
                self.scraping_site(page)
            else:
                print('Wrong URL!! Enter correct URL:')
        except requests.exceptions.RequestException:
            print('Wrong URL!! Enter correct URL:')

    def scraping_site(self, page):
        soup = BeautifulSoup(page.content, 'html.parser')
        features = soup.find_all("td", {"class": "spec_ttle"})
        values = soup.find_all("td", {"class": "spec_des"})
        phone_name = soup.find("span", {"itemprop": "name"}).get_text()
        stores = soup.find_all("img", {"class": "img_alt"})
        prices = soup.find_all("span", {"class": "prc"})
        # scraping the details and making dictionary.
        self.phone_name = phone_name
        dictionary = {}
        dictionary['URL'] = self.URL
        for item in range(len(features)):
            feature = features[item].text.replace("\n", "").strip()
            value = values[item].text.replace("\n", "").strip()

            if '  ' in value:
                value = value[0:value.find('  ')]

            dictionary[feature] = value

            if len(value) is 0:
                if 'yes' in str(values[item]):
                    dictionary[feature] = 'Yes'
                else:
                    dictionary[feature] = 'No'

        # scraping the price and putting it in dictionary.
        dictionary['prices'] = {}
        for item in range(len(prices)):
            store = stores[item]['alt']
            price = prices[item].get_text().replace("\n", "")
            dictionary['prices'][store] = price

        self.jsonstr = json.dumps(dictionary, sort_keys=True, indent=4)
        self.make_json()

    # making the JSON File
    def make_json(self):
        try:
            with open("phone_details.json", "r") as myfile:
                content = myfile.read()
                if len(content) > 0:
                    flag = 1
                else:
                    flag = 0
        except FileNotFoundError as exception:
            print(exception)
            content = ''
            flag = 0

        # checking if the phone already exists
        if f'"{self.phone_name}"' not in content:
            with open("phone_details.json", "w+") as myfile:
                if flag == 1:
                    content = content[:-1]
                    content = content + '\n,\n'+f'"{self.phone_name}" : \
                    ' + self.jsonstr + '\n}'
                else:
                    content = '{\n'+f'"{self.phone_name}": '+self.jsonstr+'\n}'
                myfile.write(content)
        else:
            print("You already have the phone details")
        # Opening JSON file
        self.open_file()

    @staticmethod
    def open_file():
        # opening the JSON file
        filepath = os.getcwd()
        try:
            # for windows
            os.startfile(filepath+'/phone_details.json')
        except:
            # for linux
            try:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, filepath+'/phone_details.json'])
            except NotImplementedError:
                pass

    @staticmethod
    def phone_desktop_notify(msg):
        # PUSH notification to phone and laptop
        try:
            notify = Notify()
            notify.send(msg)
        except NotImplementedError:
            pass

    @staticmethod
    def email_notify(msg):

        # EMAIL notification
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        # Replace tomail with EMAIL ID where mail will be sent
        try:
            server.login(config['sender_mail'], config['sender_password'])
            for item in config['receiver_mails']:
                server.sendmail(config['sender_mail'], item, msg)
            print("\nEmails sent\n")
            server.close()

        except smtplib.SMTPAuthenticationError:
            print('\nwrong email/password\n\
            Please try again with correct credentials.')
            print("please UPDATE your Email/Password and run the app again.\n")

    # checking current prices at different sites .
    def check_price(self):
        page = requests.get(self.URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        prices = soup.find_all("span", {"class": "prc"})
        stores = soup.find_all("img", {"class": "img_alt"})

        for item in range(len(prices)):
            store = stores[item]['alt']
            price = prices[item].get_text().replace("\n", "")
            price = int(price[price.find(' ')+1:-3].replace(",", ""))
            # checking the minimum price.
            if price < self.min_price:
                self.min_price = price
                self.lowest_priced_store = store
        # Comparing Price
        self.price_comparator()

    # Comparing the current and previous prices and sending notifications.
    def price_comparator(self):
        if self.BASE_PRICE >= self.min_price:
            print("Base price reached")
            msg1 = f"The price of {self.phone_name} is \n\
            Rs. {self.min_price} which is\n\
            below the base price on {self.lowest_priced_store}\n\
            as of {datetime.now()}.\n\
            HURRY UP!!!!"
            self.phone_desktop_notify(msg1)
            self.email_notify(msg1)

        elif (self.count == 1):
            self.prev_min_price = self.min_price

        elif self.prev_min_price > self.min_price:
            print('Price has decreased')
            msg = f"Price has decreased \n\
            from Rs. {self.prev_min_price} to Rs. {self.min_price} for\n\
            {self.phone_name} on {self.lowest_priced_store} as of {datetime.now()}."
            self.phone_desktop_notify(msg)
            self.email_notify(msg)
            self.prev_min_price = self.min_price
        print(f"Lowest Price for {self.phone_name} is\n\
         Rs. {self.min_price} on {self.lowest_priced_store}\n \
        as of {datetime.now()}")

    # Function to check price at given Intervals.
    def regular_price_checker(self, time_interval, base_price):
        self.BASE_PRICE = base_price
        self.min_price = 1000000
        self.prev_min_price = 1000000
        self.count = 1
        while True:
            self.check_price()
            self.count += 1
            time.sleep(time_interval)


# Main starts here
if __name__ == "__main__":

    # making class
    phone_details = PhoneDetails()

    # checking URL and generating JSON file.
    jsonstr = phone_details.check_url("")

    print('URL entered and JSON file created .')

    BASE_PRICE = int(input("Enter the price at which you want to purchase:\n"))
    time_interval = int(input("Enter the time interval in seconds:"))
    phone_details.regular_price_checker(time_interval, BASE_PRICE)
