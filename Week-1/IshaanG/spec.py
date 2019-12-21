import json
import configparser

import requests
import bs4


class Spec:
    def __init__(self):
        self.config = self.read_config()

    def smartprix_spec(self):
        spec_all = []
        for name in self.config['Mobile Phones'].items():
            mobile_name = name[0]
            list_page = requests.get(f"https://www.smartprix.com/products/?q={mobile_name}")
            soup = bs4.BeautifulSoup(list_page.content, 'lxml')
            phone_name = soup.find('div', class_='info').find('a').text
            minimum_price = soup.find('span', class_='price').text
            spec = []
            spec.append(phone_name)
            spec.append(minimum_price)
            for span in soup.find('ul', class_='pros').find_all('span'):
                spec.append(span.text.replace('\u2009', ''))
            for span in soup.find('ul', class_='cons').find_all('span'):
                spec.append(span.text.replace('\u2009', ''))
            spec_all.append(spec)
        return spec_all

    def save_json(self):
        spec_all = self.smartprix_spec()
        data_all = []
        for phone_spec in spec_all:
            data = {
                "Name": phone_spec[0],
                "Price": phone_spec[1],
                "Connectivity": phone_spec[2],
                "Processor": phone_spec[3],
                "Memory": phone_spec[4],
                "Battery": phone_spec[5],
                "Display": phone_spec[6],
                "Camera": phone_spec[7],
                "External Storage": phone_spec[8],
                "Operating System": phone_spec[9]
            }
            data_all.append(data)
        with open('data.json', 'w', encoding='utf-8') as data_file:
            json.dump(data_all, data_file, ensure_ascii=False, indent=4)

    def read_config(self):
        config = configparser.ConfigParser(allow_no_value=True)
        config.read('config.ini')
        return config


if __name__ == "__main__":
    Spec().save_json()
