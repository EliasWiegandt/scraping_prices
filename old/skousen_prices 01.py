# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
from pricebot.items import Product, ProductLoader, Website, WebsiteLoader
import pyhelpers.loadfuncs as lf
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SkousenSpider(CrawlSpider):
    name = 'skousen_prices'
    allowed_domains = ['skousen.dk']
    start_urls = ['https://www.skousen.dk/hvidevarer/koele-fryseskab/']
    products = lf.load_names()
    product_url = [product.lower() for product in products]

    rules = (
        Rule(LinkExtractor(allow=(product_url)), callback='parse_item'),
        Rule(LinkExtractor(allow=r"koele")),
    )

    def parse_item(self, response):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        for product in self.products:
            if product.lower() in response.request.url:
                product_match = product
        p = ProductLoader(item=Product(), response=response)
        p.add_value('product', product_match)

        normal_div = '//div[@class="vip__price-box-price"]/text()'
        discount_div = '//div[@class="campaign-banner__info__right"]//span[@class="top"]/text()'
        normal_container = response.xpath(normal_div)
        discount_container = response.xpath(discount_div)

        if len(discount_container) > 0:
            price_div = discount_div
        else:
            price_div = normal_div

        print('============================')
        print(normal_container)
        print(discount_container)
        print('============================')

        p.add_xpath('price', price_div)
        p.add_value('date', date)
        p.add_value('retailer', "Skousen")
        yield p.load_item()

        w = WebsiteLoader(item=Website(), response=response)
        w.add_value('html', response.body)
        w.add_value('date', date)
        w.add_value('product', product_match)
        w.add_value('retailer', "Skousen")
        yield w.load_item()
