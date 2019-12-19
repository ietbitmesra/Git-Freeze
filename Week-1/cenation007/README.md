# # Problem 1- Ankit's Phone

The application accepts the name of two phones as the input from user. It compares the features of the two phones and gives the output in the form of JSON file named as 'compare2.json'. It also checks for the drop in price of any of the two phones and provides the notification by email. You can compare any two mobile phones of you choice.

## Getting Started

You can clone the project on you local machine. The main file is " new.js " which contains the code. 

## Prerequisites

You need to install the packages mentioned in the " package.json " file in the dependencies by running the following command in console:

```
   npm install 
```
## Usage 

After installing the packages, you need to run the command the command 
```
node new.js
```
It'll ask you to provide the details of the smartphones you want to compare...eg.
```
For phone 1
Brand:
Model:
For phone 2
Brand:
Model:
```
You need to provide the details without any extra spaces and in proper format. Don't worry about the cases...eg;
```
For phone 1
Brand: samsung
Model: galaxy j7 prime
For phone 2
Brand: apple
Model: iphone 7 plus
```
The output will be provided in a file named " compare2.json".

The price of the phones are tracked after every 30 seconds.
For tracking prices you need to provide the emails of the sender ans the receivers in the " new.js " file.eg;
```
user: 'abc@gmail.com',//sender's mail
pass: 'password'     //sender's password
```
```
from: 'abc@gmail.com',
to: ['xyz@gmail.com',
     'pqr@gmail.com']
```
You can generate a new password by turning on the 2-step verification and then go to security->app passwords.
You can use this generated password.

## Built with

- Javascript
- Node.js
- Cheerio.js
- Request-Promise
- Nodemailer
- Prompt-sync
- fs

## Author
> Ayush Pandey
