import spec
import time
import smtplib
import ssl


class TrackPrice:
    def __init__(self):
        self.config = spec.Spec().read_config()
        self.current_price = self.getCurrentPrice()

    def getCurrentPrice(self):
        specs = spec.Spec()
        spec_all = specs.smartprix_spec()
        current_price = []
        for phone_spec in spec_all:
            current_price.append(phone_spec[1])
        return current_price

    def low_price(self):
        while True:
            new_price = self.getCurrentPrice()
            i = 0
            for old, new in zip(self.current_price, new_price):
                if (new < old):
                    self.send_email(i)
                i += 1
            time.sleep(int(self.config['Settings']['polling frequency']))

    def send_email(self, mobile):
        port = 465
        message = f"""\
        Subject: Price drop for {self.config.items('Mobile Phones')[mobile][0]}

        Current price {self.getCurrentPrice()[mobile]}"""
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(self.config['Emails']['sender email'], self.config['Emails']['sender password'])
            server.sendmail(self.config['Emails']['sender email'], self.config['Emails']['receiver email'], message.encode("utf8"))


trackprice = TrackPrice()
trackprice.low_price()
