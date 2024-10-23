import os
# from dotenv import load_dotenv
from supabase import create_client, Client
from itemadapter import ItemAdapter
from datetime import datetime, timedelta

# Load environment variables from .env file
# load_dotenv()

SUPABASE_URL = os.getenv("SUPABASEURL")
SUPABASE_KEY = os.getenv("SUPABASEKEY")

class NewsScraperPipeline:
    def open_spider(self, spider):
        # Create Supabase client
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Cleanup old news when the spider opens
        self.delete_old_news(spider)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Prepare the data to be inserted
        data = {
            "title": adapter.get('title'),
            "link": adapter.get('link'),
            "date": adapter.get('date'),  # Ensure this matches the format expected in Supabase
            "description": adapter.get('description'),
            "source": adapter.get('source')
        }

        # Insert the data into Supabase
        try:
            response = self.supabase.table('news').insert(data).execute()
            if response.status_code != 200:
                spider.logger.error(f"Error inserting data: {response}")
        except Exception as e:
            spider.logger.error(f"Error inserting into Supabase: {e}")

        return item

    def delete_old_news(self, spider):
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        try:
            # Perform the deletion
            response = self.supabase.table('news').delete().lt('date', one_day_ago).execute()
            if response.status_code == 200:
                spider.logger.info("Old news deleted successfully")
            else:
                spider.logger.error(f"Error deleting old news: {response.error}")
        except Exception as e:
            spider.logger.error(f"An exception occurred while deleting old news: {str(e)}")
