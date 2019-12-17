
### Setting Up The Application

For installing the depenencies used in the project open the terminal and type the following command 
```
	npm install
```

### Running The Application

The main script is index.js. For running the application you need to provide the names of the two smartphones you want to compare as arguments, the format of the command should be

```
	node index.js smartphone1 smartphone2
```

For example if you want to compare Samsung Galaxy Note 10 and Xiaomi Redmi K20 Pro then you need to type the following command

```
	node index.js Samsung-Galaxy-Note-10 Xiaomi-Redmi-K20-Pro
```

If the two phones you want to compare are Apple iPhone 11 and OnePlus 7T Pro then the command should be

```
    node index.js Apple-iPhone-11 OnePlus-7T-Pro
```

Make sure that every word in the smartphone's name is seperated by a `-` ( hyphen ) instead of a space and also that every word is in the appropriate case (upper or lower).


### Tech Used

 - Javascript
 - Node.js
 - Cheerio.js
 - Request-Promise
 - Nodemailer


### What It Does?

The only inputs the application takes from the user are the names of the smartphones the user wants to compare. The application scrapes data about the specifications of the two phones from GadgetsNow and stores it into **specifications.json**. Then it checks for price drops regularly after every 2 minutes. If there is a drop in price then it sends an email to the user about the price drop which also contains the url to the website. The application is not limited to any particular smartphone, the user can select any two smartphone of their choice.
 
 
