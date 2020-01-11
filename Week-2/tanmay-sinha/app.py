# Flask app to control browser.
from flask import Flask
from flask import request
from flask import Markup
import os
import sys
import json
import lz4.block

app = Flask(__name__)

# To open any url using browser.
@app.route("/start")
def openbrowser():
    browser_name = request.args.get('browser')
    url = request.args.get('url')
    if browser_name == 'chrome':
        browser_name = 'google-chrome'

    os.system(f"{browser_name} '{url}'")
    return Markup(f"<h1>Started {url} on\
    {browser_name.capitalize()}</h1>")

# To close any browser.
@app.route("/stop")
def close():
    browser_name = request.args.get('browser')
    os.system(f"killall {browser_name}")
    return Markup(f"Closed {browser_name.capitalize()}")

# To clear all the data from the browser of default user.
@app.route("/cleanup")
def clean():
    browser_name = request.args.get('browser')
    if(browser_name == 'firefox'):
        os.system("rm -rf ~/.mozilla/firefox*/*.default/")
        os.system("rm ~/.mozilla/firefox/profiles.ini")
    elif browser_name == 'chrome':
        os.system("rm -rf ~/.config/google-chrome/Default/")
    return Markup("<h1>Deleted Everything!!!</h1>")

# To get the active URL.
@app.route("/geturl")
def urls():
    browser_name = request.args.get('browser')
    current_urls = ''
    if browser_name == 'firefox':
        file_path = os.popen(
            "(find ~/.mozilla/firefox*/*.default/sessionstore-backups/recovery.jsonlz4)")\
            .read()
        file_name = open(str(file_path[0:-1]), "rb")
        openfile = file_name.read(8)
        count = 1
        json_data = json.loads(lz4.block.decompress(
            file_name.read()).decode("utf-8"))
        file_name.close()
        for window in json_data.get("windows"):
            for tab in window.get("tabs"):
                item = int(tab.get("index"))-1
                current_url = tab.get("entries")[item].get("url")
                current_urls += f"{count}. <a href='{current_url}'>{current_url}</a><br>"
                count += 1
    elif browser_name == 'chrome':
        current_urls += os.popen(
            ("strings ~/'.config/google-chrome/Default/Current Session' | 'grep' -E '^https?://'"
             )).read()
        current_urls = current_urls[current_urls.rfind("http"):-1]
        current_urls = f"<a href={current_urls}>{current_urls}</a>"
    return Markup(f"The active url :<br><br>{current_urls}")

#======MAIN======#
if __name__ == "__main__":
    app.run(debug=True)
