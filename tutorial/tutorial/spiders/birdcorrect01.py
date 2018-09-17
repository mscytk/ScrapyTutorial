# -*- coding: utf-8 -*-
import scrapy


class Birdcorrect01Spider(scrapy.Spider):
    name = 'birdcorrect01'
    allowed_domains = ['https://www.birdfan.net/pg/']
    start_urls = ['http://https://www.birdfan.net/pg//']

    def parse(self, response):
        pass
