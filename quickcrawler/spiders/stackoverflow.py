import scrapy
import pathlib

class StackoverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions']

    custom_settings = {
        # 'FEED_FORMAT': 'csv',
        # 'FEED_URI' : 'tmp/stackoverflow_questions.csv'
        'FEEDS': {
            pathlib.Path('data/stackoverflow/questions.csv'): {
                'format': 'csv',
                'fields': ['title', 'url', 'tag'],
                # 'item_filter': 'myproject.filters.MyCustomFilter2',
                # 'postprocessing': [MyPlugin1, 'scrapy.extensions.postprocessing.GzipPlugin'],
                # 'gzip_compresslevel': 5,
            },
        },
    }

    def parse(self, response):
        questions = response.css('.s-post-summary--content-title > a')
        urls=questions.css('a::attr(href)').extract()
        titles=questions.css('a::text').extract()
        tags_list = response.css(".s-post-summary--meta-tags")
        tags = [tag.css('a::text').extract() for tag in tags_list]
        # title = response.css('.s-post-summary--content-title > a::attr(href)')
        self.log(f'urls {urls[0]}')
        self.log(f'titles {titles[0]}')
        self.log(f'tag {tags[0]}')

        for item in zip(titles,urls,tags):
            question_info = {
                'title' : item[0],
                'url' : item[1],
                'tag' : item[2]
            }

            yield question_info
