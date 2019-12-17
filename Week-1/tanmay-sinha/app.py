import requests, time, os
import subprocess
import smtplib
import sys
from getpass import getpass
from bs4 import  BeautifulSoup
from notify_run import Notify
from datetime import datetime
import json
import httplib2

with open("config.json","r") as f:
    config = json.load(f)

class PhoneDetails:

    # checking if URL is correct
    def check_url(self):
        
        while True:
            URL = input(f"Enter the URL {i+1} from 91mobiles.com only (for better results):\n")
            try:
                page = requests.get(URL)
                if page.status_code ==200:
                    break
                else:
                    print('Wrong URL!! Enter correct URL:')
            except:
                print('Wrong URL!! Enter correct URL:')  

        URLlist.append(URL)

        return page 
        
        
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
        return jsonstr

    # checking current prices at different sites .
    def check_price(self, MIN_PRICE, lowest_priced_store, lowest_priced_phone):
        for i in range(len(URLlist)):
            
            page = requests.get(URLlist[i])
            soup = BeautifulSoup(page.content, 'html.parser')
            prices = soup.find_all("span", {"class":"prc"})
            phone_name = soup.find("span", {"itemprop":"name"}).get_text()
            stores = soup.find_all("img", {"class":"img_alt"})
            
            for j in range(len(prices)):
                store = stores[j]['alt']
                price = prices[j].get_text().replace("\n","")
                price = int(price[price.find(' ')+1:-3].replace(",",""))
                # checking the minimum price.
                if price < MIN_PRICE :
                    MIN_PRICE = price
                    lowest_priced_store = store
                    lowest_priced_phone = phone_name
            
        return MIN_PRICE, lowest_priced_store, lowest_priced_phone                

    # making the JSON File
    def make_json(self, jsonstr, phone_name):
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
        if f"{phone_name}" not in content:
            with open("phone_details.json","w+") as myfile:
                if flag == 1:
                    content = content[:-1]
                    content = content + '\n,\n'+f'"{phone_name}" : ' + jsonstr + '\n}'
                else:
                    content = '{\n'+ f'"{phone_name}" : ' + jsonstr +'\n}'
                myfile.write(content)
        else:
            print("You already have the phone details")
            

    def open_file(self):
        # opening the JSON file
        filepath = os.getcwd()
        try:
            # for windows
            os.startfile(filepath+'/phone_details.json') 
        except:
            # for linux
            opener ="open" if sys.platform == "darwin" else "xdg-open" 
            subprocess.call([opener, filepath+'/phone_details.json'])

    
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
            print("Emails sent")
            server.close()
        except:
            print('wrong email/password: Please try again..')
            exit(0)


    def price_comparator(self, MIN_PRICE,\
         lowest_priced_store, lowest_priced_phone,\
             PREV_MIN_PRICE):

        if BASE_PRICE >= MIN_PRICE :
            print("Base price reached")
            msg1 = f"The price of {lowest_priced_phone} is Rs. {MIN_PRICE} which is\n\
                below the base price on {lowest_priced_store} as of {datetime.now()}.\n\
            HURRY UP!!!!"
            self.phone_desktop_notify(msg1)
            self.email_notify(msg1)

        elif (count==1):
            PREV_MIN_PRICE = MIN_PRICE

        elif PREV_MIN_PRICE > MIN_PRICE:
            print('Price has decreased')
            msg = f"Price has decreased from Rs. {PREV_MIN_PRICE} to Rs. {MIN_PRICE}\n\
                which is of {lowest_priced_phone} on {lowest_priced_store} as of {datetime.now} ."
            self.phone_desktop_notify(msg)
            self.email_notify(msg)
            PREV_MIN_PRICE = MIN_PRICE
        
        return PREV_MIN_PRICE

# Main starts here
if __name__ == "__main__":

    no_of_urls = int(input("Enter the number of phones you want to track:"))
    # variables assigned
    MIN_PRICE = 1000000
    lowest_priced_store = ''
    lowest_priced_phone = ''
    PREV_MIN_PRICE = MIN_PRICE
    URLlist = []


    for i in range(no_of_urls):
        # making class
        phone_details  = PhoneDetails()
        # checking URL
        webpage = phone_details.check_url()

        # getting json of details
        jsonstr = phone_details.scraping_site(webpage)

        # making and appending the JSON File
        phone_details.make_json(jsonstr,phone_details.phone_name)

    # opening the JSON File
    phone_details.open_file()

    print('URLS entered and JSON file created .')
    
    BASE_PRICE = int(input("Enter the price at which you want to purchase:\n"))

    count = 1
    while(True):
        MIN_PRICE, lowest_priced_store, lowest_priced_phone =\
        phone_details.check_price(MIN_PRICE,lowest_priced_store,\
            lowest_priced_phone)

        PREV_MIN_PRICE = phone_details.price_comparator(MIN_PRICE, lowest_priced_store,\
             lowest_priced_phone, PREV_MIN_PRICE)   
        print(f"Lowest Price is of {lowest_priced_phone} at Rs. {MIN_PRICE} on {lowest_priced_store}\n \
            as of {datetime.now()}")
        count += 1 
        # Change the time according to your convenience.
        time.sleep(10) # in seconds
