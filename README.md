# UdemyEnrollEverywhere
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![GitHub stars](https://img.shields.io/github/stars/keethesh/UdemyEnrollEverywhere?style=for-the-badge)](https://github.com/keethesh/UdemyEnrollEverywhere/stargazers)

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/T6T81UCB0)

Want to brag about having a lot of Udemy courses? Then UdemyEnrollEverywhere is what you need! It searches for coupons, and adds the corresponding courses to your account!

#### Please answer the poll! Else, at night, when I'm not able to sleep, I'll ask myself if my script is working for everyone or not...
[![](https://api.gh-polls.com/poll/01EB98NEYFACZVT4YWZRG4A8EJ/Working%20great!%20%F0%9F%91%8D)](https://api.gh-polls.com/poll/01EB98NEYFACZVT4YWZRG4A8EJ/Working%20great!%20%F0%9F%91%8D/vote)
[![](https://api.gh-polls.com/poll/01EB98NEYFACZVT4YWZRG4A8EJ/I%20have%20an%20error%F0%9F%98%AD%20(If%20you%20vote%20for%20this%2C%20please%20open%20an%20issue))](https://api.gh-polls.com/poll/01EB98NEYFACZVT4YWZRG4A8EJ/I%20have%20an%20error%F0%9F%98%AD%20(If%20you%20vote%20for%20this%2C%20please%20open%20an%20issue)/vote)

## Installation
### The requirements
- Python 3.6+
- Chrome
- A Udemy account

### Installing the modules
To install needed modules, do 

`pip3 install -r requirements.txt`

If any error pops up, try

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
5. Then, note the values of `access_token` and `client_id`

That's it!

## Todo
- Scrape coupons from more websites
    - [x] Learnviral
    - [ ] Discudemy
    - [ ] Real.discount
    - [ ] allmycourses

    If you know such websites, that are not using Javascript preferably, please open an issue and tell me about it!

- [ ] Make it use Firefox if Chrome cannot be used
- [ ] Add a system to get and keep track of your courses, so that it won't try adding them again

- Add more things to the Todo section of my README

## Footnote
[AmmeySaini](https://github.com/AmmeySaini) did [a very interesting, similar project](https://github.com/AmmeySaini/Udemy-Paid-Courses-Grabber), only using requests. I'd like to say that no idea(except using cookies to login) is taken from him. I even saw that we were both using browser_cookie3 to get the cookies from the browsers! 

This project idea was given to me in an issue of my other Udemy project, [UdemyCourseGrabber](https://github.com/keethesh/UdemyCourseGrabber).
