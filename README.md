
UdemyEnrollEverywhere

￼

￼

￼

Want to brag about having a lot of Udemy courses? Then UdemyEnrollEverywhere is what you need! It searches for coupons, and adds the corresponding courses to your account!

Please answer the poll! Else, at night, when I'm not able to sleep, I'll ask myself if my script is working for everyone or not...

￼

￼

Installation

The requirements
• Python 3
• Chrome
• A Udemy account

Installing the modules

To install needed modules, do

 pip3 install -r requirements.txt 

If any error appears, try

 pip install -r requirements.txt 

Usage

Automatic way

If you already are logged in on Firefox or Chrome, simply do

 python3 main.py 

Manual way

If you are not logged in, or if you want to login manually for whatever reason, do

 python3 main.py --client_id="<Your client ID>" --access_token="<Your access token>" 

Getting your cookies

Ask your grandma to bake them or bake them yourself
1. Visit Udemy and login if you're not already logged-in
2. Open Developer Tools ( F12 or Ctrl-Shift-I ). If on Chrome, after opening DevTools , go to the Application tab
3. Open the dropdown of the Cookies option
4. Click on the Udemy landing page URL( https://www.udemy.com for those not following)
5. Then, note the values of access_token and client_id 

That's it!

Todo
• Scrape coupons from more websites
• [x] Learnviral
• [ ] Discudemy
• [ ] Real.discount
• [ ] allmycourses

If you know such websites, that are not using Javascript preferably, please open an issue and tell me about it!
• Add more things to the Todo section of my README

Footnote

AmmeySaini did a very interesting, similar project , only using requests. I'd like to say that no idea(except using cookies to login) is taken from him. I even saw that we were both using browser_cookie3 to get the cookies from the browsers!

This project idea was given to me by chaoscreater , in issue#10 of my other Udemy project, UdemyCourseGrabber .