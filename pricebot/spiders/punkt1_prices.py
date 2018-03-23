# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
from pricebot.items import Product, ProductLoader, Website, WebsiteLoader
import pyhelpers.loadfuncs as lf
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import csv


class Punkt1Spider(scrapy.Spider):

    name = 'punkt1_prices'
    allowed_domains = ['punkt1.com']

    def __init__(self):
        now = datetime.datetime.now()
        self.date = now.strftime("%Y%m%d")
        self.links = []
        self.products = []
        retailer = self.name.split('_')[0]
        filepath = os.path.join(
            os.getcwd(), 'linksdata/%s/punkt1_links_%s.csv' % (retailer,
                                                               self.date))
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
        for product in self.products:
            if product.lower() in response.request.url:
                product_match = product
                p = ProductLoader(item=Product(), response=response)
                p.add_value('product', product_match)

                normal_div = '//span[@class="product-price-tag"]/text()'
                discount_div = '//span[@class="product-price-tag"]/text()'
                normal_container = response.xpath(normal_div)
                discount_container = response.xpath(discount_div)

                if len(discount_container) > 0:
                    price_div = discount_div
                else:
                    price_div = normal_div

                # print('============================')
                # print(normal_container)
                # print(discount_container)
                # print('============================')

                p.add_xpath('price', price_div)
                p.add_value('date', date)
                p.add_value('retailer', "Punkt1")
                yield p.load_item()

                w = WebsiteLoader(item=Website(), response=response)
                w.add_value('html', response.body)
                w.add_value('date', date)
                w.add_value('product', product_match)
                w.add_value('retailer', "Punkt1")
                yield w.load_item()
