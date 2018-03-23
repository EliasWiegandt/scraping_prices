# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
from pricebot.items import Product, ProductLoader, Website, WebsiteLoader
import pyhelpers.loadfuncs as lf


class ElgigantenSpider(scrapy.Spider):
    name = 'elgiganten_prices'
    allowed_domains = ['https://www.elgiganten.dk']

    products = lf.load_names()
    url_base = 'https://www.elgiganten.dk'
    url_before = 'https://www.elgiganten.dk/search?SearchTerm='
    url_end = '&search=&searchResultTab='

    def start_requests(self):
        for product in self.products:
            url = self.url_before + product + self.url_end
            yield scrapy.Request(url=url, callback=self.parse_product_page)

    def parse_product_page(self, response):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        for product in self.products:
            if product.lower() in response.request.url:
                product_match = product

                p = ProductLoader(item=Product(), response=response)
                p.add_value('product', product_match)
                p.add_xpath(
                    'price',
                    '//div[@class="product-price-container"]//span/text()')
                p.add_value('date', date)
                p.add_value('retailer', "Elgiganten")
                yield p.load_item()

                w = WebsiteLoader(item=Website(), response=response)
                w.add_value('html', response.body)
                w.add_value('date', date)
                w.add_value('product', product_match)
                w.add_value('retailer', "Elgiganten")
                yield w.load_item()
