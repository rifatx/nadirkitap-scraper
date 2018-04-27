import re

import scrapy
import logging

logging.getLogger('scrapy').setLevel(logging.DEBUG)


class SiteSpider(scrapy.Spider):
    name = "site"
    start_urls = [
        "https://www.nadirkitap.com/sahaflar.html",
    ]
    custom_settings = {
        'CONCURRENT_REQUESTS': '1000',
        'CONCURRENT_ITEMS': '10000'
    }

    def parse(self, response):
        for sahaf in response.xpath('//ul[@class="kitapsatici-list"]/li'):
            url = sahaf.xpath(
                'div[@class="col-md-2 no-padding icons hidden-xs"][1]/span[@class="icon icon-bg icon-kitap"]/a/@href').extract_first()

            # p = re.compile(".*satici=(\d*)")
            # p = p.search(url)
            # bookshopId = p.group(1)
            #
            # bookshopName = sahaf.xpath('div[@class="col-md-8 col-xs-7 no-padding"]/p/a/text()').extract_first()
            # bookCount = sahaf.xpath(
            #     'div[@class="col-md-2 no-padding icons hidden-xs"][1]/span[@class="icon icon-bg icon-kitap"]/a/text()').extract_first()
            #
            # print(bookshopName, bookCount)

            if url is not None:
                yield scrapy.Request(url=url, callback=self.parse_book_list)
                # print(url)

        next_page_url = response.xpath('//a[@aria-label="Next"]/@href').extract_first()
        if next_page_url is not None:
            yield response.follow(url=next_page_url, callback=self.parse_book_list)

    def parse_book_list(self, response):
        for kitap in response.xpath('//ul[@class="product-list"]/li'):
            url = kitap.xpath(
                'div[@class="col-md-10 col-sm-12 col-xs-12 no-padding"]/div[@class="product-list-right-top"]/div[@class="col-md-8"]/h4[@class="break-work"]/a/@href').extract_first()

            if url is not None:
                yield scrapy.Request(url=url, callback=self.parse_book)

        next_page_url = response.xpath('//a[@aria-label="Next"]/@href').extract_first()
        if next_page_url is not None:
            yield response.follow(url=next_page_url, callback=self.parse_book_list)

    def parse_book(self, response):
        bookshopName = response.xpath(
            '//div[@class="row"]/div[@class="col-md-3 col-xs-12 mbl-margin-top20"]/div[@class="product-rg-list"]/div[@class="top-bg"]/p/a/text()').extract_first()
        bookshopId = response.xpath(
            '//div[@class="row"]/div[@class="col-md-3 col-xs-12 mbl-margin-top20"]/div[@class="product-rg-list"]/div[@class="top-bg"]/p/a/@href').extract_first()
        bookName = response.xpath(
            '//div[@class="row"]/div[@class="col-md-6 no-padding mbl-padding col-xs-12"]/h1[@class="a18"]/text()').extract_first()
        writer = response.xpath(
            '//div[@class="row"]/div[@class="col-md-6 no-padding mbl-padding col-xs-12"]/p[@class="a14"]/a/text()').extract_first()
        price = response.xpath(
            '//div[@class="row"]/div[@class="col-md-6 no-padding mbl-padding col-xs-12"]/div[@class="col-md-12 no-padding"][1]/p[@class="col-md-9 col-xs-12 no-padding product-price"]/text()').extract_first()
        productId = response.xpath(
            '//div[@class="row"]/div[@class="col-md-6 no-padding mbl-padding col-xs-12"]/div[@class="col-md-12  no-padding"][1]/div[@class="product-dt-list col-xs-12"]/ul[@class="msj-list col-md-6 col-xs-12 no-padding"][1]/li[@class="col-md-7 col-xs-8 clr-36"][1]/text()').extract_first()
        translator = response.xpath(
            '//div[@class="row"]/div[@class="col-md-6 no-padding mbl-padding col-xs-12"]/div[@class="col-md-12  no-padding"][1]/div[@class="product-dt-list col-xs-12"]/ul[@class="msj-list col-md-6 col-xs-12 no-padding"][1]/li[@class="col-md-7 col-xs-8 clr-36"][3]/text()').extract_first()

        if bookshopId is not None:
            p = re.compile(".*uyeid=(\d*)")
            p = p.search(bookshopId)
            bookshopId = p.group(1)

        if price is not None:
            price = price[:-3]

        if productId is not None:
            productId = productId[2:]

        if translator is not None:
            translator = translator[2:]

        if price is not None:
            yield {
                'bookshopName': bookshopName,
                'bookshopId': bookshopId,
                'productId': productId,
                'name': bookName,
                'writer': writer,
                'price': price,
                'translator': translator
            }
