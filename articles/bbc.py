import feedparser
import datetime
import time
from articles import func_editor

# Function to check for political news from BBC
def func_bbc_newsroom(themes, history_articles = str, interval = int):

    BBCFeed = feedparser.parse("http://feeds.bbci.co.uk/news/politics/rss.xml")

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Checking Politics News from BBC")
    entry = BBCFeed.entries[0]
    description = entry.description
    if entry.title not in history_articles:
        if description.lower() in themes:
            print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Processing article from BBC: "+entry.title)

            if 'VIDEO: ' not in entry.title and 'watch the video' not in entry.title and 'Podcast:' not in entry.title and 'live:' not in entry.link:
                func_editor(entry, 'BBC')
                print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Waiting predefined time")
                time.sleep(interval) 
            else:
                print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Article with video, skipping...")
