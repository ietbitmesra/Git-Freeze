import json
import time
import smtplib

from index import mobile_features as mobile

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class send_mail():
    """Class to create a smtp server and 
       then send the mail using that server"""

    def __init__(self):
        self.iphone_url = 'https://www.flipkart.com/apple-iphone-11-black-64-gb/p/itm0f37c2240b217?pid=MOBFKCTSVZAXUHGR&lid=LSTMOBFKCTSVZAXUHGREPBFGI&marketplace=FLIPKART&srno=s_1_2&otracker=search&otracker1=search&fm=SEARCH&iid=4ec7cfd9-9360-4726-89a1-6d4723f4124d.MOBFKCTSVZAXUHGR.SEARCH&ppt=sp&ppn=sp&ssid=3bqcgs0jj827icqo1576479418646&qH=d6db477051465f9a'
        self.oneplus_url = 'https://www.flipkart.com/oneplus-7t-pro-haze-blue-256-gb/p/itm0ce470755470d?pid=MOBFHC8GY8XRXJPF&lid=LSTMOBFHC8GY8XRXJPFPLKHLS&marketplace=FLIPKART&srno=s_1_1&otracker=AS_Query_OrganicAutoSuggest_2_10_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_2_10_na_na_na&fm=SEARCH&iid=f5a682fd-8c7b-4e2a-8395-ec360dc65349.MOBFHC8GY8XRXJPF.SEARCH&ppt=sp&ppn=sp&ssid=u84mk0yrvpvkmtq81576479448004&qH=cbe63fd794ac7f32'
        self.iphone = mobile("Apple Iphone 11", self.iphone_url)
        self.oneplus = mobile("OnePlus 7t Pro", self.oneplus_url)
        self.iphone_price = ""
        self.oneplus_price = ""
        self.config = dict()

    def create_server(self):
        """Method for creating a smtp server which can login
           to the required email host and send mails to the user"""

        with open('config.json', 'r') as file:
            self.config = json.load(file)
        try:
            server = smtplib.SMTP(host=self.config['host'], port=self.config['host_port'])
            server.starttls()
            server.login(self.config['email_sender'], self.config['sender_password'])
        except:
            print('Unable to establish connection due to wrong Username and Password or permission denied.')
        return server

    def send_message(self):
        """Method for getting the current price of the phones,
           then comparing it with the previous price and sending 
           mail to the user if there is a price drop"""

        while(True):
            server = self.create_server()
            self.iphone.create_dictionary()
            self.oneplus.create_dictionary()

            if self.iphone.phone['Price'] < self.iphone_price:
                for email in self.config['email_receiver']:
                    msg = MIMEMultipart()
                    msg['From'] = self.config['email_sender']
                    msg['To'] = email
                    msg['Subject'] = "Price drop in phones"
                    msg.attach(MIMEText("There is a drop in the price for the phone " + self.iphone.phone_type+", from " + self.iphone_price + " to " + self.iphone.phone['Price'], 'plain'))
                    try:
                        server.send_message(msg)
                        print("Message sent successfully to " + email)
                    except:
                        print("Unable to send message.")

            if self.oneplus.phone['Price'] < self.oneplus_price:
                for email in self.config['email_receiver']:
                    msg = MIMEMultipart()
                    msg['From'] = self.config['email_sender']
                    msg['To'] = email
                    msg['Subject'] = "Price drop in phones"
                    msg.attach(MIMEText("There is a drop in the price for the phone " + self.oneplus.phone_type + ", from " + self.oneplus_price + " to " + self.oneplus.phone['Price'], 'plain'))                
                    try:
                        server.send_message(msg)
                        print("Message sent successfully to " + email)
                    except:
                        print("Unable to send message.")

            self.iphone_price = self.iphone.phone['Price']
            self.oneplus_price = self.oneplus.phone['Price']
            server.quit()
            time.sleep(60*60)

def main():
    mail = send_mail()
    mail.send_message()

if __name__ == '__main__':
    main()
