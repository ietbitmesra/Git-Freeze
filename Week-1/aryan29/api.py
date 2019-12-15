import requests
import bs4
import sys
import json
with open("user_config.json","r") as f:
    conf=json.load(f)
class Api:
    def get_data(self,mob):
        b=requests.get(f"https://www.smartprix.com/mobiles/{mob[0]}")
        l1=bs4.BeautifulSoup(b.text,'lxml')
        price2=l1.select("#product-price .price")[0]
        try:
            a=requests.get(f"https://www.mysmartprice.com/mobile/{mob[1]}")
            l=bs4.BeautifulSoup(a.text,'lxml')
            price1=l.select(".prdct-dtl__prc-val")[0]
            price=self.getminprice(price1,price2)
        except:
            price=price2
        a=l1.select(".has-favorite-button , .cons span , .pros span")
        f_list=a
        f_list.append(price)
        return f_list
    def getminprice(self,price1,price2):
        #print((price1.getText()),price2.getText()[1:])
        if((price1.getText(),10)<(price2.getText()[1:],10)):
            return price1
        else:
            return price2
    def name_data(self,mob,code):
        list=[]
        for i in range(len(mob)):
            list.append(mob[i].getText().replace('\u2009',' ').replace('\u20b9',''))
        #print(list)
        dict={"name":list[0],"RAM/Internal Storage":list[3],"Battery":list[4],"Camera":list[6],"Screen-Size":list[5],"Connectivity":list[1],"OS":list[8],"Best Price":list[9],"Processor":list[2],"Code":code}
        return dict
    def generate_json(self,mob):
        list=[]
        try:
            f=open("data.json","r")
            data=json.load(f)
            f.close()
        except:
            f=open("data.json","w")
            print("[]",file=f)
            data=[]
            f.close()
        with open("data.json","w") as f:
            data.append(mob)
            json.dump(data,f,indent=4)
    def organize(self):
        for i in conf["mob"]:
            mob=conf["mob"][i]
            m=self.get_data(mob)
            j=self.name_data(m,mob)
            self.generate_json(j)
        print("Json File successfull generated Do you want to Receive Price Updates on this email?(y/n)")
        res=input()
        if(res=="Y" or res=="y"):
            email=input("Enter your Email")
            conf['receiver_email'].append(email)
            data=conf
            with open("user_config.json","w") as f:
                json.dump(data,f,indent=4)
                print("We added your email successfully")
        else:
            print("Thanks for using us")
    def get_smartprix_code(self,mob_name):
        q=requests.get(f"https://www.smartprix.com/products/?q={mob_name}")
        s=bs4.BeautifulSoup(q.text,'lxml')
        sel=s.select(".f-mobiles:nth-child(1) h2 a")
        st=sel[0]['href']
        print("Smartprix Code -> ",st[st.find("mobiles/")+8:])
if __name__ == "__main__":
    if(sys.argv[1]=='-j'):
        Api().organize()
    elif(sys.argv[1]=='-gc'):
        if(sys.argv[2]==''):
            print("Enter a valid mobile name enter -h for help")
        else:
            Api().get_smartprix_code(sys.argv[2])
    elif(sys.argv[1]=='-h'):
        print(" -j -> Gets you a json file of Mobiles\n","-gc [Mobile Name]-> Gets you Smartprix Code for a particular Mobile\n","-h -> Help Menu\n")