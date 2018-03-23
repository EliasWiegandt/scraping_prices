# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from w3lib.html import remove_tags, replace_escape_chars
from scrapy.loader.processors import MapCompose, Compose, Join, TakeFirst


def set_to_lower(scrape):
    return str(scrape).lower()


def extract_number(scrape):
    number = int(''.join([str(s) for s in str(scrape) if s.isdigit()]).strip())
    return number


class Product(scrapy.Item):
    product = scrapy.Field()
    price = scrapy.Field()
    retailer = scrapy.Field()
    date = scrapy.Field()


class Website(scrapy.Item):
    html = scrapy.Field()
    product = scrapy.Field()
    retailer = scrapy.Field()
    date = scrapy.Field()


class Link(scrapy.Item):
    link = scrapy.Field()
    product = scrapy.Field()
    retailer = scrapy.Field()
    date = scrapy.Field()


class ProductLoader(scrapy.loader.ItemLoader):
    default_output_processor = MapCompose(remove_tags)

    product_in = MapCompose(remove_tags,
                            lambda s: replace_escape_chars(s, which_ones=('\n', '\t', '\r', '\xa0', ' ')))
    product_out = TakeFirst()

    price_in = MapCompose(remove_tags,
                          lambda s: replace_escape_chars(s, which_ones=('\n', '\t', '\r', '\xa0', ' ')),
                          extract_number)
    price_out = TakeFirst()

    retailer_in = Compose()
    retailer_out = TakeFirst()

    date_in = Compose()
    date_out = TakeFirst()


class WebsiteLoader(scrapy.loader.ItemLoader):
    retailer_in = Compose()
    retailer_out = TakeFirst()

    date_in = Compose()
    date_out = TakeFirst()

    product_in = TakeFirst()
    product_out = TakeFirst()

    html_in = Compose()
    html_out = TakeFirst()


class LinkLoader(scrapy.loader.ItemLoader):
    product_in = MapCompose(remove_tags)
    product_out = TakeFirst()

    retailer_in = Compose()
    retailer_out = TakeFirst()

    date_in = Compose()
    date_out = TakeFirst()

    link_in = Compose()
    link_out = TakeFirst()
