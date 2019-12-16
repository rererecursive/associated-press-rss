from dateutil import parser
import boto3
import json
import logging
import scrapy
from scrapy.exporters import XmlItemExporter
from scrapy.crawler import CrawlerProcess

logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('nose').setLevel(logging.WARNING)


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
    from scrapy.utils.project import get_project_settings
    from scrapy.settings import Settings
    import settings as my_settings

    print("Received event:", json.dumps(event))

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(settings=crawler_settings)
    # process = CrawlerProcess(get_project_settings())

    process.crawl(ApSpider)
    process.start() # the script will block here until the crawling is finished

    print('Crawling complete.')

    bucket = 'my-versioning-app'
    key = 'output.xml'

    print("Copying object to S3: '%s/%s'..." % (bucket, key))
    client = boto3.client('s3', region_name='ap-southeast-2')
    client.put_object(Bucket=bucket, Key=key, Body=open('/tmp/output.xml', 'rb'))
    print("Done.")

if __name__ == "__main__":
    handler('', '')
