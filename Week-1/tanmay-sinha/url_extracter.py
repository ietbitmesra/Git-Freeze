# program for scraping the phone names and their URLS.
# This program is not related with the functioning of main program

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
browser.get("https://www.91mobiles.com/phonefinder.php")
time.sleep(3)
grid = browser.find_element_by_xpath('/html[1]/body[1]/div[1]/div[7]/form[1]/div[1]/div[2]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/div[1]')
grid.click()
elem = browser.find_element_by_tag_name("body")

count = 0
while True:
    times = 30
    while times != 0:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.4)
        times -= 1
    count += 1
    if count > 21:
        break
    time.sleep(2)
    try:
        more = browser.find_element_by_class_name("moreresultbtn")
        more.click()
    except NameError:
        print("Not found the button!!")
    time.sleep(2)
dictionary = {}
phones = browser.find_elements_by_class_name("hover_blue_link")

for phone in phones:
    dictionary[phone.text] = phone.get_attribute("href")


with open("phoneurls.json", "a") as myfile:
    myfile.write(json.dumps(dictionary, indent=4, sort_keys=True))
