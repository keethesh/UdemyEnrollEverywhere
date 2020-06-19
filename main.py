import argparse
import asyncio
from itertools import chain

import browser_cookie3
from colorama import init, Fore
from fake_useragent import UserAgent
from pyderman import chrome, install
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException, \
    NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as chromeOpts
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from scrapers import *

tick = u"\u2713"
warning = u"\u26A0"


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


def get_cookies():
    try:
        udemy_cookies = browser_cookie3.load(domain_name='www.udemy.com')._cookies["www.udemy.com"]["/"]
        return udemy_cookies["access_token"].value, udemy_cookies["client_id"].value

    except KeyError:
        raise NoCookiesException()


def get_free_courses():
    all_courses = loop.run_until_complete(asyncio.gather(*[asyncio.ensure_future(func) for func in site_list]))
    return list(chain.from_iterable(all_courses))


def start_browser():
    opts = chromeOpts()
    opts.add_argument("--headless")
    opts.add_argument(f"user-agent={ua.random}")
    prefs = {'profile.managed_default_content_settings.images': 2}  # Disallow images from loading
    opts.add_experimental_option("prefs", prefs)
    try:
        driver = Chrome(options=opts)
    except WebDriverException:
        print("Chromedriver not detected, it will now be downloaded...")
        install(browser=chrome, file_directory='./', filename="chromedriver.exe")
        driver = Chrome(options=opts)
    return driver


def enroll_possible():
    try:
        WebDriverWait(browser, 1.25).until(EC.presence_of_element_located((
            By.XPATH, "//span[contains(text(),'Free')]")))
        return True

    except TimeoutException:
        if len(browser.find_elements_by_xpath("//button[contains(text(),'Buy now')]")) == 1:
            reason = "the coupon does not provide enough discount or the coupon is invalid"
        elif len(browser.find_elements_by_xpath("//button[contains(text(),'Go to course')]")) == 1:
            reason = "you already own this course"
        else:
            reason = "of an unknown reason"
        return False, reason


parser = argparse.ArgumentParser()
parser.add_argument('--client_id', action="store_true", default=False, help="This is your client ID")
parser.add_argument('--access_token', action="store_true", default=False, help="This is your access token")
args = parser.parse_args()
# The following two lines are there because Pycharm was bothering me. But apart from that, they exist for no reason.
client_id = args.client_id
access_token = args.access_token
init()

if not client_id or not access_token:
    print(f"{Fore.YELLOW}[!] No cookies provided, trying to get them automatically...")
    access_token, client_id = get_cookies()
print(f"{Fore.GREEN}[{tick}] Successfully extracted needed cookies from your browsers!")

loop = asyncio.get_event_loop()
ua = UserAgent()
enroll_xpath = "//button[@class='course-cta btn btn-lg btn-quaternary btn-block']"
courses = get_free_courses()
browser = start_browser()

browser.get("https://www.udemy.com/random_page_that_does_not_exist/")
browser.add_cookie({'name': 'client_id', 'value': client_id, 'domain': "udemy.com"})
browser.add_cookie({'name': 'access_token', 'value': access_token, 'domain': "udemy.com"})
browser.get("https://www.udemy.com/?persist_locale=&locale=en_US")

try:
    WebDriverWait(browser, 3.5).until(EC.presence_of_element_located((
        By.XPATH, "//span[contains(text(),'Log in')]")))
    browser.quit()
    raise InvalidCookiesException()
except TimeoutException:
    print(f"{Fore.GREEN}[{tick}] Successfully logged in!\n")

success_counter = 0
for url in courses:
    browser.get(url)
    WebDriverWait(browser, 2).until(EC.presence_of_element_located((
        By.XPATH, "//h1[contains(@class,'clp-lead__title')]")))

    course_name = browser.find_element_by_xpath("//h1[contains(@class,'clp-lead__title')]").text.strip()
    enroll_test = enroll_possible()
    if enroll_test is not True:
        print(f"{Fore.YELLOW}[!] Cannot enroll in '{course_name}' because {enroll_test[1]}")
        continue
    try:
        WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, enroll_xpath)))
        browser.find_element_by_xpath(enroll_xpath).click()
    except (NoSuchElementException, ElementNotInteractableException,
            ElementClickInterceptedException, TimeoutException):
        continue
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((
            By.XPATH, "//strong[contains(text(),'Great choice, ')]")))

        print(f"{Fore.GREEN}[{tick}] Successully enrolled in {course_name}")
        success_counter += 1
        continue
    except TimeoutException:
        pass
    print(f"{Fore.RED}[{warning}] Unknown error, couldn't enroll in " + course_name)

print(f"\n{Fore.GREEN}[{tick}] All courses have been checked!")
success_rate = success_counter / len(courses)
if success_rate >= 50:
    print(f"{Fore.GREEN}[{tick}] Added {success_counter} courses to your account out of {len(courses)}")
else:
    print(f"{Fore.RED}[{tick}] Added only {success_counter} courses to your account out of {len(courses)}")
