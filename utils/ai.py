import datetime
import openai
from openai import AzureOpenAI
import config

# Function to call OpenAI's API to get a summary of the news.
def func_openai(aiprompt: str, link: str):

    openai.organization = config.OPENAI_ORGANIZATION
    openai.api_key = config.OPENAI_API_KEY

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Calling OpenAI")
    chat_completion = openai.chat.completions.create(model="gpt-4.1", messages=[{"role": "user", "content": aiprompt}])

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Getting response from OpenAI")
    return chat_completion.choices[0].message.content

# Function to call Azure OpenAI's API to get a summary of the news.
def func_azureopenai(aiprompt: str, link: str):

    client = AzureOpenAI(
        azure_endpoint=config.AZURE_ENDPOINT,
        api_key=config.AZURE_API_KEY,
        api_version=config.AZURE_API_VERSION,
    )

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Invoking Azure OpenAI")
    chat_completion = client.chat.completions.create(model="gpt-4.1", messages=[{"role": "system", "content": aiprompt}])

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Getting response from Azure OpenAI")
    return chat_completion.choices[0].message.content
