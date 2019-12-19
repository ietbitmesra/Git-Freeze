#How to run?
--------------
To run the code simply locate the directory Major2001 in command line and type in the command node app.js

#Software/Tools used
---------------------
Used Nodejs as the base language
Used npm packages : 1. cheerio
                    2. nodemailer
                    3. request

#Working of the project
-----------------------
The project declares an object by the name of prices.The request package of npm allows to make an request to amazon's website for the required webpage. It then gets cost of Iphone 11(64gb variant) and OnePlus 7T Pro from Amazon's website (by selecting required html element with designated id using the cheerio package) after every 6 hours and compares it with the original price. If there is a price drop, It mails at xyz@gmail.com using the nodemailer package                    