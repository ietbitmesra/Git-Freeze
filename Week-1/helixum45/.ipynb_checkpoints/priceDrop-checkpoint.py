import requests
from bs4 import BeautifulSoup
import os
import json
import smtplib
from features import Features
import time


class trackPrice:
    
    def __init__(self,mobile, initialPrice,senderEmail,senderPassword,receiverEmail):
        self.mobile = mobile
        self.initialPrice = initialPrice
        self.senderEmail = senderEmail
        self.senderPassword = senderPassword
        self.receiverEmail = receiverEmail
        
    def __init__(self,mobile1,mobile2, initialPrice,senderEmail,senderPassword,receiverEmail):
        self.mobile1 = mobile1
        self.mobile2 = mobile2
        self.initialPrice = initialPrice
        self.senderEmail = senderEmail
        self.senderPassword = senderPassword
        self.receiverEmail = receiverEmail
        
    def priceDown(self,mobile):
        currentPrice = int(''.join(mobile.getSpecs()['Price'][1:].split(',')))
        if(currentPrice < initialPrice):
            return currentPrice
        else:
            return 0
        
    def sendMail(self,mobile): 
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        
        s.login(self.senderEmail, self.senderPassword) 
        
        modelName = mobile.getSpecs()['Model Name']
        priceD = self.priceDown()
        
        message = "Hey boy there is price drop for the model {Model Name} you had searched for.It is now available at {priceD}".format()

        s.sendmail(senderEmail, receiverEmail, message) 

        s.quit() 
        
    def trackAndNotifyOne(self, timeToCheck):
        while True:
            
            if(self.priceDown(self.mobile)):
                self.sendMail(self.mobile)
            
            time.sleep(timeToCheck)
    
    def trackAndNotifyTwo(self, timeToCheck):
        while True:
            
            if(self.priceDown(self.mobile1)):
                self.sendMail(self.mobile1)
                
            if(self.priceDown(self.mobile2)):
                self.sendMail(self.mobile2)
                
            time.sleep(timeToCheck)