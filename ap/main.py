from dateutil import parser
import boto3
import json
import logging
import os
import scrapy
from scrapy.exporters import XmlItemExporter
from scrapy.crawler import CrawlerProcess

logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('nose').setLevel(logging.WARNING)


class ApSpider(scrapy.Spider):
    name = "ap"

    def __init__(self, start_urls=[], feed_title='', *args, **kwargs):
      super().__init__(**kwargs)  # python3
      self.start_urls = start_urls
      self.feed_title = feed_title

    def parse(self, response):
        items =  response.xpath('//div[re:test(@class, "^FeedCard")]')
        base_url = 'https://apnews.com'

        yield {
          'description': self.feed_title,
          'link': self.start_urls[0],
          'title': self.feed_title
        }

        for item in items:
            title = item.css('h1::text').get()
            identifier = item.xpath('.//a[re:test(@class, "^Component-headline")]/@href').get('')
            description = item.xpath('.//a[re:test(@class, "^firstWords")]/div/p/text()').get('No description was provided.')
            pub_date = item.xpath('.//span[re:test(@class, "^Timestamp Component")]/@data-source').get()

            # Fri, 13 Dec 2019 18:56:20 +0000
            if not title or not identifier or not pub_date:
              continue
            pub_date_formatted = parser.parse(pub_date).strftime('%a, %d %b %Y %H:%M:%S +0000')

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

    url = event['url']
    title = event['title']
    filename = event['url'].split('-')[-1]

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(settings=crawler_settings)

    print('Starting crawling...')
    process.crawl(ApSpider, start_urls=[url], feed_title=title)
    process.start() # the script will block here until the crawling is finished

    print('Crawling complete.')
    process.stop()

    bucket = os.environ['BUCKET']
    key = 'output-%s.xml' % (filename)

    print("Copying object to S3: '%s/%s'..." % (bucket, key))
    client = boto3.client('s3', region_name='ap-southeast-2')
    client.put_object(Bucket=bucket, Key=key, Body=open('/tmp/output.xml', 'rb'))
    print("Done.")

if __name__ == "__main__":
    handler('', '')
