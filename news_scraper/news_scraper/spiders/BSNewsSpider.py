import scrapy
from news_scraper.items import News

class BSNewsSpider(scrapy.Spider):
    name = "bsnewsspider"
    allowed_domains = ["business-standard.com"]
    start_urls = ["https://www.business-standard.com/latest-news/"]

    # Maximum number of pages to scrape
    max_pages = 4
    current_page = 1  # Initialize the current page counter

    custom_settings = {
        'FEEDS': {
            'bsnewsdata.json': {'format': 'json', 'overwrite': False}
        }
    }

    def parse(self, response):
        # Select all news list items
        elements = response.css('div.cardlist')

        for element in elements:
            item = News()

            # Extract title
            title = element.css('a.smallcard-title::text').get()
            item['title'] = title.strip() if title else None

            # Extract link
            link = element.css('a.smallcard-title::attr(href)').get()
            item['link'] = response.urljoin(link) if link else None

            # Extract date (adjust selector as needed)
            date = element.css('span.datetime::text').get()
            item['date'] = date.strip() if date else None

            # Extract description (adjust selector as needed)
            description = element.css('div.article-body p::text').getall()
            item['description'] = ' '.join(description).strip() if description else None

            # Extract source
            item['source'] = "Business Standard"

            yield item

        # Handle pagination, limiting to max_pages
        if self.current_page < self.max_pages:
            # Find the next page link
            next_page = response.css('div.Loadmore_loadmorebtn__IVsn_ button.btn a::attr(href)').get()

            if next_page:
                self.current_page += 1  # Increment the page counter
                # Construct the full URL for the next page
                next_page_url = response.urljoin(next_page)
                yield response.follow(next_page_url, self.parse)