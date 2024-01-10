from datetime import datetime
from utils.processing_utils import get_str_date


class OutgoingNewsArticle:
    """This object is for the outgoing articles"""

    def __init__(
        self,
        title: str,
        source_url: str,
        summarized_content: str,
        image_url: str,
        published_at: datetime,
        author: str = "",
    ) -> None:
        # private properties
        self.__title = title
        self.__source_url = source_url
        self.__summarized_content = summarized_content
        self.__image_url = image_url
        self.__published_at = published_at
        self.__author_name = author

    def get_title(self) -> str:
        return self.__title

    def get_source_url(self) -> str:
        return self.__source_url

    def get_summarized_content(self) -> str:
        return self.__summarized_content

    def get_image_url(self) -> str:
        return self.__image_url

    def get_published_at(self) -> datetime:
        return self.__published_at

    def get_author_name(self) -> str:
        return self.__author_name

    def __str__(self) -> str:
        return (
            "Title - "
            + self.get_title()
            + "\nSource URL - "
            + self.get_source_url()
            + "\nSummarized Content - "
            + self.get_summarized_content()
            + "\nImage URL - "
            + self.get_source_url()
            + "\nPublished Date - "
            + self.get_published_at().isoformat()
            + "\nAuthor Name - "
            + self.get_author_name()
        )

    @property
    def __dict__(self):
        return {
            "title": self.get_title(),
            "source_url": self.get_source_url(),
            "summarized_content": self.get_summarized_content(),
            "image_url": self.get_image_url(),
            "published_at": self.get_published_at().isoformat(),
            "author_name": self.get_author_name(),
        }
