import scrapy
from sfaptsscraper.items import SfaptsscraperItem
from scrapy.loader import ItemLoader

class SFaptsSpider(scrapy.Spider):
    name = 'sfapts'
    start_urls =  ['https://sfbay.craigslist.org/d/apartments-housing-for-rent/search/sfc/apa']

    def parse(self, response):
        
        for link in response.css('a.result-title.hdrlnk::attr(href)').getall():
            yield scrapy.Request(link, callback = self.parse_page)

        PATH_START = 'https://sfbay.craigslist.org'
        next_page = response.css('a.button.next').attrib['href']
        if next_page is not None:
            yield response.follow(PATH_START + next_page, callback=self.parse)

    def parse_page(self, response):
        
        l = ItemLoader(item = SfaptsscraperItem(), response=response)

        l.add_xpath('name','//*[@id="titletextonly"]/text()')
        l.add_css('price', 'span.price::text')
        l.add_css('address', 'div.mapaddress::text')
        l.add_xpath('neighborhood', '/html/body/section/section/h1/span/small/text()')
        l.add_xpath('bedrooms', '/html/body/section/section/section/div[1]/p[1]/span[1]/b[1]/text()')
        l.add_xpath('bathrooms', '/html/body/section/section/section/div[1]/p[1]/span[1]/b[2]/text()')
        l.add_xpath('link', '/html/head/link[1]/@href')
        l.add_xpath('postid', '/html/body/section/section/section/div[2]/p[1]/text()')
        l.add_xpath('postdate', '/html/body/section/section/section/div[2]/p[2]/time/@datetime')
        l.add_xpath('latitude', '//*[@id="map"]/@data-latitude')
        l.add_xpath('longitude', '//*[@id="map"]/@data-longitude')
        
        return l.load_item()