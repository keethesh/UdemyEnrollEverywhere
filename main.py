import argparse
import asyncio
import atexit
import json
import sys

import browser_cookie3
import helium
from colorama import Fore
from fake_useragent import UserAgent
from lxml import html
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, \
    ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options as chromeOpts

import scrapers

tick = u"\u2713"
warning = u"\u26A0"
udemy_domain = "www.udemy.com"
ua = UserAgent()
enroll_label = "Enroll now"
enroll_xpath = "//button[@data-purpose='buy-this-course-button']/span"
parser = argparse.ArgumentParser()

if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
else:
    loop = asyncio.SelectorEventLoop()
asyncio.set_event_loop(loop)


class Error(Exception):
    pass


class InvalidCookiesException(Error):
    def __init__(self, message="The cookies are invalid, please visit Udemy and login using Firefox or Chrome, "
                               "and relaunch the script. If you set them by command-line arguments, please "
                               "check if they're valid."):
        self.message = message
        super().__init__(self.message)


class NoCookiesException(Error):
    def __init__(self, message="No cookies found, please visit Udemy and login using Firefox or Chrome, "
                               "and relaunch the script. You can also set these by running the script "
                               "with the --token and --id flags"):
        self.message = message
        super().__init__(self.message)


def get_user_info():
    try:
        helium.go_to("https://www.udemy.com/user/edit-profile/")
        user_information = browser.execute_script('return UD.me')
        mail = user_information["email"]
        display_name = user_information["display_name"]
        account_id = user_information['id']
        return mail, display_name, account_id
    except TimeoutException:
        return None


def get_cookies():
    try:
        udemy_cookies = browser_cookie3.load(domain_name=udemy_domain)._cookies[udemy_domain]["/"]
        return udemy_cookies["access_token"].value, udemy_cookies["client_id"].value

    except KeyError:
        raise NoCookiesException()


def get_free_courses():
    return loop.run_until_complete(scrapers.get_courses())


def start_and_login():
    while True:
        opts = chromeOpts()
        opts.add_argument(f"user-agent={ua.random}")
        prefs = {'profile.managed_default_content_settings.images': 2}  # Disallow images from loading
        opts.add_experimental_option("prefs", prefs)
        driver = helium.start_chrome("https://www.udemy.com/random_page_that_does_not_exist/",
                                     headless=False,
                                     options=opts)
        driver.add_cookie(
            {'name': 'client_id', 'value': client_id, 'domain': udemy_domain})
        driver.add_cookie(
            {'name': 'access_token', 'value': access_token, 'domain': udemy_domain})
        helium.go_to("https://www.udemy.com/?persist_locale=&locale=en_US")
        if 'upgrade-your-browser' in driver.current_url:
            driver.quit()
        else:
            break
    try:
        helium.wait_until(helium.Button('Log in').exists, timeout_secs=3.5)
        helium.kill_browser()
        raise InvalidCookiesException()
    except TimeoutException:
        return driver


def is_enroll_possible():
    doc = html.fromstring(browser.page_source)
    course_info = doc.xpath("//div[@class='ud-component--course-landing-page-udlite--price-text']")
    if not course_info:
        return "you already own this course"

    try:
        course_info = json.loads(course_info[0].attrib["data-component-props"])
        if course_info["pricing_result"]["price"]["amount"] != 0.0:
            return "the coupon does not provide enough discount or the coupon is invalid"
        else:
            return True
    except KeyError:
        return "of an unknown reason"


parser.add_argument('--client_id', default=False, help="This is your client ID")
parser.add_argument('--access_token', default=False, help="This is your access token")
args = parser.parse_args()
# The following two lines are there because Pycharm was bothering me. But apart from that, they exist for no reason.
client_id = args.client_id
access_token = args.access_token

if not client_id or not access_token:
    print(f"{Fore.YELLOW}[!] No cookies provided, trying to get them automatically...")
    access_token, client_id = get_cookies()
    print(f"{Fore.GREEN}[{tick}] Successfully extracted needed cookies from your browsers!")

print(f"{Fore.YELLOW}[!] Scraping courses from {len(scrapers.scrapers_list)} websites...")
courses = get_free_courses()
print(f"{Fore.GREEN}[{tick}] Scraped {len(courses)} courses!")

browser = start_and_login()
user_info = get_user_info()
if user_info is None:
    print(f"{Fore.GREEN}[{tick}] Successfully logged in!\n")
else:
    print(f"{Fore.GREEN}[{tick}] Successfully logged in!")
    print(f"{Fore.YELLOW}[!] Email: {user_info[0]}")
    print(f"{Fore.YELLOW}[!] Display Name: {user_info[1]}\n")
atexit.register(browser.quit)

success_counter = 0
for url in courses:
    helium.go_to(url)
    if helium.S("//span[contains(text(),'Sorry, this course is no longer accepting enrollme')]").exists():
        print(f"{Fore.YELLOW}[!] Cannot enroll in the course at {url} because the course is not "
              f"accepting enrollments anymore")
        continue
    elif helium.S("//span[contains(text(), ' is no longer available.')]").exists():
        print(f"{Fore.YELLOW}[!] The course at {url} does not exist anymore")
        continue
    elif helium.S("//h1[@class='error__greeting']").exists():
        print(f"{Fore.YELLOW}[!] The {url} does not exist")
        continue
    try:
        helium.wait_until(helium.S("//h1[@data-purpose='lead-title']").exists)
        course_name = helium.S("//h1[@data-purpose='lead-title']").web_element.text
    except TimeoutException:
        continue

    enroll_test = is_enroll_possible()
    if enroll_test is not True:
        print(f"{Fore.YELLOW}[!] Cannot enroll in '{course_name}' because {enroll_test}")
        continue

    try:
        helium.wait_until(helium.Button(enroll_label).exists)
        helium.click(helium.Button(enroll_label))
    except (NoSuchElementException, ElementNotInteractableException,
            ElementClickInterceptedException, TimeoutException) as e:
        continue
    try:
        helium.wait_until(lambda: "checkout" in browser.current_url)
        helium.click(helium.Button(enroll_label))
        helium.wait_until(lambda: "success" in browser.current_url)
        print(f"{Fore.GREEN}[{tick}] Successfully enrolled in '{course_name}'")
        success_counter += 1
        continue
    except TimeoutException as e:
        print(f"{Fore.RED}[{warning}] Unknown error, couldn't enroll in '{course_name}'")

print(f"\n{Fore.GREEN}[{tick}] All courses have been checked!")

success_rate = success_counter / len(courses)
if success_counter == 0:
    print(f"{Fore.RED}[!] None of the courses have been added to your account out of {len(courses)}")

if success_rate >= 0.5:
    print(f"{Fore.GREEN}[{tick}] Added {success_counter} courses to your account out of {len(courses)}")

else:
    print(f"{Fore.RED}[{tick}] Added only {success_counter} courses to your account out of {len(courses)}")

helium.kill_browser()
