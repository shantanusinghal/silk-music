# import os
# os.system("scrapy crawl quotes -o quotes.json")
from twisted.internet import reactor

import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
# from tutorial.spiders.apple_music_spider import AppleMusicSpider
from amazon_music_spider2 import AmazonMusicSpider2
from spiders.amazon_music_spider import AmazonMusicSpider


def run():

    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'csv')
    settings.set('FEED_URI', 'result6.csv')

    configure_logging()
    runner = CrawlerRunner(settings)
    runner.crawl(AmazonMusicSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()  # the script will block here until all crawling jobs are finished

if __name__ == '__main__':
    run()
