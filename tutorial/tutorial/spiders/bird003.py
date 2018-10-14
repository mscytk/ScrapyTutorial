from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders import Rule
# itemを使用するためにはImportが必要
from tutorial.items import BirdfanItem

class BirdSpider(CrawlSpider):
    # 実行するときの識別子
    name = 'bird003'
    # spiderに探査を許可するドメイン
    allowed_domains = ['www.birdfan.net']
    # 起点(探査を開始する)URL
    start_urls = ['https://www.birdfan.net/pg/kind/']

    # スクレイピング対象のパスパターン、ドメイン以下のURLに関して正規表現で指定します
    # スクレイピング対象URL「https://www.birdfan.net/yyyy/mm/dd/数字」を指定
    allow_list = ['[12]\d{3}/[01]\d{1}/[0123]\d{1}/\d+/']

    # スクレイピング対象のドメイン、パスを指定（動作確認用に探査範囲を狭めるときに使用した）
    allowd_list = []
#    allowd_list = ['https://www.birdfan.net/pg/kind/ord17/fam1703/spe170305/']

    rules = [
        # スクレイピングするURLのルールを LinkExtractorの引数で指定(https://scrapy-ja.readthedocs.io/ja/latest/topics/link-extractors.html)
        Rule(LinkExtractor(allow=allow_list, allow_domains=allowd_list), callback='parse_topics'),
        Rule(LinkExtractor(), follow=True),
    ]

    def parse_topics(self, response):
        # 全角をローマ字に変換してくれるコンバータ(pykakasi)を準備
        from pykakasi import kakasi
        kakasi = kakasi()
        kakasi.setMode('H', 'a')
        kakasi.setMode('K', 'a')
        kakasi.setMode('J', 'a')
        conv = kakasi.getConverter()

        # アイテムクラス"birditem"に画像ファイルごとの情報を格納
        jpgpath = response.xpath('//*[@id="contents"]/div[3]/div/p/img/@src').extract_first()
        birditem = BirdfanItem()
        # 画像ファイルを持つページのURL
        birditem['url'] = response.url
        # 画像ファイルを持つページのタイトル（人間向けのほう）
        birditem['title'] = response.xpath('//*[@id="contents"]/div[3]/h2/a/text()').extract_first()
        # 画像ファイルの野鳥の種別名（全角）をローマ字に変換して格納
        birditem['birdname'] = conv.do(response.xpath('//*[@id="contents"]/div[3]/div/div/h3/a/text()').extract_first())
        # 画像ファイルのURL
        birditem['jpgurl'] = response.urljoin(jpgpath)
        yield  birditem
