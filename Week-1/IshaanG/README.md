# Problem 1 - Ankit's Phone

Here is my solution to the first task of git freeze. The spec.py script generates a JSON with specifications of any Mobile Phone given in the config.ini file. Another script trackprice.py provides alerts for price drops via email. All configuration in done directly through the config.ini file.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

The scripts are written in python and require python 3. Dependencies are provided in requirements.txt which can be simply install by:


    $ pip install -r requirements.txt


To avoid having to give root permission it is advised to install in a virtual environment or with the --user flag.

### Usage

Modify the config.ini file as desired taking care of the section headers.


    # List the mobiles phones to get the information and track prices
    [Mobile Phones]
    iPhone 11
    OnePlus 7T Pro
    # Provide email for price drop alerts
    [Emails]
    sender email = test@gmail.com # You need to enable permission for less secure apps for the sender gmail account
    sender password = abc123
    receiver email = pqr@123.com
    # Other settings
    [Settings]
    polling frequency = 60 # Frequency in seconds to check for the lowest prices 


Run the spec.py file to generate the JSON in data.json.


    $ python spec.py


To get notified on price drops configure the sender email and enable permission for less secure apps. The program uses SSL to keep your credentials secure over the network, however, note that the password will be in plain text in config.ini.


    $ python trackprice.py


## Built With

* [Python](https://www.python.org/) - The programming language used
* [Requests](https://requests.readthedocs.io/en/master/) - HTTP library for Python
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Used for parsing HTML pages

## Contributing

Feel free to make a pull request or email me at <ishaang12@gmail.com>.

## Author

* **Ishaan Gupta** - [IshaanG](https://github.com/IshaanG)