# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
import pyhelpers.loadfuncs as lf
from pricebot.items import Link, LinkLoader
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


class WhiteawayLinksSpider(scrapy.Spider):

    name = 'whiteaway_links'
    allowed_domains = ['whiteaway.com']
    start_urls = ['https://www.whiteaway.com/']

    products = lf.load_names()
    product_url = [product.lower() for product in products]

    def __init__(self):
        # self.driver = webdriver.Firefox()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(executable_path=r"chromedriver.exe", chrome_options=options)
        self.products = lf.load_names()
        # self.products = ['KGE36BW40', 'KG49EBI40']

    def parse(self, response):
        url = response.request.url
        links_list = []
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        self.driver.get(response.url)

        for product in self.products:
            # search_form_class = "search__input js-search-field js-sniper-click js-click-track"
            search_form_class = "search__input"
            search_form = self.driver.find_element_by_class_name(search_form_class)
            search_form.send_keys(product)
            time.sleep(1)
            search_button_class = "search__submit"
            search_button = self.driver.find_element_by_class_name(search_button_class)
            search_button.click()
            time.sleep(1)
            try:
                link_container = self.driver.find_element_by_xpath(
                    '//div[@class="srp-product-box__image-section list"]//a')
                link = str(link_container.get_attribute("href"))
                product_link = 'https://www.whiteaway.com' + link
                l = LinkLoader(item=Link())
                l.add_value('link', product_link)
                l.add_value('product', product)
                l.add_value('date', date)
                l.add_value('retailer', 'Whiteaway')
                yield l.load_item()
            except NoSuchElementException:
                print(" ")
                print("-----------------------------")
                print("Element does not exist")
                print("-----------------------------")
                print(" ")
        self.driver.close()
