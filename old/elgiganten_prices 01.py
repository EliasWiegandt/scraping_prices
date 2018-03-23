# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
from pricebot.items import Product, ProductLoader, Website, WebsiteLoader
import pyhelpers.loadfuncs as lf


class ElgigantenSpider(scrapy.Spider):
    name = 'elgiganten_prices'
    allowed_domains = ['https://www.elgiganten.dk']

    def __init__(self):
        self.products = lf.load_names()
        self.base_url = 'https://www.elgiganten.dk/product/hvidevarer/kolefryseskab/'

    def start_requests(self):
        for product in self.products:
            url = self.base_url + product + '/'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        product_match = response.request.url.split('/')[-2]
        p = ProductLoader(item=Product(), response=response)
        p.add_value('product', product_match)
        p.add_xpath('price',
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
