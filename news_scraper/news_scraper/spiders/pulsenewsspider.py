import scrapy
from news_scraper.items import News

class PulseNewsSpider(scrapy.Spider):
    name = "pulsenewsspider"
    allowed_domains = ["pulse.zerodha.com"]
    start_urls = ["https://pulse.zerodha.com"]

    custom_settings = {
        'FEEDS' : {
            'newsdata.json' : {'format' : 'json', 'overwrite' : False}
        }
    }

    # user_agent_list = [
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    # ]


    def parse(self, response):
        elements = response.css('li.box.item')

        for element in elements:
            item = News()

            # Extract title, assign None if missing
            title = element.css('h2.title a::text').get()
            item['title'] = title.strip() if title else None

            # Extract link, assign None if missing
            link = element.css('h2.title a::attr(href)').get()
            item['link'] = response.urljoin(link) if link else None

            # Extract date, assign None if missing
            date = element.css('span.date::text').get()
            item['date'] = date.strip() if date else None

            # Extract description, assign None if missing
            description = element.css('div.desc::text').get()
            item['description'] = description.strip() if description else None

            # Extract source, assign None if missing
            source = element.css('span.feed::text').get()
            item['source'] = source.strip() if source else None

            yield item
