import unittest
from unittest.mock import patch
from tech_news.analyzer.reading_plan import ReadingPlanService


@patch('tech_news.analyzer.reading_plan.find_news')
def test_reading_plan_group_news(mock_find_news):
    # Mock data
    mock_find_news.return_value = [
        {"title": "Notícia 1", "reading_time": 4},
        {"title": "Notícia 2", "reading_time": 3},
        {"title": "Notícia 3", "reading_time": 10},
        {"title": "Notícia 4", "reading_time": 15},
        {"title": "Notícia 5", "reading_time": 12},
    ]

    # Test invalid available_time
    with unittest.TestCase().assertRaises(ValueError):
        ReadingPlanService.group_news_for_available_time(0)

    # Test valid available_time
    result = ReadingPlanService.group_news_for_available_time(10)
    expected_result = {
        "readable": [
            {
                "unfilled_time": 3,
                "chosen_news": [
                    ("Notícia 1", 4),
                    ("Notícia 2", 3),
                ],
            },
            {
                "unfilled_time": 0,
                "chosen_news": [
                    ("Notícia 3", 10),
                ],
            },
        ],
        "unreadable": [
            ("Notícia 4", 15),
            ("Notícia 5", 12),
        ],
    }
    unittest.TestCase().assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
