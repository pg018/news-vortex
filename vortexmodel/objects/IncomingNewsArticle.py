from datetime import datetime
from utils.processing_utils import get_parsed_date_article, get_str_date


class IncomingNewsArticle:
    """This object is for the incoming articles from news api. Converted from json to proper object"""

    def __init__(self, article_json_obj) -> None:
        # private properties
        self.__author: str = article_json_obj["author"]
        self.__title: str = article_json_obj["title"]
        self.__url: str = article_json_obj["url"]
        self.__url_to_image: str = article_json_obj["urlToImage"]
        self.__published_at: datetime = get_parsed_date_article(
            article_json_obj["publishedAt"]
        )

    def get_author(self) -> str:
        return self.__author

    def get_title(self) -> str:
        return self.__title

    def get_url(self) -> str:
        return self.__url

    def get_url_to_image(self) -> str:
        return self.__url_to_image

    def get_published_at(self) -> datetime:
        return self.__published_at

    def __str__(self) -> str:
        return (
            "Author = "
            + self.get_author()
            + "\nTitle = "
            + self.get_title()
            + "\nURL = "
            + self.get_url()
            + "\nURL To Image = "
            + self.get_url_to_image()
            + "\nPublished At = "
            + get_str_date(self.get_published_at())
            + "\n"
        )
