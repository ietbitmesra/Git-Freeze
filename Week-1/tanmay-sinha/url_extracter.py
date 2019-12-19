import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
browser.get("https://www.91mobiles.com/phonefinder.php")
time.sleep(3)
grid = browser.find_element_by_xpath('/html[1]/body[1]/div[1]/div[7]/form[1]/div[1]/div[2]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/div[1]')
grid.click()
elem = browser.find_element_by_tag_name("body")

c = 0
while True:
    t = 30
    while t!=0:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.4)
        t-=1
    c+= 1
    if c > 21:
        break
    time.sleep(2)
    try:
        more = browser.find_element_by_class_name("moreresultbtn")
        more.click()
    except:
        pass
    time.sleep(2)
    
dct = {}
phones = browser.find_elements_by_class_name("hover_blue_link")

for phone in phones:
    dct[phone.text] = phone.get_attribute("href")


with open("phoneurls.json","a") as f:
    f.write(json.dumps(dct,indent=4,sort_keys=True))
