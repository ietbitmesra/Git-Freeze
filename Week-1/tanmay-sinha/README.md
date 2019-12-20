## About

This is a basic python Tkinter program where user can type the phone name and then select phone from the suggestions(dropdown). It includes almost 1500 phones from which user can select the required phone. It appends phone details to the file "phone_details.json" every time user select a new phone.
<br>
<br>
User will also receive desktop and mobile notifications and also E-mails regarding price drops and if price drops below the base price, at given time intervals. User can set the base price ( price at which user wants to purchase the phone ) and time interval at which user wants to check the price.

## Quick Setup

1. Tkinter comes pre-installed with python. In case you have any problem using Tkinter , refer [this](https://stackoverflow.com/a/11690261).
2. Install requirements by using
```python 
pip install -r requirements.txt
```
3. For setting up notify-run services ( desktop-mobile notifications ),
refer this [Quick setup](https://notify.run/). User have to make his channel on the given link and the devices where he wants to receive notifications .

4. Open "congif.json" file and update the email credentials . You have to allow less secure apps on your sender's Gmail account to send emails. Refer [this](https://hotter.io/docs/email-accounts/secure-app-gmail/).

You are good to go.

## How to Use?

1. Run the python program GUIapp in the terminal. A window will appear like this.
2. Type anything related to your phone name as shown.
3. Select your phone from the given options and click on "Generate JSON" button . The phone details will be appended to the "phone_details.json" file .<br><br>
If you don't find your phone, go to [91Mobiles](https://www.91mobiles.com/), find your phone and its 91Mobiles link and add it to "phoneurls.json" file in JSON format anywhere.

4. Now a window will appear asking for Base price and time intervals . Enter details and click on "Start Server" button. You can close the server using Ctrl+C if you don't want to receive further notifications .

Notification Images :-

Email Images :-

## Contributing

You can add features like multiple phones price , specs comparision etc .
Feel free to contact me at <alokratn001@gmail.com> for any suggestions .