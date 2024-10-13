from tech_news.database import db
from datetime import datetime


# Requisito 7
def search_by_title(title):
    query = {"title": {"$regex": title, "$options": "i"}}
    news = db.news.find(query)
    result = [(new["title"], new["url"]) for new in news]
    return result


# Requisito 8
def search_by_date(date):
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime(
            "%d/%m/%Y"
        )
    except ValueError:
        raise ValueError("Data inválida")

    query = {"timestamp": formatted_date}
    news = db.news.find(query)
    result = [(new["title"], new["url"]) for new in news]
    return result


# Requisito 9
def search_by_category(category):
    query = {"category": {"$regex": category, "$options": "i"}}
    news = db.news.find(query)
    result = [(new["title"], new["url"]) for new in news]
    return result
