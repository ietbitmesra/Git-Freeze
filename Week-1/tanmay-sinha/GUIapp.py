import tkinter as tk
import json
from app import PhoneDetails
from tkinter import *

with open("phoneurls.json","r") as f:
    cont = json.load(f)

dct = cont
def on_keyrelease(event):

    # get text from entry
    value = event.widget.get()
    value = value.strip().lower()

    # get data from test_list
    if value == '':
        data = test_list
    else:
        data = []
        for item in test_list:
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
    phone_details.check_url(dct[f'{entry1_var.get()}'])
    root.destroy()


def start_server():
    print("Server has started . Press Ctrl+C to stop server.")
    root1.destroy()
    phone_details.regular_price_checker(time_var.get(),base_var.get())
    

# --- main ---

# Extracting URLs
test_list = dct.keys()

phone_details = PhoneDetails()
root = tk.Tk()

# Initial window
root.minsize(500,800)
root.title("Phone Price tracker and Notifier")


label = tk.Label(root,text= "Type the phone name \n\
     you want to search : (from given options only)",pady = 30).pack()

entry1_var = StringVar()

entry = tk.Entry(root, width = 40, textvariable = entry1_var)
entry.pack()
entry.focus()
entry.bind('<KeyRelease>', on_keyrelease)

listbox = tk.Listbox(root,width = 40,height = 20)
listbox.pack()
listbox.bind('<<ListboxSelect>>', on_select)
listbox_update(test_list)

button = Button(root, text="Generate Json file",pady=10,command = generate_file)
button.pack()

label2 = tk.Label(root ,text = " If you can't find your phone name (rare case),\n\
    go to phoneurls.json file and add your phone name and link \n\
        from 91 mobiles.com .Go to README.md for more details ",\
            pady=10).pack()

root.mainloop()


if len(entry1_var.get())>0:
    #Start of second window.
        
    root1 = Tk()
    root1.minsize(500,500)
    root1.title("Phone Price tracker and Notifier")
    base_var = IntVar()
    time_var = IntVar()
    label = tk.Label(root1,text = "JSON File Created!!!\n\n\
        Check the current price in JSON File \n\
        add the base price (Price at which you want to purchase)\n\
        of the phone and the time interval at which you want to check for price.\n\
        You will be receiving notifications at these intervals\n\
        if prices decreases or is below the base price.",pady =10)
    label.pack()

    base_label = tk.Label(root1,text = "Base Price :(in Rs.) ").pack()
    entry1 = tk.Entry(root1, width = 20, textvariable = base_var)
    entry1.pack()

    time_label = tk.Label(root1,text="\n\nTime Interval (in Seconds) : ").pack()
    entry2 = tk.Entry(root1,width = 20,textvariable = time_var)
    entry2.pack()

    button1 = Button(root1,text = "Start getting Notifications!",\
    command = start_server,pady = 20)
    button1.pack()

    root1.mainloop()