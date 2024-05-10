import requests
import re
import json
import scrapy


from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent
from config import API_KEY

# pattern = r'https://goldapple\.ru/(\d+)'



# urls = 

# result_links = set()
# for url in ['https://goldapple.ru/sitemap-{}.xml'.format(i) for i in range (1, 7)]:
#     response = requests.get(
#         url = url
#     )
#     links = re.findall(
#         r'<loc>(.*?)</loc>', response.text
#     )
#     for link in links:
#         result_links.add(link)
#     print ("+1")



        

# new_result = [
#     "https://goldapple.ru/front/api/catalog/product-card?itemId={}&cityId=0c5b2444-70a0-4932-980c-b4dc0d3f02b5&customerGroupId=0".format(re.match(pattern, link)[1]) 
#     for link in result_links if re.match(pattern, link) is not None
# ]
# for link in new_result:
#     response = requests.get(
#         url = link,
#         headers = {
#             'user-agent' : UserAgent().random
#         }
#     )
#     print (response.json())




class GoldAppleSpider(scrapy.Spider):
    name = 'goldApple'
    pattern = re.compile(r'https://goldapple\.ru/(\d+)')

    custom_settings = {
        'FEEDS' : {
            'result.json' : {
                'format' : 'json',
                'overwrite' : True,
                'encoding' : 'utf-8',
                'indent' : 4,
                'ensure_ascii' : False
            },
            'result.jsonlines' : {
                'format' : 'jsonlines',
                'overwrite' : True,
                'encoding' : 'utf-8'
            }
        },
        'CONCURRENT_REQUESTS' : 100,
        "CONCURRENT_REQUESTS_PER_DOMAIN" : 90,
        'LOG_FILE' : 'goldApple.log',
        'LOG_FILE_APPEND' : False

    }

    def start_requests(self):
        for url in ['https://goldapple.ru/sitemap-{}.xml'.format(i) for i in range (1, 2)]:
            yield scrapy.Request(
                url = url,
                callback = self.sitemap,
                meta = {
                    'proxy' : 'http://arsenijbrezgin1469:08d32b@51.89.125.18:10351'
                }
            )

    def sitemap(self, response):
        urls = re.findall(
            r'<loc>(.*?)</loc>', response.text
        )
        for url in urls:
            match = re.match(self.pattern, url)
            if match is None:
                continue
            else:
                url = "https://goldapple.ru/front/api/catalog/product-card?itemId={}&cityId=0c5b2444-70a0-4932-980c-b4dc0d3f02b5&customerGroupId=0".format(match[1])
                yield scrapy.Request(
                    url = url,
                    callback = self.parse,
                    headers = {
                        'user-agent' : UserAgent().random
                    },
                    meta = {
                        'proxy' : 'http://arsenijbrezgin1469:08d32b@51.89.125.18:10351'
                    }
                    
                )

    def parse(self, response):
        data = response.json()
        yield data



    




if __name__ == '__main__':
    process = CrawlerProcess(Settings())
    process.crawl(GoldAppleSpider)
    process.start()



