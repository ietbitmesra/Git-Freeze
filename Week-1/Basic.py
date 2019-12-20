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

b = Basic()
b.enter()
print("Thanks")