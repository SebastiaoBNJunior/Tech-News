import requests
import time
import parsel
import re
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    headers = {"user-agent": "Fake user-agent"}
    time.sleep(1)
    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.RequestException:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = parsel.Selector(html_content)
    news_urls = selector.css('h2.entry-title a::attr(href)').getall()
    return news_urls if news_urls else []


# Requisito 3
def scrape_next_page_link(html_content):
    selector = parsel.Selector(html_content)
    next_page_url = selector.css('a.next.page-numbers::attr(href)').get()
    return next_page_url if next_page_url else None


# Requisito 4
def scrape_news(html_content):
    selector = parsel.Selector(html_content)

    url = selector.css('link[rel="canonical"]::attr(href)').get()
    title = selector.css('h1.entry-title::text').get().strip()
    timestamp = selector.css('li.meta-date::text').get()
    writer = selector.css('span.author a::text').get()
    reading_time_text = selector.css('li.meta-reading-time::text').get()
    reading_time_match = re.search(r'\d+', reading_time_text)
    reading_time = int(reading_time_match.group()) if reading_time_match else 0
    summary = (
        selector.css('div.entry-content > p')
        .xpath('string()')
        .get()
        .strip()
    )
    category = selector.css('span.label::text').get()

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }


# Função para buscar e processar uma página de notícias
def fetch_and_process_page(url, news_list, amount):
    html_content = fetch(url)
    if not html_content:
        return None

    news_urls = scrape_updates(html_content)
    for news_url in news_urls:
        if len(news_list) >= amount:
            break
        news_html_content = fetch(news_url)
        if news_html_content:
            news_data = scrape_news(news_html_content)
            news_list.append(news_data)

    return scrape_next_page_link(html_content)


# Função principal que coordena o processo
def get_tech_news(amount):
    news_list = []
    url = "https://blog.betrybe.com"

    while len(news_list) < amount:
        url = fetch_and_process_page(url, news_list, amount)
        if not url:
            break

    create_news(news_list)
    return news_list
