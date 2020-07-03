# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


# import scrapy


# class QuotesSpider(scrapy.Spider):
#     name = "lyrics"
#     start_urls = [
#         'http://www.ananmanan.lk/sinhala-lyrics/lyric-unicode/3333/athula-adikari-mage-wela.html',
#         'http://www.ananmanan.lk/sinhala-lyrics/lyric-unicode/3339/ridma-weerawardena-kuweni-kuweniye-ma-kuweniye.html',
#     ]

#     def parse(self, response):
#         yield{        
#             'artist': response.css("div h4 a::text").get(),
#             'title': response.css("div h1::text").get().split('-')[0],
#             'lyrics': response.css("div.lyric-unicode::text").getall()
            
#         }


import scrapy
from lyrics.items import LyricsItem


class LyricsSpider(scrapy.Spider):
    name = "lyrics"
    start_urls = [
#         'http://lyricslk.com/lyrics/shihan-mihiranga/1645-aa-sonduru-samanal-viye.html',
#         'http://lyricslk.com/lyrics/milton-mallawarachchi/1590-aadare-mese-kathaa-weev.html',
        'http://lyricslk.com/lyrics/sort/a'
    ]
    def parse(self,response):
        links = response.xpath('//div[@id="links"]/ul/li/a//@href').getall()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_alpha)
        
    def parse_alpha(self, response):
        
        pages = response.xpath('//div[@id="searchNavigation"]/ul/li/a//@href').getall()
        for page in pages:
            yield scrapy.Request(page, callback=self.parse_pages)
            
    def parse_pages(self, response):            
        song_list = response.xpath('//div[@id="SearchResults"]/div[@class="ResBound"]/div[@class="ResTitleSin"]/a//@href').getall()
        for en in song_list:
                yield scrapy.Request(en, callback=self.parse_content)

    def parse_content(self, response):
        item = LyricsItem()
        
        title_info_si = response.xpath('//div[@id="lyricsTitle"]/h2/text()').get()
        title_info_en = response.xpath('//div[@id="lyricsTitle"]/h1/text()').get()
        item['title_si'] = title_info_si.split(' - ')[0]
        item['artist_si'] = title_info_si.split(' - ')[1]
        item['title_en'] = title_info_en.split(' - ')[0]
        item['artist_en'] = title_info_en.split(' - ')[1]
        
        lyrics_body = response.xpath('//div[@id="lyricsBody"]/text()').getall()
        content =''
        for line in lyrics_body:
            content += line.split('\n')[1] + ' '
        
        item['lyrics_raw'] = lyrics_body
        item['lyrics_content'] = content
        item['author'] = response.xpath('//div[@class="lyricsInfo"]/span[@class="infInfo"]/text()').getall()[1].split(': ')[1]
        
        yield item
        
