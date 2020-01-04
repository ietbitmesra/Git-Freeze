# Problem Statement
Ankit recently came 1st at a hackathon and now he wants to buy a new phone with the prize money he received. He is confused between iPhone 11 and OnePlus 7T Pro. Since he is very busy preparing for his exams, he needs your help. Give him a list of features comparing the 2 phones.

# My Solution
I have created a Simple Python Program that fetches the basic feature namely Price, Operating System, RAM Capacity, Camera Quality, Screen Size, Connectivity Features, Internal Storage Capacity and Processor pf both the phones, and stores it in both - a "JSON" file and a "CSV" File. Also, it contains the optional fetaures of checking periodically for price changes(in this case, every half an hour, if the program keeps running) and if there is deduction in prices, notification is sent to the person through E-Mails.

# How It Run?
To run the program, open the "Sample1.py" file in any Python IDE, preferably PyCharm. Then set the Python Interpreter and Script to "Week-1\rondon1947\venv\Scripts". Then run the Sample1.py file. A "data.json" file and a "index.csv" file are created in the same location as Sample1.py, both of which contain the same data. The CSV file, which can be opened in Spreadsheet Applications like MS Excel, compares the corresponding data of both the Smartphones.

# What Softwares I used?
To make the whole project, I used the PyCharm IDE by Jetbrains and the new Windows Powershell Terminal. To perform Web Scraping I used the BeautifulSoup library and to send the E-Mails, I used the "smtplib" library.