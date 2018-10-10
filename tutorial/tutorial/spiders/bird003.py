from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders import Rule
# itemを使用するためにはImportが必要
from tutorial.items import BirdfanItem

class BirdSpider(CrawlSpider):
    name = 'bird003'
    allowed_domains = ['www.birdfan.net']
    start_urls = ['https://www.birdfan.net/pg/kind/']
    #start_urls = ['https://www.birdfan.net/pg/kind/ord17/fam1703/spe170305/']

    # スクレイピング対象のパスパターン、ドメイン以下のURLに関して正規表現で指定します
    # スクレイピング対象URL「https://www.birdfan.net/yyyy/mm/dd/数字」を指定
    allow_list = ['[12]\d{3}/[01]\d{1}/[0123]\d{1}/\d+/']
    #allow_list = ['2018/08/[0123]\d{1}/\d+/']

    allowd_list = []
#    allowd_list = ['https://www.birdfan.net/pg/kind/ord17/fam1703/spe170305/']

    rules = [
        Rule(LinkExtractor(allow=allow_list), callback='parse_topics'),
        Rule(LinkExtractor(allow_domains=allowd_list), follow=True),
    ]

    def parse_topics(self, response):
        from pykakasi import kakasi
        kakasi = kakasi()

        kakasi.setMode('H', 'a')
        kakasi.setMode('K', 'a')
        kakasi.setMode('J', 'a')

        conv = kakasi.getConverter()

        jpgpath = response.xpath('//*[@id="contents"]/div[3]/div/p/img/@src').extract_first()
        birditem = BirdfanItem()
        birditem['url'] = response.url
        birditem['title'] = response.xpath('//*[@id="contents"]/div[3]/h2/a/text()').extract_first()
#        birditem['birdname'] = response.xpath('//*[@id="contents"]/div[3]/div/div/h3/a/text()').extract_first()
        birditem['birdname'] = conv.do(response.xpath('//*[@id="contents"]/div[3]/div/div/h3/a/text()').extract_first())
        birditem['jpgurl'] = response.urljoin(jpgpath)
#        print("birditem : {0}".format(birditem))
        yield  birditem
