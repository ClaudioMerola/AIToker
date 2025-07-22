# Default configuration for the AI Video Maker application
SUBTITLE_FONT = 'P052-Bold'
TTS_TOOL = 'Google' # 'MS' or 'Google' or 'TikTok'
AI_TOOL = 'AzureOpenAI' # 'openai' or 'azureopenai'
AI_PROMPT = 'write a summary ready to be posted online (without anything extra besides the text) of this article with no more than 220 words mentioning the source name: '
PATH_TO_HISTORY_FILE = "F:\\history.txt"  # Path to the history file where processed articles are stored
PATH_VIDEO_OUTPUT = "F:\\toker\\videos\\"  # Path to the output directory for videos
PATH_BACKGROUND_VIDEOS = "F:\\toker\\background\\"  # Path to the directory containing background videos
PATH_TO_SCREENSHOT = "F:\\"  # Path to the directory for storing screenshots of news articles
BACKGROUND_VIDEOS_COUNT = 5 # Number of YouTube videos to randomly select from for background video generation

# This variable is used to filter the news articles based on themes for news channels that don't have a specific political RSS feed.
NEWS_THEMES = ['politics', 'elections', 'trump', 'democrat', 'republican', 'far-right', 'senator', 'senate', 'congress', 'congressman', 'congresswoman', 'political news', 'political party', 'political election']

COOKIE_LIST = [{"domain": ".nytimes.com", "path": "/", "name": "nyt-geo", "value": "US"},
                #{"domain": ".nytimes.com", "path": "/", "name": "nyt-purr", "sameSite": "Lax" ,"value": "cfhhpnahhcdlhclssdds2fdnd"},
                {"domain": ".nytimes.com", "path": "/", "name": "nyt-gdpr" ,"value": "0"},
                {"domain": ".nytimes.com", "path": "/", "name": "nyt-traceid" ,"value": "0000000000000000634c4a2bcc36f419"},
                {"domain": ".nytimes.com", "path": "/", "name": "nyt-us" ,"value": "0"}]

##################### TEXT TO SPEECH #####################

# IF using Text-to-Speech from TikTok, set the following variables:

TIKTOK_SESSION_ID = ''
TIKTOK_VOICE = 'en_us_006'

# IF using Microsoft Azure for Text-to-Speech, set the following variables:

AZURE_SUBSCRIPTION_KEY = ""
AZURE_REGION = "eastus"  # Replace with your Azure region
AZURE_VOICE = "pt-BR-YaraNeural"  # Replace with your desired Azure voice


##################### TEXT GENERATION CONFIGURATION #####################

# IF using Azure OpenAI for Text Generation, set the following variables:

AZURE_ENDPOINT = "https://*****.openai.azure.com/"
AZURE_API_KEY = ""
AZURE_API_VERSION = ""

# IF using OpenAI for Text Generation, set the following variables:

OPENAI_ORGANIZATION = ""
OPENAI_API_KEY = ""
