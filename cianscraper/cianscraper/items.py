  # Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import scrapy

def remove_price_tag(value):
    return value.replace(' ','').strip()


def remove_newline(value):
    return value.replace('\n\n', '').replace('\n', '').replace('\\', '').strip()


class CianscraperItem(scrapy.Item):
    headline = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    rooms = scrapy.Field(input_processor=MapCompose(str, remove_tags), output_processor=TakeFirst())
    area = scrapy.Field(input_processor=MapCompose(str, remove_tags), output_processor=TakeFirst())
    floor = scrapy.Field(input_processor=MapCompose(str, remove_tags), output_processor=TakeFirst())
    address = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, remove_price_tag), output_processor=TakeFirst())
    ad_id = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    page_number = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())


def remove_currency(value):
    return value.replace('£','').strip()

class WhiskyscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    price = scrapy.Field(input_processor = MapCompose(remove_tags, remove_currency), output_processor = TakeFirst())

    link = scrapy.Field()