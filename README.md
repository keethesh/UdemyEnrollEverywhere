# UdemyEnrollEverywhere
Want to brag about having a lot of Udemy courses? Then UdemyEnrollEverywhere is what you need! It searches for coupons, and adds the corresponding courses to your account!

## Installation
### The requirements
- Python 3
- Chrome for Selenium
- A Udemy account

### Installing the modules
To install needed modules, do 

`pip3 install -r requirements.txt`

If any error appears, try

`pip install -r requirements.txt`

## Usage
### Automatic way
If you already are logged in on Firefox or Chrome, simply do

`python3 main.py`

### Manual way
If you are not logged in, or if you want to login manually for whatever reason, do

`python3 main.py --client_id="<Your client ID>" --access_token="<Your access token>"`

## Getting your cookies
###### Ask your grandma to bake them or [bake them yourself](https://joyfoodsunshine.com/the-most-amazing-chocolate-chip-cookies/)
1. Visit [Udemy](https://www.udemy.com/) and login if you're not already logged-in
2. Open _Developer Tools_(`F12` or `Ctrl-Shift-I`). 
If on Chrome, after opening _DevTools_, go to the `Application` tab
3. Open the dropdown of the `Cookies` option
4. Click on the Udemy landing page URL(https://www.udemy.com for those not following)
5. Then, copy the value of `access_token` and `client_id`

That's it!

### Last note
[AmmeySaini](https://github.com/AmmeySaini) did [a very interesting, similar project](https://github.com/AmmeySaini/Udemy-Paid-Courses-Grabber), only using requests. I'd like to say that no idea(except using cookies to login) is taken from him. I even saw that we were both using browser_cookie3 to get the cookies from the browsers! 

This project idea was given to me by [chaoscreater](https://github.com/chaoscreater), in [issue#10](https://github.com/keethesh/UdemyCourseGrabber/issues/10) of my other Udemy project, [UdemyCourseGrabber](https://github.com/keethesh/UdemyCourseGrabber).

