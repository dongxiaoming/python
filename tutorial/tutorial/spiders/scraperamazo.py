import logging
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "amazone"
    start_urls = ['https://www.amazon.co.jp/product-reviews/B01ETRGGYI/ref=cm_cr_dp_see_all_btm?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=recent',
      #  'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for brickset in response.xpath("//*[contains(@class, 'a-section celwidget')]"):
            NAME_SELECTOR = ".//*[contains(@class, 'review-text')]/text()"
            PIECES_SELECTOR = ".//div[contains(@class, 'a-row')]/a/@title"
            MINIFIGS_SELECTOR = ".//span[contains(@class, 'review-date')]/text()"

            yield {
                'text': brickset.xpath(NAME_SELECTOR).extract_first(),
                'star': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'date': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
            }
        #next_page = response.css('li.next a::attr("href")').extract_first()
        url = response.xpath("//li[contains(@class,'a-last')]/a/@href").extract_first()
        #logging.warning("==================###===%s",url)
        if url is not None:
            url=url.replace('/Fire-TV-Stick-New-モデル','https://www.amazon.co.jp')
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse)
