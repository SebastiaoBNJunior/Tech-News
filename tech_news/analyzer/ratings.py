from collections import Counter
from tech_news.database import find_news


def top_5_categories():
    all_news = find_news({})

    category_count = Counter(
        news['category'] for news in all_news if 'category' in news
    )

    sorted_categories = sorted(
        category_count.items(),
        key=lambda x: (-x[1], x[0])
    )

    top_categories = [
        category for category, count in sorted_categories[:5]
    ]

    return top_categories
