import asyncio
import time
from itertools import chain

import aiohttp
from colorama import init, Fore
from fake_useragent import UserAgent
from lxml import html

tick = u"\u2713"
warning = u"\u26A0"
init()


async def get_courses():
    gathered_urls = [link for link in list(set(chain.from_iterable(await asyncio.gather(*functions_list))))]
    return gathered_urls


async def yofreesamples():
    t1 = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://yofreesamples.com/courses/free-discounted-udemy-courses-list/") as response:
            response = await response.read()
            doc = html.fromstring(response)
            print(
                f"{Fore.GREEN}[{tick}] Successfully scraped courses from YoFreeSamples in {round(time.time() - t1)} seconds!")
            return list(
                set([course.attrib["href"] for course in doc.xpath('//a[@href][@class="btn btn-md btn-success"]')]))


async def learnviral_wrapper():
    tasks, session = await create_learnviral_futures("https://udemycoupon.learnviral.com/"
                                                     "coupon-category/free100-discount")
    t1 = time.time()
    courses = list(set(chain.from_iterable(await asyncio.gather(*tasks))))
    t2 = time.time()
    courses = [link for link in courses if "/?couponCode=" in link]
    await session.close()
    print(f"{Fore.GREEN}[{tick}] Successfully scraped courses from LearnViral in {round(t2 - t1)} seconds!")
    return courses


async def create_learnviral_futures(base_url, pages_number=100):
    session = aiohttp.ClientSession()
    if pages_number == "all":
        async with session.get(base_url, headers={"User-Agent": ua.random}) as response:
            response = await response.read()
            doc = html.fromstring(response)
            pages_number = int(doc.xpath("//div[@id='content']//a[last()-1]")[0].text.replace(",", ""))
    tasks = [asyncio.ensure_future(learnviral(f"{base_url}/page/{page_number}", session))
             for page_number in range(1, pages_number + 1)]
    return tasks, session


async def learnviral(url, session):
    coupon_xpath = '//div[@class="content-box"]//a[@class="coupon-code-link btn promotion"]'
    courses_list = []
    for _ in range(2):
        try:
            async with session.get(url) as response:
                response = await response.read()
                doc = html.fromstring(response)
                for link in doc.xpath(coupon_xpath):
                    courses_list.append(link.attrib.get("href"))
            break
        except asyncio.TimeoutError:
            await asyncio.sleep(15)
    return courses_list


times = 0
ua = UserAgent()
functions_list = [yofreesamples(),
                  learnviral_wrapper()]
