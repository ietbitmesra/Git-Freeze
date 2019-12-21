# Problem 2 – Busy  Sanskar 
Sanskar is an awesome web developer and loves creating great web services. One day one of his friends challenged him to build a web service that would allow his friend to interact with the web browsers on Sanskar’s system. But Sanskar is busy building the website for the upcoming cultural fest in his college. Sanskar has asked you to help him win the challenge.

## Basic Requirements:

You have to implement a simple stateless web service that allows one to interact with the two web browsers: Google Chrome and Mozilla Firefox.

The service should support following endpoints:

| Method | Endpoint | Parameter(s) | Description | Should handle|
|--------| ---------|--------------|-------------|--------------|
|GET | /start| browser, url| Starts the < browser > which has the < url > open inside it.| Chrome and Firefox|
|GET|/stop|browser|Kills the < browser >|Chrome and Firefox
|GET|/cleanup|browser|Deletes all the browser session information such as history, cache, cookies, downloads, saved passwords, etc for < browser >|Chrome or Firefox
|GET|/geturl|browser|Returns the currently active tab’s URL. Assume < browser > has exactly one window and one tab open.|Chrome and Firefox|


NOTE:   
1.  < browser > = chrome/firefox
2.  < url > = Any valid URL like: http://www.medium.com

Example usage of endpoints: 
> `http://<server>/start?browser=<browser>&url=<url>`
should start the desired browser and open the URL in the same browser instance

> `http://<server>/geturl?browser=<browser>` 
should get the current active tab URL for the given browser

> `http://<server>/stop?browser=<browser>` 
should stop the given browser if it is running

> `http://<server>/cleanup?browser=<browser>` 
should clean up the browsing session for the given browser if has been stopped

## Points to note:
- Browsers have to be started/stopped on the server's end. i.e. if the server is running on machine A and a request to /start is made from machine B, the browser should start on machine A. For testing you may assume machines A and B to be the same, i.e. your own machine.
- Any tool or library that relies on the Selenium (WebDriver) protocol should not be a dependency of the service.
- Service does not need to be OS independent, i.e. if you have a Windows machine, it is expected that the service runs properly in Windows but it is not expected that it runs properly across all operating systems.
- There are no language restrictions.



## Resources:
- IET Explains: [Building an API in Node.js](https://www.youtube.com/playlist?list=PLSQotcOyCW5y7nYGr-NRedbtK5ePgKq7m)
- [Multi-process Browser Architecture](https://helgeklein.com/blog/2019/01/modern-multi-process-browser-architecture/)
- [How browsers work?](https://www.html5rocks.com/en/tutorials/internals/howbrowserswork/)
