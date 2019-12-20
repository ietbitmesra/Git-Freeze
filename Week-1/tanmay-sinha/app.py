import requests, time, os
import subprocess
import smtplib
import sys
from bs4 import  BeautifulSoup
from notify_run import Notify
from datetime import datetime
import json
import httplib2

with open("config.json","r") as f:
    config = json.load(f)
MIN_PRICE = 1000000
lowest_priced_store = ''
PREV_MIN_PRICE = MIN_PRICE
count = 1

class PhoneDetails():

    # checking if URL is correct
    def check_url(self,url):
       
        if len(url) == 0:
            URL = input(f"Enter the URL from 91mobiles.com only (for better results):\n")
        else:
            URL = url
        try:
            page = requests.get(URL)
            if page.status_code ==200:
                print("Correct URL")
                self.URL = URL
                self.scraping_site(page)
            else:
                print('Wrong URL!! Enter correct URL:')
        except:
            print('Wrong URL!! Enter correct URL:')  
         
        
    def scraping_site(self, page):
        soup = BeautifulSoup(page.content, 'html.parser')
        features = soup.find_all("td", {"class":"spec_ttle"})
        values = soup.find_all("td", {"class":"spec_des"})
        phone_name = soup.find("span", {"itemprop":"name"}).get_text()
        stores = soup.find_all("img", {"class":"img_alt"})
        prices = soup.find_all("span", {"class":"prc"})
        # scraping the details and making dictionary.
        self.phone_name = phone_name
        dictionary ={}
        dictionary['URL'] = self.URL
        for i in range(len(features)):
            feature = features[i].text.replace("\n", "").strip()
            value = values[i].text.replace("\n", "").strip()

            if '  ' in value:
                value = value[0:value.find('  ')]

            dictionary[feature] = value

            if len(value) is 0:
                if 'yes' in str(values[i]):
                    dictionary[feature] = 'Yes'
                else:
                    dictionary[feature] = 'No'

        #scraping the price and putting it in dictionary.
        dictionary['prices'] ={}
        for i in range(len(prices)):
            store = stores[i]['alt']
            price = prices[i].get_text().replace("\n","")
            dictionary['prices'][store] = price

        jsonstr = json.dumps(dictionary,sort_keys=True,indent=4)
        self.make_json(jsonstr)

    # making the JSON File
    def make_json(self, jsonstr):
        try:
            with open("phone_details.json","r") as myfile:
                content = myfile.read()
                if len(content) > 0:
                    flag = 1
                else:
                    flag = 0
        except:
            content = ''
            flag = 0

        # checking if the phone already exists
        if f'"{self.phone_name}"' not in content:
            with open("phone_details.json","w+") as myfile:
                if flag == 1:
                    content = content[:-1]
                    content = content + '\n,\n'+f'"{self.phone_name}" : ' + jsonstr + '\n}'
                else:
                    content = '{\n'+ f'"{self.phone_name}" : ' + jsonstr +'\n}'
                myfile.write(content)
        else:
            print("You already have the phone details")
        #Opening JSON file
        self.open_file()
            

    def open_file(self):
        # opening the JSON file
        filepath = os.getcwd()
        try:
            # for windows
            os.startfile(filepath+'/phone_details.json') 
        except:
            # for linux
            try:
                opener ="open" if sys.platform == "darwin" else "xdg-open" 
                subprocess.call([opener, filepath+'/phone_details.json'])
            except:
                pass

    
    def phone_desktop_notify (self, msg):
        # PUSH notification to phone and laptop
        try:
            notify = Notify()
            notify.send(msg)
        except:
            pass

    
    def email_notify(self,msg):

        # EMAIL notification
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        # Replace tomail with EMAIL ID where mail will be sent
        try:
            server.login(config['sender_mail'],config['sender_password'])
            for i in config['receiver_mails']:
                server.sendmail(config['sender_mail'], i, msg)
            print("\nEmails sent\n")
            server.close()
        except:
            print('\nwrong email/password: Please try again with correct credentials.')
            print("please UPDATE your Email/Password and run the app again.\n")

    
    # checking current prices at different sites .
    def check_price(self):
        global MIN_PRICE,lowest_priced_store
        page = requests.get(self.URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        prices = soup.find_all("span", {"class":"prc"})
        stores = soup.find_all("img", {"class":"img_alt"})
            
        for j in range(len(prices)):
            store = stores[j]['alt']
            price = prices[j].get_text().replace("\n","")
            price = int(price[price.find(' ')+1:-3].replace(",",""))
            # checking the minimum price.
            if price < MIN_PRICE :
                MIN_PRICE = price
                lowest_priced_store = store
        # Comparing Price
        self.price_comparator()
                           

    def price_comparator(self):
        global MIN_PRICE, lowest_priced_store
        global PREV_MIN_PRICE
        if BASE_PRICE >= MIN_PRICE :
            print("Base price reached")
            msg1 = f"The price of {self.phone_name} is Rs. {MIN_PRICE} which is\n\
                below the base price on {lowest_priced_store} as of {datetime.now()}.\n\
            HURRY UP!!!!"
            self.phone_desktop_notify(msg1)
            self.email_notify(msg1)

        elif (count==1):
            PREV_MIN_PRICE = MIN_PRICE

        elif PREV_MIN_PRICE > MIN_PRICE:
            print('Price has decreased')
            msg = f"Price has decreased from Rs. {PREV_MIN_PRICE} to Rs. {MIN_PRICE}\n\
                for {self.phone_name} on {lowest_priced_store} as of {datetime.now()} ."
            self.phone_desktop_notify(msg)
            self.email_notify(msg)
            PREV_MIN_PRICE = MIN_PRICE
        print(f"Lowest Price for {self.phone_name} at Rs. {MIN_PRICE} on {lowest_priced_store}\n \
            as of {datetime.now()}")

    # Function to check price at given Intervals.
    def regular_price_checker(self, time_interval, base_price):
    
        global BASE_PRICE, count
        count = 1
        BASE_PRICE = base_price
        while True:
            self.check_price()
            count += 1
            time.sleep(time_interval)
            
        
# Main starts here
if __name__ == "__main__":

    # making class
    phone_details  = PhoneDetails()

    # checking URL and generating JSON file.
    jsonstr = phone_details.check_url("")
            
    print('URL entered and JSON file created .')
    
    BASE_PRICE = int(input("Enter the price at which you want to purchase:\n"))
    time_interval = int(input("Enter the time interval in seconds:"))
    phone_details.regular_price_checker(time_interval,BASE_PRICE)