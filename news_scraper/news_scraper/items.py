# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class News(scrapy.Item):
    # Define the fields for your item
    title = scrapy.Field()        # Title of the news article
    link = scrapy.Field()         # URL of the article
    date = scrapy.Field()         # Publication date
    description = scrapy.Field()  # Brief description of the article
    source = scrapy.Field()       # Source or feed name
