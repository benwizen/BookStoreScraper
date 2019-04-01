# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Book(scrapy.Item):
    stars = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()


class BookSpider(CrawlSpider):
    name = 'BookSpider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    rules = (Rule(LinkExtractor(allow='http://books.toscrape.com/', restrict_css='.next>a')
                  , callback="parse_books", follow=True),)

    def parse_books(self, response):
        stars_enum = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        for book in response.css('article.product_pod'):
            b = ItemLoader(item=Book(), response=response)
            b.add_value('stars', book.css('.star-rating::attr(class)').extract(),
                        Compose(lambda v: stars_enum[v[0].split()[1]]))
            b.add_value('title', book.css('.product_pod > h3 > a::attr(title)').extract())
            b.add_value('price', book.css('.product_price > p.price_color::text').extract(),
                        Compose(lambda v: float(v[0][1:])))
            yield b.load_item()
