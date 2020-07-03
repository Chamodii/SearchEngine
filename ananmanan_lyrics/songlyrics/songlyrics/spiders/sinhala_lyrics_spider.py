# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


import scrapy
from songlyrics.items import SonglyricsItem

class SongLyricsSpider(scrapy.Spider):
    name = "songlyrics"
    start_urls = [
        'http://www.ananmanan.lk/sinhala-lyrics/page/1'
    ]
    
    def parse(self, response):
        base_url = 'http://www.ananmanan.lk/sinhala-lyrics/page/'
        for i in range(1,6):
            page_url = base_url + str(i)
            yield scrapy.Request(page_url, callback=self.parse_songs)
        
    def parse_songs(self, response):
        songs = response.xpath('//div[@id="content"]/div[@class="mp3"]/a//@href').getall()
        for song in songs:
            song_url = 'http://www.ananmanan.lk/sinhala-lyrics/' + song[3:]
            yield scrapy.Request(song_url, callback=self.parse_download)

            
    def parse_download(self, response):
        download_url = response.xpath('//div[@id="download"]/a//@href').get()
        unicode = response.xpath('//div[@id="more"]/a//@href').get()[5:]
        unicode_url = 'http://www.ananmanan.lk/sinhala-lyrics' + unicode

        # yield scrapy.Request(unicode_url, callback=self.parse_lyrics)
        yield scrapy.Request(download_url, callback=self.parse_stats)


    def parse_stats(self,response):
        item = SonglyricsItem()
        title_header = response.xpath('//div[@class="mp3downloadheader"]/h1/text()').get()
        stats = response.xpath('//div[@class="stats"]/strong/text()').getall()
        size = response.xpath('//div[@class="downloadicon"]/text()').getall()[1]
        extra_stats = response.xpath("//div[contains(@class, 'songdetailsgp')]//div[contains(@class, 'songdetail')]/descendant::text()").getall()
        stat_date_added = stats[0]
        stat_downloads = stats[1]
        stat_listens = stats[2]
        item['title_en'] = title_header.split('-')[0].strip()
        item['artist_en'] = title_header.split('-')[1].strip()
        item['size'] = size
        item['date'] = stat_date_added
        item['downloads'] = stat_downloads
        item['plays'] = stat_listens
        
        if(len(extra_stats) == 8):
            item['lyricist'] = extra_stats[5]
            item['musician'] = extra_stats[7]
        elif(len(extra_stats) == 6):
            if(extra_stats[4] == "Lyrics"):
                item['lyricist'] = extra_stats[5]
                item['musician'] = ""
            else:
                item['lyricist'] = ""
                item['musician'] = extra_stats[5]

        else:
            item['lyricist'] = ""
            item['musician'] = ""

        yield item       
        
    def parse_lyrics(self, response):
        yield{        
            'artist': response.css("div h4 a::text").get(),
            'title': response.css("div h1::text").get().split('-')[0].strip(),
            'lyrics': response.css("div.lyric-unicode::text").getall()
        }