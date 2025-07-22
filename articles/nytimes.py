import feedparser
import datetime
import time
from articles import func_editor

# Function to check for political news from NYTimes
def func_nytimes_newsroom(themes, history_articles = str, interval = int):

    NYTFeed = feedparser.parse("https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml")

    counter = 0
    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Checking Politics News from NYTimes")
    while counter < 4:
        entry = NYTFeed.entries[counter]
        description = entry.title
        if(entry.title not in history_articles and '/videos/' not in entry.link and '/live-news/' not in entry.link and '/collections/' not in entry.link):        
            print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Processing article from NYTimes: "+entry.title)

            if('VIDEO: ' not in entry.title and 'watch the video' not in entry.title and 'Podcast:' not in entry.title and 'live:' not in entry.link):
                func_editor(entry, 'NYTimes')
                print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Waiting predefined time")
                time.sleep(interval) 
            else:
                print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Article with video, skipping...")
        counter += 1
