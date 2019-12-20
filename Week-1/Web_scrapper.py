import requests
from bs4 import BeautifulSoup as soup
import json
import smtplib
import csv
import datetime
from threading import Timer
# For running code every minute
def runn_multiple_times():
    # For putting date and time of entry in the "price_at_each_run.csv"
    date_time=datetime.datetime.now()
    
    #Parsing information of both the phones
    iphone_url=requests.get("https://www.flipkart.com/apple-iphone-11-white-128-gb/p/itm846a8ba21ab11?pid=MOBFKCTS4MZVJ6FJ&lid=LSTMOBFKCTS4MZVJ6FJPY4SUX&marketplace=FLIPKART&srno=s_1_1&otracker=AS_Query_OrganicAutoSuggest_2_6_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_2_6_na_na_na&fm=SEARCH&iid=1faeec82-078c-4afb-ac82-005cd00f7df2.MOBFKCTS4MZVJ6FJ.SEARCH&ppt=sp&ppn=sp&ssid=r77hztg9jk0000001576406173066&qH=3422ffa2c9fac114")
    iphone_content=iphone_url.content
    iphone_parser=soup(iphone_content,'html.parser')
    oneplus_url=requests.get("https://www.flipkart.com/oneplus-7t-pro-haze-blue-256-gb/p/itm0ce470755470d?pid=MOBFHC8GY8XRXJPF&lid=LSTMOBFHC8GY8XRXJPFHKJLSY&marketplace=FLIPKART&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_12_na_na_pr&otracker1=AS_QueryStore_OrganicAutoSuggest_1_12_na_na_pr&fm=SEARCH&iid=50b91227-2253-4339-8e22-436dc4221d50.MOBFHC8GY8XRXJPF.SEARCH&ppt=sp&ppn=sp&ssid=x6yuv8m01s0000001576410834553&qH=5e92b45a5bf6c752")
    oneplus_content=oneplus_url.content
    oneplus_parser=soup(oneplus_content,'html.parser')
    
    #Adding the Properties of Iphone
    price_iphone='Price'
    feat_name_iphone=iphone_parser.findAll("td",{"class":"_3-wDH3 col col-3-12"})
    feat_name_iphone_edit=[]
    feat_name_iphone_edit.append(price_iphone)
    for i in feat_name_iphone:
        feat_name_iphone_edit.append(i.text)
    
    #Adding the Properties of Oneplus
    
    price_oneplus='Price'
    feat_name_oneplus=oneplus_parser.findAll("td",{"class":"_3-wDH3 col col-3-12"})
    feat_name_oneplus_edit=[]
    feat_name_oneplus_edit.append(price_oneplus)
    for i in feat_name_oneplus:
        feat_name_oneplus_edit.append(i.text)
    
    #Setting the values of properties of Iphone
    feat_value_iphone=iphone_parser.findAll("li",{"class":"_3YhLQA"})
    price_iphone_value=iphone_parser.find("div",{"class":"_1vC4OE _3qQ9m1"})
    feat_value_iphone_edit=[]
    feat_value_iphone_edit.append(price_iphone_value.text)
    for i in feat_value_iphone:
        feat_value_iphone_edit.append(i.text)
    
    #Setting the values of properties of Oneplus
    feat_value_oneplus=oneplus_parser.findAll("li",{"class":"_3YhLQA"})
    price_oneplus_value=oneplus_parser.find("div",{"class":"_1vC4OE _3qQ9m1"})
    feat_value_oneplus_edit=[]
    feat_value_oneplus_edit.append(price_oneplus_value.text)
    for i in feat_value_oneplus:
        feat_value_oneplus_edit.append(i.text)   
    
    #Creating a dictionary of dictionary of the two Phones
    iphonedict = dict( zip(feat_name_iphone_edit, feat_value_iphone_edit) )
    oneplusdict = dict( zip(feat_name_oneplus_edit, feat_value_oneplus_edit) )
    finaldict = {}
    finaldict['IPHONE 11'] = iphonedict
    finaldict['ONEPLUS 7T PRO']  = oneplusdict
    
    #Creating a final dict so that the properties of two phones can be compared in the json file by creating two lists and then converting them to dict
    features_of_phones=[]
    values_of_phones=[]
    temp_dict={}
    for i in finaldict['IPHONE 11'].keys():
        if i in finaldict['ONEPLUS 7T PRO'].keys():
            features_of_phones.append(i)
    
    for j in features_of_phones:
        temp_dict['IPHONE 11']=finaldict['IPHONE 11'].get(j)
        temp_dict['ONEPLUS 7T PRO']=finaldict['ONEPLUS 7T PRO'].get(j)
        values_of_phones.append(temp_dict)
        temp_dict={}
    
    #final comp dict created which will be used to create .json file
    comp=dict(zip(features_of_phones,values_of_phones))
    
    
    #Making Json
    jw=json.dumps(comp,indent = 4,sort_keys=True)
    with open('Compare.json','w') as f:
        f.write(jw)
        f.close()
    
    #Extracting integer from string containing price for both the phones
    value_1=(price_iphone_value.text)[1:]
    value_1=value_1.replace(',','')
    value_1=int(value_1)
    value_2=(price_oneplus_value.text)[1:]
    value_2=value_2.replace(',','')
    value_2=int(value_2)
    
    #Reading and reading values in "price_at_each_run.csv" for price checking and email on price drop
    with open('price_at_each_run.csv','r+') as read_file:
        csv_reader=csv.reader(read_file, delimiter=',')
        hell=list(csv_reader)
        
        if(len(hell)!=0): #email if iphone price drops
            if(int(hell[-1][0])>value_1):
                conn=smtplib.SMTP('smtp.gmail.com:587') # smtp address and port
                conn.ehlo()
                conn.starttls() # starts tls encryption. When we send our password it will be encrypted.
                conn.login('#add_sender_mail@gmail.com','password' )
                conn.sendmail('#add_sender_mail@gmail.com', '#receiver_mail@gmail.com', 'Subject: Price Drop Alert!\n\nAttention!\n\nIphone price has dropped!\n\n:\nPrice Notifier V1.0')
                conn.quit()	
    
    
            if(int(hell[-1][1])>value_2): #email if oneplus price drops
                conn=smtplib.SMTP('smtp.gmail.com:587') # smtp address and port
                conn.ehlo()
                conn.starttls() # starts tls encryption. When we send our password it will be encrypted.
                conn.login('#add_sender_mail@gmail.com','password' )
                conn.sendmail('#add_sender_mail@gmail.com', '#receiver_mail@gmail.com', 'Subject: Price Drop Alert!\n\nAttention!\n\nOneplus price has dropped!\n\n:\nPrice Notifier V1.0')
                conn.quit()	
           
        else:
            csv_writer=csv.writer(read_file, delimiter=',')
            csv_writer.writerow(['Prev_Price_iphone','Prev_Price_oneplus','Date_Time'])
        
        csv_writer=csv.writer(read_file, delimiter=',')
        csv_writer.writerow([value_1,value_2,date_time])
    Timer(60,runn_multiple_times).start()   
runn_multiple_times()        
    