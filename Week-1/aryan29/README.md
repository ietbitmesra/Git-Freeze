# # Problem 1 - Ankit's Phone

This is a python program which can get you JSON of features of any number of mobiles in simple steps and store it in file named "data.json" and provide you with regular updates about decrease in price of mobiles mentioned

## Usage

The program initially comes with a "user_config.json" file in which you can add your custom settings to get started with using the product and make sure to add smartprix code of the product you want to keep track of after that just type this to get your json file

```python
python api.py -j
```
You can add mysmartprice code too as a second code for keeping track of best price from both of the websites
![Example UserConfig.json](https://github.com/aryan29/Git-Freeze/blob/aryan29/week1/Week-1/aryan29/images/user_config.png)
## Generating Codes from Smartprix and MySmartPrice
You can get smartprix code directly form your terminal
```python
python api.py -gc "Asus Zenfone Max Pro M1 6GB"
```
You can use their website too to get the link

As shown below:-    
Getting Link from Smartprix    
![Getting Link from Smartprix](https://github.com/aryan29/Git-Freeze/blob/aryan29/week1/Week-1/aryan29/images/mysmartprixcode.png)    

Getting Link from MySmartprice    
![Getting Link from MySmartprice](https://github.com/aryan29/Git-Freeze/blob/aryan29/week1/Week-1/aryan29/images/mysmartpricecode.png)
=======
As shown below:-
## Setting Up Server
Setup comes with a file called keeptrack.py which you can run infiniely on your system for keep receiving regular updates for linux systems just run this command
```python
nohup keeptrack.py &
```
And for Windows try
[this](https://stackoverflow.com/questions/55932829/how-to-make-sure-that-python-script-will-run-forever-on-windows)   
Remeber to restart the service each time you reboot or try adding a new cronjob or use any of the ways mentioned on [this](https://stackoverflow.com/questions/24518522/run-python-script-at-startup-in-ubuntu/25805871) link   
Windows user can make use of Microsoft Task Scheduler to do the Same    
## Features
We get you the JSON of features Any Number of Mobiles in just  a single Click    

Example JSON file Generated    
![Example JSON file Generated](https://github.com/aryan29/Git-Freeze/blob/aryan29/week1/Week-1/aryan29/images/data(json).png)
We get you the best price of mobile by making use of the websites like [Smartprix](https://www.smartprix.com/) and [MySmartPrice](https://www.mysmartprice.com/) which compares price of mobile from various stores like Amazon,Flipkart,Ebay,Shopclues and various others   
We get you the JSON of features Any Number of Mobiles in just  a single Click   

We get you the best price of mobile by making use of the websites like [https://www.smartprix.com/](https://www.smartprix.com/) and [https://www.mysmartprice.com/](https://www.mysmartprice.com/) which compares price of mobile from various stores like Amazon,Flipkart,Ebay,Shopclues and various others   

For Smartprix there is no need to get the code as well we can do that for you by a single click

We Provide you with Emails and Telegram Messages whenever there is a price decerease in your products from the time when you checked it last(We check for decrease in Price in every 3 hours)   

Example Image:-   
![Price Change Updates](https://github.com/aryan29/Git-Freeze/blob/aryan29/week1/Week-1/aryan29/images/Screenshot_20191215-224146.png)
We Provide you with Daily Emails and messages regarding whether your server is running or not if it is not Working you will not recive Email so you can switch it on   
Example Image:-   
![Server Running Update](https://github.com/aryan29/Git-Freeze/blob/aryan29/week1/Week-1/aryan29/images/Screenshot_20191215-224219.png)

We Provide you with Daily Emails and messages regarding whether your server is running or not if it is not Working you will not recive Email so you can switch it on   

## Updates
Added a smart feature to directly compare 2 phones on basis of their spec score just use
```python
python api.py -cm "Asus Zenfone Max Pro M1" "Redmi Mi A2"
```
## Contributing 
Feel Free to Contribute and for any suggestions you can mail me at <nk28agra@gmail.com>
## License
[MIT](https://choosealicense.com/licenses/mit/)
