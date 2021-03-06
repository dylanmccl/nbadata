import scrapy
from scrapy.http.headers import Headers
import json
from nba.items import PlayerLinkItem
from urlparse import urljoin

class NbaSpider(scrapy.Spider):
    name = "nba"
    start_urls = ["http://stats.nba.com/players/"]
   # RENDER_HTML_URL = "http://localhost:8050/render.html"
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,self.parse,meta={'splash':{
                'args':{'wait':0.5,
                        'js_source':'angular.element("#main-container > div:nth-child(2) > div > div.row > div > div > div.stat-table > div.title > div > div.col-md-6.col-sm-6.search-col > div > div > a:nth-child(2)").trigger("click");'},
                'endpoint':'render.html'}})
            
                                                      
                
    def parse(self,response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)
       # for sel in response.xpath('//a[@class="active"]'):
        #    item = PlayerLinkItem()
         #   item['url']= sel.xpath('@href').extract()
          #  item['name']= sel.xpath('text()').extract()
           # item['status']=['active']
           # yield item
        for sel in [response.xpath('//a[@class="historic"]')[0]]:
            item = PlayerLinkItem()
            item['url']=[ urljoin('http://stats.nba.com/',sel.xpath('@href').extract()[0]+'career/')]
            item['name']= sel.xpath('text()').extract()
            item['status']=['historic']
            url = item['url'][0]
            item['uid']=int(url.split('/')[-3])
            yield item
            #request = scrapy.Request(url,self.parse_historic,meta={'splash':{
             #   'args':{'wait':0.5
              #      },
               # 'endpoint':'render.html'}})
            #request.meta['uid'] = item['uid']
            #yield request
           # yield scrapy.Request(url,self.parse_historic,meta={'splash':{
            #    'args':{'wait':1,
             #           },
              #  'endpoint':'render.html'}})
           # yield scrapy.Request(url,self.parse_historic ,meta={'splash':{
            #    'args':{'wait':0.5},
             #   'endpoint':'render.html'}})
           # yield scrapy.Request(url,self.parse_historic, meta={'splash':{
            #     'args':{'wait':0.5},
             #    'endpoint': 'render.html'}})
    def parse_historic(self,response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        
