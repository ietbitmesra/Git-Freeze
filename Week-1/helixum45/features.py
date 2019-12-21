import requests
from bs4 import BeautifulSoup
import os
import json
import smtplib


class Features:

    def __init__(self,name):
        self.name= name
        pre_url = "https://www.flipkart.com/search?q="
        post_url = "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
        mobile_url = "%20".join(list(self.name.split(" ")))
        
        self.url = pre_url+mobile_url+post_url


    def getSpecs(self):
        try: 
            page = requests.get(self.url)
            soup = BeautifulSoup(page.content,"html5lib")
        except:
            print("Check your internet connectivity")
            return None

    
        link = soup.findAll("a",{"class":"_31qSD5"})
        linkOfModel = 'https://www.flipkart.com'+link[0]['href']
        
        specs_page = requests.get(linkOfModel)
        specs_soup = BeautifulSoup(specs_page.content,"html5lib")
        
        price = specs_soup.findAll('div',{'class':'_1vC4OE _3qQ9m1'})
        
        specs_elab = specs_soup.findAll('div',{'class':'_2RngUh'})
        
        required_specs = ['Model Name','Color','SIM Type','Hybrid Sim Slot','SAR Value','Display Size','Resolution','Operating System','Processor Type',
                 'Primary Camera','Secondary Camera','GPU','Processor Core','Primary Clock Speed','Internal Storage','RAM','Network Type']

        self.modelPrice = price[0].text
        
        row_1 = ['Price']
        row_2 = [self.modelPrice]
        
        for j in range(len(specs_elab)):
            row1 = specs_elab[j].findAll('td',{'class':'_3-wDH3 col col-3-12'})
            row2 = specs_elab[j].findAll('li',{'class':'_3YhLQA'})
            for i in range(len(row1)):
                if(row1[i].text in required_specs):
                    row_1.append(row1[i].text)
                    row_2.append(row2[i].text)

        modelFeatures = dict(zip(row_1,row_2))
        
        return modelFeatures
            
    
    def saveToJSON(self):
        
        current_folder_path = os.getcwd()
        filePath = current_folder_path+'/'+'{}.json'.format(self.name)
        
        values = self.getSpecs()

        with open(filePath, 'w', encoding='utf-8') as f:
            json.dump(values, f, ensure_ascii=False, indent=4)
            

        
class compareJSON():
    def __init__(self,mobile1, mobile2):
        self.mobile1Data = mobile1.getSpecs()
        self.mobile2Data = mobile2.getSpecs()
        
    def saveJSONComparision(self):
        current_folder_path = os.getcwd()
        filePath = current_folder_path+'/'+'{}.json'.format("comparisionData")
        
        mobile1Specs = self.mobile1Data
        mobile2Specs = self.mobile2Data
        
        values = [mobile1Specs, mobile2Specs]
        
        with open(filePath, 'w', encoding='utf-8') as f:
            json.dump(values, f, ensure_ascii=False, indent=4)
            
        print("<<<<<<<comparisionData.json saved at >>>>>>>>"+filePath)
        
                
