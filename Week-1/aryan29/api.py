import sys
import json
import requests
import bs4
from termcolor import cprint
with open("user_config.json", "r") as f:
    CONF = json.load(f)
    if (len(CONF["mob"]) == 0):
        cprint(('Please Configure your user_config.json file and add'
                'Code of Atleast 1 mobile Phone to generate json'), 'red')
        sys.exit()


class Api:
    def get_data(self, mob):
        req1 = requests.get(f"https://www.smartprix.com/mobiles/{mob[0]}")
        soup1 = bs4.BeautifulSoup(req1.text, 'lxml')
        price1 = soup1.select("#product-price .price")[0]
        try:
            req2 = requests.get(
                f"https://www.mysmartprice.com/mobile/{mob[1]}"
                )
            soup2 = bs4.BeautifulSoup(req2.text, 'lxml')
            price2 = soup2.select(".prdct-dtl__prc-val")[0]
            price = self.get_min_price(price2, price1)
        except Exception as ex:
            price = price1
        myList = soup1.select(".has-favorite-button , .cons span , .pros span")
        myList.append(price)
        return myList

    @staticmethod
    def get_min_price(price1, price2):
        # print((price1.getText()),price2.getText()[1:])
        if ((price1.getText(), 10) < (price2.getText()[1:], 10)):
            return price1
        else:
            return price2

    @staticmethod
    def name_data(mob, code):
        myList = []
        for spec in mob:
            myList.append(spec.getText()
                          .replace('\u2009', ' ').replace('\u20b9', ''))
        # print(List)
        myDict = {"name": myList[0],
                  "RAM/Internal Storage": myList[3],
                  "Battery": myList[4],
                  "Camera": myList[6],
                  "Screen-Size": myList[5],
                  "Connectivity": myList[1],
                  "OS": myList[8],
                  "Best Price": myList[9],
                  "Processor": myList[2],
                  "Code": code}
        return myDict

    def generate_json(self, mob):
        try:
            f = open("data.json", "r")
            data = json.load(f)
            f.close()
        except Exception as ex:
            f = open("data.json", "w")
            print("[]", file=f)
            data = []
            f.close()
        with open("data.json", "w") as f:
            data.append(mob)
            json.dump(data, f, indent=4)

    def organize(self):
        for i in CONF["mob"]:
            mob = CONF["mob"][i]
            m = self.get_data(mob)
            j = self.name_data(m, mob)
            self.generate_json(j)
        cprint(("Json File successfull generated Do you want to "
                "Receive Price Updates on this email?(y/n)"), 'yellow')
        res = input()
        if (res in ("Y", "y")):
            email = input("Enter your Email")
            CONF['receiver_email'].append(email)
            data = CONF
            with open("user_config.json", "w") as f:
                json.dump(data, f, indent=4)
                cprint("We added your email successfully", 'green')
        else:
            cprint("Thanks for using us", 'magenta')

    def get_smartprix_code(self, mob_name):
        # print(mob_name)
        req = requests.get(f"https://www.smartprix.com/products/?q={mob_name}")
        soup = bs4.BeautifulSoup(req.text, 'lxml')
        sel = soup.select(".f-mobiles:nth-child(1) h2 a")
        st = sel[0]['href']
        x = st[st.find("mobiles/") + 8:]
        cprint(f"Smartprix Code -> {x}", 'magenta')

    def smart_compare(self, mob1, mob2):
        req1 = requests.get(f"https://www.smartprix.com/products/?q={mob1}")
        req2 = requests.get(f"https://www.smartprix.com/products/?q={mob2}")
        soup1 = bs4.BeautifulSoup(req1.text, 'lxml')
        sel1 = soup1.select(".f-mobiles:nth-child(1) .score-val")[0]
        soup2 = bs4.BeautifulSoup(req2.text, 'lxml')
        sel2 = soup2.select(".f-mobiles:nth-child(1) .score-val")[0]
        # print(sel2,sel1)
        if (int(sel2.text) > int(sel1.text)):
            mob1, mob2 = mob2, mob1
        cprint(f"{mob1} is better than {mob2}", 'cyan')


if __name__ == "__main__":
    if (len(sys.argv) > 1):
        if (sys.argv[1] == '-j'):
            Api().organize()
        elif (sys.argv[1] == '-gc'):
            if (len(sys.argv) != 3):
                cprint("Enter a valid mobile name enter -h for help", 'cyan')
            else:
                Api().get_smartprix_code(sys.argv[2])
        elif(sys.argv[1] == '-cm'):
            if (len(sys.argv) != 4):
                cprint("Enter a valid mobile name enter -h for help", 'cyan')
            else:
                Api().smart_compare(sys.argv[2], sys.argv[3])
        elif (sys.argv[1] == '-h'):
            HELPMENU = ('-j -> GetsyouajsonfileofMobiles\n'
                        '-gc [Mobile Name]-> Gets you Smartprix Code'
                        'for a Mobile\n'
                        '-cm [Mobile 1] [Mobie 2] to compare phones on basis '
                        'of their spec score\n'
                        '-h -> Help Menu\n')
            cprint(HELPMENU, 'cyan')
        else:
            cprint("Enter a valid mobile name enter -h for help", 'cyan')
    else:
        cprint("Invalid Command -h for help", 'red')
