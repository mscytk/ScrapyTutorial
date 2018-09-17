import scrapy


class BirdsSpider(scrapy.Spider):
    name = "birds001"

    start_urls = [
      'https://www.birdfan.net/pg/kind/',
    ]

    def parse(self, response):
        for bird in response.xpath('//*[@id="species_table"]/tbody/tr'):
          yield {
            'name' : bird.xpath('td[1]/a/text()').extract_first(),
            'link' : response.urljoin(bird.xpath('td[1]/a/@href').extract_first()),
            'num' : bird.xpath('td[2]/text()').extract_first()
          }