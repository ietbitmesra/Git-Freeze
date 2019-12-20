class Basic:
    
    def __init__(self):
        a = None
        
    def get_url(self):
        from googlesearch import search
        
        query = "smartprix" + input("Enter mobile/ model name: ")
        url_list = []
        for j in search(query, tld="co.in", num=10, stop = 5, pause=2): 
            url_list.append(str(j))
        url = url_list[0]
        print("Scanning From URL: ", url)
        return str(url)
        
    def prepare(self, url = None):
        
        if url is None:
            url = self.get_url()
        
        import requests
        from bs4 import BeautifulSoup
        response = requests.get(url)
        content = str(response.content)[2:-1]
        res_soup = BeautifulSoup(content, 'html.parser')
        
        specval = []
        specval.append( res_soup.find('div', class_='info').find('a').text)
        specval.append( 'INR ' + str(res_soup.find('span', class_='price').text)[12:])
        
        spec = []
        for i in res_soup.find('ul', class_='pros').find_all('span'):
            spec.append(i.text)
        for i in res_soup.find('ul', class_='cons').find_all('span'):
            spec.append(i.text)
        
        for i in spec:
            i = i.replace('\\xe2\\x80\\x89', ' ')
            specval.append(i)
        
        speckey = ["Name: ", "Price: ", "Connectivity: " ,"Processor: ", "Memory: ", "Battery: ", "Screen: ", "Camera: ", "External Memory: ", "OS: "]
        di_json = {}
        for i in range(len(specval)):
            di_json[str(specss[i])] = specval[i]

        return di_json
        
    def get_json(self, di_json = None):
        
        if di_json is None:
            di_json = self.prepare()
        
        import json
        with open('results.json', 'a') as fp:
            json.dump(di_json, fp, indent= 4)

    def enter(self):
        
        import os
        if os.path.exists("results.json"):
            os.remove("results.json")
            
        choice = input("Enter F to get json for Test condition ie iPhone 11 vs OnePlus 7t pro,\nany other key for Normal Operation:\n")
        if choice in ['f', 'F']:
            self.get_json(self.prepare("https://www.smartprix.com/mobiles/apple-iphone-11-ppd17p0q4s2c"))
            self.get_json(self.prepare("https://www.smartprix.com/mobiles/oneplus-7t-pro-ppd16isrkf1u"))
        else:
            elts = int(input("Enter no of Devices you wish to compare:\n"))
            for cases in range(elts):
                self.get_json()


class Notif:
    
    def __init__(self):
        
        namesake = None
        sender_eml = input("Sender email: ")
        sender_psswd = input("Sender Password: ")                    #enter two-check password for gmail if needed
        
    def send_email(self, rec_email = None, message = None):
        
        import ssl
        from smtplib import SMTP_SSL
        
        if rec_email is None:
            rec_email = self.get_rec()
        if message is None:
            message = self.get_msg()
        
        with SMTP_SSL("smtp.gmail.com", port = 465, context = ssl.create_default_context()) as server:
            server.login(self.sender_eml, self.sender_psswd)
            server.sendmail(self.sender_eml, rec_email, message)
            
    def get_rec(self):
        
        inp = input("Enter mail to send to: ")
        return inp
    
    def get_price(self, url = None):
        
        if url is None:
            pass
        
        b_obj = Basic()
        dicti = b_obj.prepare(url)
        dd = [dicti['Name: '], dicti['Price: ']]
        return dd
    
    def if_change(self, initial = None, url = None):
        
        if initial is None:
            return True
        if url is None:
            pass
        
        dicti == self.get_price(url)[1]
        
        return dicti != initial
    
    def notify(self):
        
        import time
        
        rec_email = self.get_rec()
        cases = int(input("How many devices to be notified about: "))
        url_list = []
        price_list = [0] * cases
        
        for case in range(cases):
            url = input("Enter the url of the device to be notified about: ")
            url_list.append(url)
            price_list[case] = self.get_price(url_list[case])[1]
            
        for mins in range(14400):                                  # for 10 days notifications
            time.sleep(60)
            msg = "Subject: Price Change\n"
            for case in cases:
                if self.if_change(initial = price_list[case], url = url_list[case]):
                    msg += str(self.get_price(url_list[case])[0]) + " changed price to " + str(self.get_price(url_list[case])[1])
                    price_list[case] = self.get_price(url_list[case])[1]
            
            self.send_email(rec_email = rec_email, message = msg)

n = Notif()
n.notify()