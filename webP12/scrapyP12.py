import scrapy 
from scrapy.crawler import CrawlerProcess

class spiderP12(scrapy.Spider):
    name = 'spiderP12'
    allowed_domains = ['pagina12.com.ar']
    custom_settings = {'FEED_FORMAT':'json', 
                       'FEED_URI': 'results.json',
                       'FEED_EXPORT_ENCODING': 'utf-8',
                       'DEPTH_LIMIT': 2}
    
    start_urls = ['https://www.pagina12.com.ar/secciones/el-pais',
                  'https://www.pagina12.com.ar/secciones/economia',
                  'https://www.pagina12.com.ar/secciones/sociedad',
                  'https://www.pagina12.com.ar/suplementos/cultura-y-espectaculos',
                  'https://www.pagina12.com.ar/secciones/el-mundo',
                  'https://www.pagina12.com.ar/secciones/deportes',
                  'https://www.pagina12.com.ar/secciones/contratapa']
    
    def parse(self, response):
        #Principal article 
        principal_news = response.xpath('//div[@class = "featured-article__container"]/h2/a/@href').get()
    
        if principal_news is not None:
            yield response.follow(principal_news, callback = self.parse_news)
        
        #News List 
        news = response.xpath('//ul[@class = "article-list"]//li//h2//a/@href').getall()
        for new in news:
            if new:
                yield response.follow(new, callback = self.parse_news)
         
        #Link to next page 
        next_page = response.xpath('//a[@class = "pagination-btn-next"]/@href').get()
        
        if next_page:
            yield response.follow(next_page, callback = self.parse)
        
                
    
    def parse_news(self, response):
        #get title 
        
        title = response.xpath('//div[@class = "article-titles"]/h1/text()').get()
       
            
        #get date 
        
        date = response.xpath('//div[@class = "time"]/span/@datetime').get()
        
           
            
        #get prefix
        
        prefix = response.xpath('//div[@class = "article-titles"]/h2/text()').get()
        
            
        #get summary
         
        summary = response.xpath('//div[@class = "article-summary"]/text()').get()
        
            
        #get text
        
        text = ' '.join(response.xpath('//div[@class = "article-text"]//p/text()').getall())
        
        #get main image 
        
        #image  = response.xpath('//div[@class = "article-main-media-image"]//image)').getall()[-1]
            
        
        yield {'url':response.url,
               'title': title,
               'date': date,
               'prefix': prefix,
               'summary': summary,
               'text': text,}
               #'urlImage': image}
            




if __name__ == '__main__': 
    process = CrawlerProcess()
    process.crawl(spiderP12)
    process.start()