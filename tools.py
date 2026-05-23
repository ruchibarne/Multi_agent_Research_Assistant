from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

tavily = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
@tool
def web_search(query: str) -> str:
    '''Search the web for the given query and return the results.'''
    results = tavily.search(query=query, max_results=5)
    out=[]
    for r in results['results']:
        out.append(f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n")
    return "\n--------\n".join(out)
# print(web_search.invoke("What is the current news of war?"))


@tool
def scrape_url(url:str) -> str:
    '''Scrape the content of the given URL and return the text.'''
    try:
        response = requests.get(url, timeout=8, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()
        return soup.get_text(separator=' ', strip=True)[:3000]
    except Exception as e:
        return f"Error scraping URL: {str(e)}"
# print(scrape_url.invoke("https://www.bbc.com/news/articles/cedpz9669deo"))