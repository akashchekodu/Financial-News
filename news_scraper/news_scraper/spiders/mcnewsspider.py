import scrapy
from news_scraper.items import News

class MCNewsSpider(scrapy.Spider):
    name = "mcnewsspider"
    allowed_domains = ["moneycontrol.com"]
    start_urls = ["https://www.moneycontrol.com/news/news-all/"]

    # Maximum number of pages to scrape
    max_pages = 4
    current_page = 1  # Initialize the current page counter

    custom_settings = {
        'FEEDS': {
            'mcnewsdata.json': {'format': 'json', 'overwrite': False}
        }
    }

    def parse(self, response):
        # Select all news list items
        elements = response.css('li.clearfix')

        for element in elements:
            item = News()

            # Extract title
            title = element.css('h2 a::text').get()
            item['title'] = title.strip() if title else None

            # Extract link
            link = element.css('h2 a::attr(href)').get()
            item['link'] = response.urljoin(link) if link else None

            # Extract date if available
            date = element.css('span::text').get()  # Update the selector if necessary
            item['date'] = date.strip() if date else None

            # Extract description
            description = element.css('p::text').get()  # Getting the first paragraph's text
            item['description'] = description.strip() if description else None

            # Extract source
            item['source'] = "Money Control"

            yield item

        # Handle pagination, limiting to max_pages
        if self.current_page < self.max_pages:
            # Find the next page link
            next_page = response.css('a.last::attr(href)').get()  # Update selector if necessary

            if next_page:
                self.current_page += 1  # Increment the page counter
                # Construct the full URL for the next page
                next_page_url = response.urljoin(next_page)
                yield response.follow(next_page_url, self.parse)
