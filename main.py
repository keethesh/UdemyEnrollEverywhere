import argparse

import browser_cookie3
from selenium.common.exceptions import ElementClickInterceptedException, \
    NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as chromeOpts
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scrapers import *

tick = u"\u2713"
warning = u"\u26A0"
loop = asyncio.ProactorEventLoop()
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


def get_user_info(driver):
    try:
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((
            By.XPATH, "//a[@id='header.profile']//div[@data-purpose='user-avatar']")))
        hover = ActionChains(driver).move_to_element(
            driver.find_element_by_xpath("//a[@id='header.profile']//div[@data-purpose='user-avatar']"))
        hover.perform()
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((
            By.XPATH, "//span[@class='text-midnight ellipsis']")))
        mail = driver.find_element_by_xpath("//span[@class='text-midnight ellipsis']").text
        display_name = driver.find_element_by_xpath("//span[contains(text(),'@')]").text
        return mail, display_name
    except TimeoutException:
        return None


def get_cookies():
    try:
        udemy_cookies = browser_cookie3.load(domain_name='www.udemy.com')._cookies["www.udemy.com"]["/"]
        return udemy_cookies["access_token"].value, udemy_cookies["client_id"].value

    except KeyError:
        raise NoCookiesException()


def get_free_courses():
    return loop.run_until_complete(get_courses())


def start_browser():
    opts = chromeOpts()
    # opts.add_argument("--headless")
    opts.add_argument(f"user-agent={ua.random}")
    prefs = {'profile.managed_default_content_settings.images': 2}  # Disallow images from loading
    opts.add_experimental_option("prefs", prefs)
    driver = Chrome(ChromeDriverManager(log_level=0).install(), options=opts)
    return driver


def start_and_login():
    while True:
        driver = start_browser()

        driver.get("https://www.udemy.com/random_page_that_does_not_exist/")
        driver.add_cookie(
            {'name': 'client_id', 'value': client_id, 'domain': "udemy.com"})
        driver.add_cookie(
            {'name': 'access_token', 'value': access_token, 'domain': "udemy.com"})
        driver.get("https://www.udemy.com/?persist_locale=&locale=en_US")
        if 'upgrade-your-browser' in driver.current_url:
            driver.quit()
        else:
            break

    try:
        WebDriverWait(driver, 3.5).until(ec.presence_of_element_located((
            By.XPATH, "//span[contains(text(),'Log in')]")))
        driver.quit()
        raise InvalidCookiesException()
    except TimeoutException:
        user_info = get_user_info(driver)
        if user_info is None:
            print(f"{Fore.GREEN}[{tick}] Successfully logged in!\n")
        else:
            print(f"{Fore.GREEN}[{tick}] Successfully logged in!")
            print(f"{Fore.YELLOW}[!] Email: {user_info[0]}")
            print(f"{Fore.YELLOW}[!] Display Name: {user_info[1]}\n")
    return driver


def enroll_possible():
    try:
        WebDriverWait(browser, 1.25).until(ec.presence_of_element_located((
            By.XPATH, "//span[contains(text(),'Free')]")))
        return True

    except TimeoutException:
        if len(browser.find_elements_by_xpath("//button[contains(text(),'Buy now')]")) == 1:
            reason = "the coupon does not provide enough discount or the coupon is invalid"
        elif len(browser.find_elements_by_xpath("//button[contains(text(),'Go to course')]")) == 1:
            reason = "you already own this course"
        else:
            reason = "of an unknown reason"
        return reason


parser = argparse.ArgumentParser()
parser.add_argument('--client_id', action="store_true",
                    default=False, help="This is your client ID")
parser.add_argument('--access_token', action="store_true",
                    default=False, help="This is your access token")
args = parser.parse_args()
# The following two lines are there because Pycharm was bothering me. But apart from that, they exist for no reason.
client_id = args.client_id
access_token = args.access_token

if not client_id or not access_token:
    print(f"{Fore.YELLOW}[!] No cookies provided, trying to get them automatically...")
    access_token, client_id = get_cookies()

print(f"{Fore.GREEN}[{tick}] Successfully extracted needed cookies from your browsers!")

ua = UserAgent()
enroll_xpath = "//button[@class='course-cta btn btn-lg btn-quaternary btn-block']"

print(f"{Fore.YELLOW}[!] Scraping courses from {len(functions_list)} websites...")
courses = get_free_courses()
print(f"{Fore.GREEN}[{tick}] Scraped {len(courses)} courses!")

browser = start_and_login()

success_counter = 0
for url in courses:
    browser.get(url)
    if len(browser.find_elements_by_xpath(
            "//span[contains(text(),'Sorry, this course is no longer accepting enrollme')]")) == 1:
        print(f"{Fore.YELLOW}[!] Cannot enroll in the course at {url} because the course is not "
              f"accepting enrollments anymore")
        continue
    try:
        WebDriverWait(browser, 3).until(ec.presence_of_element_located((
            By.XPATH, "//h1[contains(@class,'clp-lead__title')]")))
    except TimeoutException:
        continue

    course_name = browser.find_element_by_xpath("//h1[contains(@class,'clp-lead__title')]").text.strip()
    enroll_test = enroll_possible()
    if enroll_test is not True:
        print(f"{Fore.YELLOW}[!] Cannot enroll in '{course_name}' because {enroll_test}")
        continue

    try:
        WebDriverWait(browser, 3).until(
            ec.element_to_be_clickable((By.XPATH, enroll_xpath)))
        browser.find_element_by_xpath(enroll_xpath).click()
    except (NoSuchElementException, ElementNotInteractableException,
            ElementClickInterceptedException, TimeoutException):
        continue
    try:
        WebDriverWait(browser, 10).until(ec.presence_of_element_located((
            By.XPATH, "//strong[contains(text(),'Great choice, ')]")))

        print(f"{Fore.GREEN}[{tick}] Successully enrolled in '{course_name}'")
        success_counter += 1
        continue
    except TimeoutException:
        pass
    print(f"{Fore.RED}[{warning}] Unknown error, couldn't enroll in '{course_name}'")

print(f"\n{Fore.GREEN}[{tick}] All courses have been checked!")

success_rate = success_counter / len(courses)
if success_counter == 0:
    print(f"{Fore.RED}[!] None of the courses have been added to your account out of {len(courses)}")

if success_rate >= 50:
    print(f"{Fore.GREEN}[{tick}] Added {success_counter} courses to your account out of {len(courses)}")

else:
    print(f"{Fore.RED}[{tick}] Added only {success_counter} courses to your account out of {len(courses)}")

browser.quit()
