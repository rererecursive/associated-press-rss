from dateutil import parser
import json
import scrapy
from scrapy.exporters import XmlItemExporter
from scrapy.crawler import CrawlerProcess

class ApSpider(scrapy.Spider):
    name = "ap"
    start_urls = [
        'https://apnews.com/apf-topnews'
    ]

    def parse(self, response):
        items =  response.xpath('//div[re:test(@class, "^FeedCard")]')
        base_url = 'https://apnews.com'

        yield {
          'description': 'AP Top News',
          'link': 'https://apnews.com/apf-topnews',
          'title': 'AP Top News'
        }

        for item in items:
            title = item.css('h1::text').get()
            identifier = item.xpath('.//a[re:test(@class, "^Component-headline")]/@href').get('')
            description = item.xpath('.//a[re:test(@class, "^firstWords")]/div/p/text()').get('No description was provided.')
            pub_date = item.xpath('.//span[re:test(@class, "^Timestamp Component")]/@data-source').get()

            # Fri, 13 Dec 2019 18:56:20 +0000
            pub_date_formatted = parser.parse(pub_date).strftime('%a, %d %b %Y %H:%M:%S +0000')

            if not identifier:
                continue

            yield {
                'title': title,
                'link': base_url + identifier,
                'description': description,
                'guid': base_url + identifier,
                'pub_date': pub_date_formatted
            }

def handler(event, context):
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    print("Received event:", json.dumps(event))

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })


    process = CrawlerProcess(get_project_settings())

    process.crawl(ApSpider)
    process.start() # the script will block here until the crawling is finished

    print('All done.')

# if __name__ == "__main__":
#     handler('', '')
