# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
import csv
from pricebot.items import Product, ProductLoader, Website, WebsiteLoader


class PowerPricesSpider(scrapy.Spider):
    name = 'power_prices'
    allowed_domains = ['www.power.dk']

    def __init__(self):
        now = datetime.datetime.now()
        self.date = now.strftime("%Y%m%d")
        self.links = []
        self.products = []
        filepath = os.path.join(os.getcwd(),
                                'linksdata/power_links_%s.csv' % (self.date))
        with open(filepath) as f:
            links_csv = csv.DictReader(f, skipinitialspace=True)
            for row in links_csv:
                self.links.append(row['link'])
                self.products.append(row['product'])

    def start_requests(self):
        for url in self.links:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        p = ProductLoader(item=Product(), response=response)
        p.add_xpath('price', '//div[@class="prices-container "]//span/text()')
        p.add_value('date', date)
        p.add_value('retailer', "Power")
        product_name = response.xpath(
            '//div[@class="container pad"]//h1/text()').extract_first()
        for product in self.products:
            if product.lower() in product_name.lower():
                product_match = product
                p.add_value('product', product_match)
        yield p.load_item()

        w = WebsiteLoader(item=Website(), response=response)
        w.add_value('html', response.body)
        w.add_value('date', date)
        w.add_value('product', product_match)
        w.add_value('retailer', "Power")
        yield w.load_item()
