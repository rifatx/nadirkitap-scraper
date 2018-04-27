import scrapy
import logging

logging.getLogger('scrapy').setLevel(logging.ERROR)

class BookshopListSpider(scrapy.Spider):
    name = "bookshoplist"
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
                yield {'url': url}

        next_page_url = response.xpath('//a[@aria-label="Next"]/@href').extract_first()
        if next_page_url is not None:
            yield response.follow(url=next_page_url, callback=self.parse)
