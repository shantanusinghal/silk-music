import scrapy


class AmazonMusicSpider(scrapy.Spider):
    name = "appleMusic"
    start_urls = [
        'https://www.amazon.com/Pop/b?ie=UTF8&node=625092011'
    ]

    def parse(self, response):
        best_selling_albums_page_link = "https://www.amazon.com" + response.css("#acsRWns_38e591f5-5cd1-3653-90b7-129de67075c4 div div a.link_emph::attr(href)").extract_first()
        yield scrapy.Request(url=best_selling_albums_page_link, callback=self.collect_album_pages_and_parse)

    def collect_album_pages_and_parse(self, response):
        album_pages = response.css('div#zg_paginationWrapper ol li.zg_page a::attr(href)').extract()
        for album in album_pages:
            yield scrapy.Request(url=album, callback=self.parse_album_page)

    def parse_album_page(self, response):
        song_page_links = [link.strip() for link in response.css("div.zg_itemImmersion div.zg_title a::attr(href)").extract()]
        for song_page in song_page_links:
            yield scrapy.Request(url=song_page, callback=self.parse_song_page)

    def parse_song_page(self, response):
        artist = response.css("div#ArtistLinkSection a ::text").extract_first()
        album_name = response.css("div#title_feature_div h1 ::text").extract_first()
        all_track_names = response.xpath("//td[starts-with(@id,'dmusic_tracklist_track_title')]/span[1]/div/a/text()").extract()
        all_track_durations = [time.strip() for time in response.xpath("//td[starts-with(@id,'dmusic_tracklist_duration')]/span/text()").extract()]
        all_track_prices = [price.strip() for price in response.xpath("//a[starts-with(@id,'dmusic_tracklist_player_buy_button')]/span/text()").extract()]
        with open('amazon/' + artist + '_' + album_name + '.html', 'wb') as f:
            f.write(response.body)
        for track_name, track_duration, track_price in zip(all_track_names, all_track_durations, all_track_prices):
            yield {
                'Artist': artist,
                'TrackName': track_name,
                'Album': album_name,
                'Time': track_duration,
                'Price': track_price,
                'Rating': '',
                'Genres': 'Pop',
                'Released': '',
                'Copyright': ''
            }

