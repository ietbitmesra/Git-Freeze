# About :

A python flask web service allowing interaction with two web browsers : Google Chrome and Mozilla Firefox.

Supports <strong>Linux OS</strong> and <strong>Python 3.6</strong> and above.
Successfully tested on <b>Ubuntu 18.04.3 LTS</b> .

## How to use :

1. Install dependencies by using
```python
pip install -r requirements.txt
```
2. Run the flask server .
3. Open any browser and try following endpoints :


<br>
NOTE:

1. < browser > = chrome/firefox
2. < url > = Any valid URL like: http://www.medium.com

Example usage of endpoints: 
> `http://<server>/start?browser=<browser>&url=<url>`
Start the desired browser and open the URL in the same browser instance

> `http://<server>/geturl?browser=<browser>` 
Get the current active tab URL for the given browser

> `http://<server>/stop?browser=<browser>` 
Stop the given browser if it is running

> `http://<server>/cleanup?browser=<browser>` 
Clean up the browsing session for the given browser if has been stopped

<b>WARNING : Be careful with cleanup as all the data from the default user profile would be deleted!!</b>

## contributing

Feel free to contact me at <alokratn001@gmail.com> for any suggestions and improvements.