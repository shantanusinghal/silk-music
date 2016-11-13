import scrapy


class AmazonMusicSpider2(scrapy.Spider):
    name = "AmazonMusic2"
    start_urls = [
        'https://www.amazon.com/gp/search/other/ref=lp_625092011_sa_p_lbr_music_artists_?rh=n%3A163856011%2Cn%3A%21624868011%2Cn%3A625092011&bbn=625092011&pickerToList=lbr_music_artists_browse-bin&ie=UTF8&qid=1475988933'
    ]
    count = 0

    def parse(self, response):
        artist_pages = "https://www.amazon.com" + response.css('div#ref_3458810011 ui li span a.link_emph:: attr(href)').extract_first()
        for artist_page in artist_pages:
            yield scrapy.Request(url=artist_page, callback=self.get_the_album_page)

    def get_the_album_page(self, response):
        album_pages = "https://www.amazon.com" + response.css('div#centerPlus div.a-row a-spcaing-mini a::attr(href)').extract()
        for album_page in album_pages:
            yield scrapy.Request(url=album_page, callback=self.parse_album_page)

    def parse_album_page(self, response):
        song_page_links = [link.strip() for link in response.css('ul#s-results-list-atf li div.a-row a-spacing-none a::attr(href)').extract()]
        for song_page in song_page_links:
            yield scrapy.Request(url=song_page, callback=self.parse_song_page)

    def parse_song_page(self, response):
        artist = response.css("div#ArtistLinkSection a ::text").extract_first()
        album_name = response.css("div#title_feature_div h1 ::text").extract_first()
        all_track_names = response.xpath("//td[starts-with(@id,'dmusic_tracklist_track_title')]/span[1]/div/a/text()").extract()
        all_track_durations = [time.strip() for time in response.xpath("//td[starts-with(@id,'dmusic_tracklist_duration')]/span/text()").extract()]
        all_track_prices = [price.strip() for price in response.xpath("//a[starts-with(@id,'dmusic_tracklist_player_buy_button')]/span/text()").extract()]
        all_track_popularity = [len(r.xpath("./div[contains(@class, 'barOn')]").extract())/15.0 * 5 for r in response.xpath("//td[starts-with(@id,'dmusic_tracklist_popularity')]")]
        release_date =  response.xpath("//*[@id='productDetailsTable']//*[text()[contains(.,'Release Date:')]]/..").extract()[1].split(
            '</strong>')[1].split('</li>')[0].strip()
        label = response.xpath("//*[@id='productDetailsTable']//*[text()[contains(.,'Label:')]]/..").extract()[0].split('</strong>')[1].split('</li>')[0].strip()

        copyright = response.xpath("//*[@id='productDetailsTable']//*[text()[contains(.,'Copyright:')]]/..").extract()[0].split('</b>')[1].split('</li>')[0].strip()

        ANSI = response.xpath("//*[@id='productDetailsTable']//*[text()[contains(.,'ASIN:')]]/..").extract()[0].split('</b>')[1].split('</li>')[0].strip()

        with open('amazon/' + artist + '_' + album_name + '.html', 'wb') as f:
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
                'Genres': 'Pop',
                'Released': release_date,
                'Label': label,
                'Copyright': copyright,
                'ASIN': ANSI

            }

