import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class YellowSpiderSpider(CrawlSpider):
    name = 'yellow_spider'
    allowed_domains = ['yellowpages.ca']

    def start_requests(self):

        urls = ['https://www.yellowpages.ca/search/si/1/realestate/Toronto+ON']
        yield scrapy.Request(urls[0])

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[contains(@href,'Ontario') and contains(@class,'name')]"), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths="//span[@class='pageCount']/following-sibling::a"), follow=True)
    )

    def parse_item(self, response):
        item = {}
        item['Name'] = response.xpath("//div[@class='merchant__name']//span[@itemprop='name'][1]/text()").get()
        address = ''
        streetAddress = response.xpath("//div[@class='merchant__name']//span[@itemprop='streetAddress'][1]/text()").get()
        if streetAddress:
            address += streetAddress
        addressLocality = response.xpath("//div[@class='merchant__name']//span[@itemprop='addressLocality']/text()").get()
        if addressLocality:
            address += addressLocality
        addressRegion = response.xpath("//div[@class='merchant__name']//span[@itemprop='addressRegion']/text()").get()
        if addressRegion:
            address += addressRegion
        postalCode = response.xpath("//div[@class='merchant__name']//span[@itemprop='postalCode']/text()").get()
        if postalCode:
            address += postalCode
        item['Address'] = address
        item['Phone'] = response.xpath("//li[contains(@class,'phone')]//span[contains(@class,'text')][1]/text()").get()
        return item
