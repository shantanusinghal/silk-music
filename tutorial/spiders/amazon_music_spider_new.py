import scrapy
import re

from scrapy.exceptions import CloseSpider


class AmazonMusicSpiderNew(scrapy.Spider):
    name = "amazonMusicNew"
    pagesScraped = 0
    maxPages = 6000

    def start_requests(self):
        urls = [
            'https://www.amazon.com/Mad-Love-Deluxe-Explicit-JOJO/dp/B01LZ8P95H/ref=sr_1_2?s=dmusic&ie=UTF8&qid=1481512024&sr=1-2&keywords=explicit&refinements=p_n_feature_browse-bin%3A625150011',
            'https://www.amazon.com/Voodoo-Explicit-Twisted-Insane/dp/B015SJMLYK/ref=sr_1_2?s=dmusic&ie=UTF8&qid=1481512268&sr=1-2&keywords=explicit&refinements=p_n_feature_browse-bin%3A625150011%2Cp_72%3A1248981011',
            'https://www.amazon.com/dp/B01MEEVB2F/ref=sr_1_2_rd?_encoding=UTF8&child=B01M64FYI1&qid=1481744688&sr=1-2%3C/a%3E',
            'https://www.amazon.com/Royalty-Deluxe-Version-Explicit-Chris/dp/B0185OMVBS/ref=sr_1_1?s=dmusic&ie=UTF8&qid=1481744762&sr=1-1-mp3-albums-bar-strip-0&keywords=Chris+brown+explicit',
            'https://www.amazon.com/dp/B01EDZ9H1U/ref=sr_1_1_rd?_encoding=UTF8&child=B01EDZ9MO2&qid=1481744627&sr=1-1%3C/a%3E'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_song_page)

    def parse_song_page(self, response):
        if self.pagesScraped > self.maxPages:
            raise CloseSpider('Finished scraping %s pages' % self.maxPages)
        artist = response.css("div#ArtistLinkSection a ::text").extract_first()
        album_name = response.css("div#title_feature_div h1 ::text").extract_first()
        all_track_names = response.xpath("//td[starts-with(@id,'dmusic_tracklist_track_title')]/span[1]/div/a/text()").extract()
        all_track_durations = [time.strip() for time in response.xpath("//td[starts-with(@id,'dmusic_tracklist_duration')]/span/text()").extract()]
        all_track_prices = [price.strip() for price in response.xpath("//a[starts-with(@id,'dmusic_tracklist_player_buy_button')]/span/text() | //span[starts-with(@id,'dmusic_tracklist_track')]/text()").extract()]
        release_date = response.xpath("//*[@id='productDetailsTable']//*[text()[contains(.,'Release Date:')]]/..").extract()[1].split('</strong>')[1].split('</li>')[0].strip()
        label = response.xpath("//*[@id='productDetailsTable']//*[text()[contains(.,'Label:')]]/..").extract()[0].split('</strong>')[1].split('</li>')[0].strip()
        genres = response.xpath("//*[@id='productDetailsTable']//*[@class='content']//*[text()[contains(.,'Genres:')]]/../div/ul/li/a/text()").extract()
        asin = response.xpath("//*[@id='productDetailsTable']//*[text()[contains(.,'ASIN:')]]/..").extract()[0].split('</b>')[1].split('</li>')[0].strip()
        all_ratings = [len(r.xpath("./div[contains(@class, 'barOn')]").extract())/15.0 * 5 for r in response.xpath("//td[starts-with(@id,'dmusic_tracklist_popularity')]")]
        if len(all_track_names) == 1:
            file_name = 'amazon/' + self.simplify(artist) + '_' + self.simplify(all_track_names[0]) + '.html'
        else:
            file_name = 'amazon/' + self.simplify(artist) + '_' + self.simplify(album_name) + '.html'
        with open(file_name, 'wb') as f:
            f.write(response.body)
        for track_name, track_duration, track_price, rating in zip(all_track_names, all_track_durations, all_track_prices, all_ratings):
            self.pagesScraped += 1
            yield {
                'Id': 'd_%s' % self.pagesScraped,
                'Artist': artist,
                'TrackName': track_name,
                'Album': album_name,
                'Time': track_duration,
                'Price': track_price,
                'Rating': rating,
                'Genres': genres,
                'Released': release_date,
                'Label': label
            }

    @staticmethod
    def simplify(string):
        return re.sub('[^A-Za-z0-9 ]+', '', string)
