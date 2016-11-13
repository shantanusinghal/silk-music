import scrapy
import re

from scrapy.exceptions import CloseSpider

class AmazonMusicSpider(scrapy.Spider):
    name = "AmazonMusic"
    start_urls = [
        'https://www.amazon.com/Pop/b?ie=UTF8&node=625092011',
        'https://www.amazon.com/Dance-DJ/b?ie=UTF8&node=624988011',
        'https://www.amazon.com/RB/b?ie=UTF8&node=625105011',
        'https://www.amazon.com/Rap-Hip-Hop/b?ie=UTF8&node=625117011',
        'https://www.amazon.com/Blues/b?ie=UTF8&node=624881011'
    ]

    maxPages = 5000
    count = 0

    def parse(self, response):
        best_selling_albums_and_songs = ["https://www.amazon.com" + link for link in response.xpath(
            "//div[starts-with(@id,'acsRWns')]/div/div[2]/a/@href").extract()]
        for link in best_selling_albums_and_songs:
            yield scrapy.Request(url=link, callback=self.collect_album_pages_and_parse)

    def collect_album_pages_and_parse(self, response):
        album_pages = response.css('div#zg_paginationWrapper ol li.zg_page a::attr(href)').extract()
        for album in album_pages:
            yield scrapy.Request(url=album, callback=self.parse_album_page)

    def parse_album_page(self, response):
        song_page_links = [link.strip() for link in response.css("div.zg_itemImmersion div.zg_title a::attr(href)").extract()]
        for song_page in song_page_links:
            yield scrapy.Request(url=song_page, callback=self.parse_song_page)

    def parse_song_page(self, response):
        if self.count > self.maxPages:
            raise CloseSpider('Finished scraping %s pages' % self.maxPages)
        artist = response.css("div#ArtistLinkSection a ::text").extract_first()
        album_name = response.css("div#title_feature_div h1 ::text").extract_first()
        all_track_names = response.xpath("//td[starts-with(@id,'dmusic_tracklist_track_title')]/span[1]/div/a/text()").extract()
        all_track_durations = [time.strip() for time in response.xpath("//td[starts-with(@id,'dmusic_tracklist_duration')]/span/text()").extract()]
        all_track_prices = [price.strip() for price in response.xpath("//a[starts-with(@id,'dmusic_tracklist_player_buy_button')]/span/text()").extract()]
        all_track_popularity = [len(r.xpath("./div[contains(@class, 'barOn')]").extract())/15.0 * 5 for r in response.xpath("//td[starts-with(@id,'dmusic_tracklist_popularity')]")]
        release_date = response.xpath("//*[@id='productDetailsTable']//*[text()[contains(.,'Release Date:')]]/..").extract()[0].split(
            '</strong>')[1].split('</li>')[0].strip()
        genres = response.xpath(
            "//*[@id='productDetailsTable']//*[@class='content']//*[text()[contains(.,'Genres:')]]/../div/ul/li/a/text()").extract()
        label = response.xpath("//*[@id='productDetailsTable']//*[text()[contains(.,'Label:')]]/..").extract()[0].split('</strong>')[1].split('</li>')[0].strip()

       # copyright = response.xpath("//*[@id='productDetailsTable']//*[text()[contains(.,'Copyright:')]]/..").extract()[0].split('</b>')[1].split('</li>')[0].strip()

        ANSI = response.xpath("//*[@id='productDetailsTable']//*[text()[contains(.,'ASIN:')]]/..").extract()[0].split('</b>')[1].split('</li>')[0].strip()

        if len(all_track_names) == 1:
            file_name = 'amazon/' + self.simplify(artist) + '_' + self.simplify(all_track_names[0]) + '.html'
        else:
            file_name = 'amazon/' + self.simplify(artist) + '_' + self.simplify(album_name) + '.html'
        with open(file_name, 'wb') as f:
            f.write(response.body)
        for track_name, track_duration, track_price, track_poplarity in zip(all_track_names, all_track_durations, all_track_prices, all_track_popularity
                                                                                          ):
            self.count += 1
            yield {

                'Id': 'z_%s' % self.count,
                'Artist': artist,
                'TrackName': track_name,
                'Album': album_name,
                'Time': track_duration,
                'Price': track_price,
                'Rating': round(track_poplarity,1),
                'Genres': genres,
                'Released': release_date,
                'Label': label,
                'ASIN': ANSI

            }

    @staticmethod
    def simplify(string):
        return re.sub('[^A-Za-z0-9 ]+', '', string)