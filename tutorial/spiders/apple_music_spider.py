import re
import scrapy
from scrapy.exceptions import CloseSpider


class AppleMusicSpider(scrapy.Spider):
    name = "appleMusic"
    pagesScraped = 0
    maxPages = 5000
    start_urls = [
        'https://itunes.apple.com/us/genre/music-pop/id14'
    ]

    # def start_requests(self):
    #     yield scrapy.Request(url='https://itunes.apple.com/us/album/piano-man/id158617297?i=158617575', callback=self.parse_song_page)

    def parse(self, response):
        artist_page_links = response.css("div#selectedcontent div ul li a::attr(href)").extract()
        for artist_page in artist_page_links:
            yield scrapy.Request(url=artist_page, callback=self.parse_artist_page)

    def parse_artist_page(self, response):
        song_page_links = response.css("div[metrics-loc='TrackList'] tbody tr td.name span a::attr(href)").extract()
        for song_page in song_page_links:
            yield scrapy.Request(url=song_page, callback=self.parse_song_page)
        next_page = response.css('div.center-stack div ul.paginate li a.paginate-more::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse_artist_page)

    def parse_song_page(self, response):
        if self.pagesScraped > self.maxPages:
            raise CloseSpider('Finished scraping %s pages' % self.maxPages)
        adam_id = response.url.split('?i=')[1]
        artist = response.css("tr[adam-id='" + adam_id + "'] td:nth-of-type(3) a span ::text").extract_first()
        track_name = response.css("tr[adam-id='" + adam_id + "'] td:nth-of-type(2) span span[class='text'] ::text").extract_first()
        with open('apple/' + self.simplify(artist) + '_' + self.simplify(track_name) + '.html', 'wb') as f:
            f.write(response.body)
        self.pagesScraped += 1
        yield {
            'Id': 's_%s' % self.pagesScraped,
            'Artist': artist,
            'TrackName': track_name,
            'Album': response.css("h1[itemprop='name'] ::text").extract_first(),
            'Time': response.css("tr[adam-id='" + adam_id + "'] td:nth-of-type(4) span span ::text").extract_first(),
            'Price': response.css("tr[adam-id='" + adam_id + "'] td:nth-of-type(5) span span ::text").extract_first(),
            'Rating': response.css("div[id='left-stack'] div div span[itemprop='ratingValue'] ::text").extract_first(),
            'Genres': response.css("div[id='left-stack'] div ul li span[itemprop='genre'] ::text").extract(),
            'Released': response.css("div[id='left-stack'] div ul li span[itemprop='dateCreated'] ::text").extract_first(),
            'Label': response.css("div[id='left-stack'] div ul li.copyright ::text").extract_first()
        }

    @staticmethod
    def simplify(string):
        return re.sub('[^A-Za-z0-9 ]+', '', string)
