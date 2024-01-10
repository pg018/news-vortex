from datetime import datetime


def get_parsed_date_article(str_date: str) -> datetime:
    return datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%SZ")


def get_str_date(parsed_date: datetime) -> str:
    return datetime.strftime(parsed_date, "%d-%m-%Y")
