# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
import csv
from selenium import webdriver
from pricebot.items import Link, LinkLoader
import pyhelpers.loadfuncs as lf


class PowerLinksSpider(scrapy.Spider):
    name = 'power_links'
    allowed_domains = ['www.power.dk']
    start_urls = [
        'https://www.power.dk/hvidevarer/koel-frys-og-koelefryseskabe/koelefryseskabe/pl-1215/'
    ]

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.products = lf.load_names()

    def parse(self, response):
        url = response.request.url
        links_list = []
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        self.driver.get(response.url)
        price = 0
        product_container = self.driver.find_elements_by_xpath(
            '//div[@class="product product-element angi product-4col"]')
        for product_check in product_container:
            product_name = product_check.find_element_by_xpath(
                './/span[@class="product-name ng-binding"]').text
            for product in self.products:
                if product.lower() in product_name.lower():
                    product_link = 'https://www.power.dk' + str(
                        product_check.get_attribute("data-gtmurl"))

                    l = LinkLoader(item=Link())
                    l.add_value('link', product_link)
                    l.add_value('product', product)
                    l.add_value('date', date)
                    l.add_value('retailer', 'Power')
                    yield l.load_item()
        self.driver.close()
