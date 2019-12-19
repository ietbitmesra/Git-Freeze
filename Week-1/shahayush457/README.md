# Scrapping E-commerce website

## Basic usage

The basic use of this app is to scrape the price and all the features of Apple Iphone 11
and OnePlus 7t Pro from an E-commerce website(I have used Flipkart, one can use any) and store it in a file in JSON format.
Run the following command to get the features of the phones.
```
python3 index.py
```

## Sending E-mail feature

There is a feature to send a mail to a list of users if there is a drop in price of any of the phones.
You need to add some details to the configuration file for sending the mail like the host address of 
the sender's service provider, port of the host, email of the sender, password of the sender's email,
list of users to whom the email is to be sent. I have gitignored the original config file but added a
sample config file with the format and the fields used in the original file.
To use this feature run the following command.
```
python3 server.py
```
If you want to run your server infinitely(even when you exit your terminal or reboot into the system),
then run the following command in your linux terminal.
```
nohup python3 server.py &
```
It will run your server in the background infinitely.
To stop the server first find the process id(PID) of the process running using the pgrep command.
Then kill the process.
```
pgrep -a python3
kill <PID>
```

## Contributions

Will be happy to see any kind of improvements.Contributions are always welcomed. Just make a pull request.

## Author

##### [Ayush Shah](https://github.com/shahayush457)
