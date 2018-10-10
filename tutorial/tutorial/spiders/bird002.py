import scrapy

class BirdsSpider(scrapy.Spider):
    name = "birds002"

    start_urls = [
      'https://www.birdfan.net/pg/kind/',
    ]

    def parse(self, response):
        counter = 0
        for href in response.xpath('//*[@id="species_table"]/tbody/tr/td[1]/a/@href').extract():
            counter = counter + int(response.xpath('//*[@id="species_table"]/tbody/tr/td[2]/text()').extract_first())
            yield scrapy.Request(response.urljoin(href), callback=self.parse_author)

        print('count: ' + str(counter))

    def parse_author(self, response):
        # <a>タグがテキストを持っている場合「すべての写真を見る」リンクがあると判断し、そのリンクでリクエストする
        if response.xpath('//*[@id="contents"]/div[4]/p/a/text()').extract_first() is not None:
            print(response.xpath('//*[@id="contents"]/div[4]/p/a/text()').extract())
            l = len(response.xpath('//*[@id="contents"]/div[4]/p/a'))
            p = response.xpath('//*[@id="contents"]/div[4]/p/a['+str(l)+']/@href').extract_first()
            scrapy.Request(response.urljoin(p), callback=self.parse_author)

        # <a>タグのhrefをforでリクエストする
        for card in response.xpath('//*[@id="contents"]/div[4]/p/a/@href').extract():
            yield scrapy.Request(response.urljoin(card), callback=self.req_card)

    def req_card(self, response):
        # 受け取ったクエリでresponseから抽出する
        def extract_with_xpath(query):
            return response.xpath(query).extract_first()

        yield {
            'uname' : extract_with_xpath('//*[@id="contents"]/div[3]/h2/a/text()'),
            'kname' : extract_with_xpath('//*[@id="contents"]/div[3]/div/div/h3/a/text()'),
            'isrc' : response.urljoin(extract_with_xpath('//*[@id="contents"]/div[3]/div/p/img/@src')),
        }
