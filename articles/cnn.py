import feedparser
import datetime
import time
from articles import func_editor

# Function to check for political news from CNN
def func_cnn_newsroom(themes, history_articles = str, interval = int):

    CNNFeed = feedparser.parse("http://rss.cnn.com/rss/edition.rss")

    counter = 0
    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Checking Politics News from CNN")
    while counter < 4:
        entry = CNNFeed.entries[counter]
        description = entry.title
        if entry.title not in history_articles and '/videos/' not in entry.link and '/live-news/' not in entry.link and '/collections/' not in entry.link:
            if description.lower() in themes:
                print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Processing article from CNN: "+entry.title)

                if 'VIDEO: ' not in entry.title and 'watch the video' not in entry.title and 'Podcast:' not in entry.link and 'live:' not in entry.link:
                    func_editor(entry, 'CNN')
                    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Waiting predefined time")
                    time.sleep(interval) 
                else:
                    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Article with video, skipping...")
        counter += 1
