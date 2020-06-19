import aiohttp
from lxml import html
from tqdm import tqdm


async def yofreesamples():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://yofreesamples.com/courses/free-discounted-udemy-courses-list/") as response:
            response = await response.read()
            doc = html.fromstring(response)
            return list(
                set([course.attrib["href"] for course in doc.xpath('//a[@href][@class="btn btn-md btn-success"]')]))


async def learnviral():  # Not used at the moment, takes too much time to complet
    courses_list = []
    base_url = "https://udemycoupon.learnviral.com/page/"
    async with aiohttp.ClientSession() as session:
        async with session.get("https://udemycoupon.learnviral.com/") as response:
            response = await response.read()
            doc = html.fromstring(response)
            total_pages = int(doc.xpath("//div[@id='content']//a[3]")[0].text.replace(",", ""))
            for link in doc.xpath('//a[@class="coupon-code-link btn promotion"]'):
                courses_list.append(link.attrib.get("href"))

        for page in tqdm(range(2, total_pages + 1)):
            async with session.get(f"{base_url}{page}") as response:
                response = await response.read()
                doc = html.fromstring(response)
                for link in doc.xpath('//a[@class="coupon-code-link btn promotion"]'):
                    courses_list.append(link.attrib.get("href"))

    return courses_list


site_list = [yofreesamples()]
