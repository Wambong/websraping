import scrapy
from scrapy.loader import ItemLoader
from urllib.parse import urlparse
from ..items import CianscraperItem
import re
class CianSpider(scrapy.Spider):
    name = 'cian'
    start_urls = ['https://kazan.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=4777&room1=1']

    def parse(self, response):

        ads = response.css('div._93444fe79c--general--BCXJ4')
        for ad in ads:
            i = ItemLoader(item=CianscraperItem(), selector=ad)
            i.add_css("headline", 'span[data-mark="OfferTitle"]')
            i.add_css("address", "div._93444fe79c--labels--L8WyJ")
            i.add_css("price", 'span[data-mark="MainPrice"]')

            ad_id = self.extract_ad_id(ad)
            i.add_value("ad_id", ad_id)
            details = ad.css('span::text').get()

            rooms, area, floor = self.extract_details(details)
            i.add_value("rooms", rooms)
            i.add_value("area", area)

            url = response.url
            page_number_match = re.search(r'&p=(\d+)', url)
            page_number = page_number_match.group(1) if page_number_match else None
            i.add_value("page_number", page_number)
            i.add_value("floor", floor)
            yield i.load_item()


        next_page_links = response.css('a._93444fe79c--button--KVooB._93444fe79c--link-button--ujZuh._93444fe79c--M--I5Xj6._93444fe79c--button--WChcG::attr(href)').getall()


        if next_page_links:
            next_page_url = next_page_links[-1]
            yield response.follow(next_page_url, self.parse)
        else:

            self.logger.info('No more pages to scrape.')
    def extract_ad_id(self, ad):

        url = ad.css('a::attr(href)').get()
        parsed_url = urlparse(url)
        ad_id = parsed_url.path.split('/')[-2]
        return ad_id
    def extract_details(self, details):

        match = re.match(r'(\d+)-комн\..*?([\d,.]+)\sм².*?(\d+)/(\d+)', details)
        if match:
            rooms = int(match.group(1))
            area = float(match.group(2).replace(',', '.'))
            floor = int(match.group(3))
            total_floors = int(match.group(4))
            return rooms, area, f"{floor}/{total_floors}"
        else:
            return None, None, None




