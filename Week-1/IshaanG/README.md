Usage:
Add the mobile phone names to the config.ini file under the "Mobile Phones" section.
pip install -r requirements.txt
python spec.py

Made using python and depends on requests, bs4, and configparser.

It gets mobile phone specifications from mysmartprix and also gets the lowest price for the model. Saves a JSON file with the details.

To get price drop alerts fill in the email credentials in config.ini.
Run the trackprice.py script