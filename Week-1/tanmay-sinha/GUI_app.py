# A simple GUI application with tkinter
# to output a JSON file containing details of mobile phone
# and set the base price and time interval.

import tkinter as tk
from tkinter import *
import json
from app import PhoneDetails

with open("phone_urls.json", "r") as myfile:
    CONTENT = json.load(myfile)
dictionary = CONTENT


def on_keyrelease(event):

    # get text from entry
    value = event.widget.get()
    value = value.strip().lower()

    # get data from TEST_LIST
    if value == '':
        data = TEST_LIST
    else:
        data = []
        for item in TEST_LIST:
            if value in item.lower():
                data.append(item)

    # update data in listbox
    listbox_update(data)


def listbox_update(data):
    # delete previous data
    listbox.delete(0, 'end')

    # sorting data
    data = sorted(data, key=str.lower)

    # put new data
    for item in data:
        listbox.insert('end', item)


def on_select(event):
    # display element selected on list
    entry1_var.set(event.widget.get(event.widget.curselection()))


def generate_file():
    # generating JSON file.
    phone_details.check_url(dictionary[f'{entry1_var.get()}'])
    window.destroy()


def start_server():
    # starting the notification server.
    print("Server has started. Press Ctrl+C inside terminal to stop server.\n")
    window1.destroy()
    phone_details.regular_price_checker(time_var.get(), base_var.get())

# =====------ MAIN -------=====

# Extracting URLs


TEST_LIST = dictionary.keys()
phone_details = PhoneDetails()

# Initial window
window = tk.Tk()
window.minsize(500, 800)
window.title("Phone Price tracker and Notifier")

label = tk.Label(window, text="Type the phone name \n\
     you want to search : (from given options only)", pady=30).pack()

entry1_var = StringVar()

entry = tk.Entry(window, width=40, textvariable=entry1_var)
entry.pack()
entry.focus()
entry.bind('<KeyRelease>', on_keyrelease)

listbox = tk.Listbox(window, width=40, height=20)
listbox.pack()
listbox.bind('<<ListboxSelect>>', on_select)
listbox_update(TEST_LIST)

button = tk.Button(window, text="Generate Json file\
", pady=10, command=generate_file)

button.pack()

label2 = tk.Label(window, text="\
    If you can't find your phone name (rare case),\n\
    go to phoneurls.json file and add your phone name and link \n\
    from 91 mobiles.com .Go to README.md for more details \
    ", pady=10).pack()

window.mainloop()
# Initial window closed.

# Start of second window.
if len(entry1_var.get()) > 0:
    window1 = tk.Tk()
    window1.minsize(500, 600)
    window1.title("Phone Price tracker and Notifier")
    base_var = IntVar()
    time_var = IntVar()
    label = tk.Label(window1, text=f"\
JSON File Created for {phone_details.phone_name}!!!\
\n\nCheck the current price in JSON File \n\
add the base price (Price at which you want to purchase)\n\
of the phone and the time interval at which you want to check for price.\n\
You will be receiving notifications at these intervals\n\
if prices decreases or is below the base price.\n\
ex-if you set 10,then you will receive notification after every 10th second\n\
if the prices decreases or is below base price.", pady=10)
    label.pack()

    base_label = tk.Label(window1, text="Base Price :(in Rs.) ").pack()
    entry1 = tk.Entry(window1, width=20, textvariable=base_var)
    entry1.pack()

    time_label = tk.Label(window1, text="\n\nTime Interval (in Seconds) : ")
    time_label.pack()
    entry2 = tk.Entry(window1, width=20, textvariable=time_var)
    entry2.pack()

    button1 = tk.Button(window1, text="Start getting Notifications!\
    ", command=start_server, pady=20)
    button1.pack()
    window1.mainloop()
    # second window closed.
