import scrapy
import pathlib

class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    allowed_domains = ['bbiquge.net']
    start_urls = ['https://www.bbiquge.net/']

    custom_settings={
        'FEEDS': {
            pathlib.Path('data/biquge/books.csv'): {
                'format': 'csv',
                'fields': ['title', 'tag', 'book_url', 'pic_url'],
                # 'item_filter': 'myproject.filters.MyCustomFilter2',
                # 'postprocessing': [MyPlugin1, 'scrapy.extensions.postprocessing.GzipPlugin'],
                # 'gzip_compresslevel': 5,
            },
        },
    }

    def parse(self, response):
        items = response.css(".item")
        for item in items:
            pic_url=item.css('.pic>a>img::attr(src)').extract_first()
            book_url=item.css('.txt>dl>dt>a::attr(href)').extract_first()
            title=item.css('.txt>dl>dt>a::text').extract_first()
            tag=item.css('.txt>dl>dd::text').extract()
            book_info = {
                'title': title,
                'tag': tag,
                'book_url': book_url,
                'pic_url': pic_url,
            }
            yield book_info
