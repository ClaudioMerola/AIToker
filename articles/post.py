import feedparser
import datetime
import time
from articles import func_editor

# Function to check for political news from Washington Post
def func_washingtonpost_newsroom(themes, history_articles = str, interval = int):

    PostFeed = feedparser.parse("https://feeds.washingtonpost.com/rss/politics?itid=lk_inline_manual_2")

    counter = 0
    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Checking Politics News from Washington Post")
    while counter < 4:
        entry = PostFeed.entries[counter]
        description = entry.title
        if(entry.title not in history_articles and '/videos/' not in entry.link and '/live-news/' not in entry.link and '/collections/' not in entry.link):
            print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Processing article from Washington Post: "+entry.title)

            if('VIDEO: ' not in entry.title and 'watch the video' not in entry.title and 'Podcast:' not in entry.title and 'live:' not in entry.link and 'https://www.washingtonpost.com' != entry.link):
                func_editor(entry, 'ThePost')
                print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Waiting predefined time")
                time.sleep(interval) 
            else:
                print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Article with video, skipping...")
        counter += 1
