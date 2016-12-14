import os
os.system("scrapy crawl amazonMusicNew -o new.csv")
# from twisted.internet import reactor
#
# import scrapy
# from scrapy.utils.project import get_project_settings
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from tutorial.spiders.amazon_music_spider_new import AmazonMusicSpiderNew
#
#
# def run():
#
#     settings = get_project_settings()
#     settings.set('FEED_FORMAT', 'csv')
#     settings.set('FEED_URI', 'tmp.csv')
#
#     configure_logging()
#     runner = CrawlerRunner(settings)
#     # runner.crawl(AppleMusicSpider)
#     runner.crawl(AmazonMusicSpiderNew)
#
#     d = runner.join()
#     d.addBoth(lambda _: reactor.stop())
#
#     reactor.run()  # the script will block here until all crawling jobs are finished
#
# if __name__ == '__main__':
#     run()
