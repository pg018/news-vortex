from httpx import HTTPError
import os
import json
from utils.processing_utils import get_parsed_date_article
from vortexmodel.objects.IncomingNewsArticle import IncomingNewsArticle
from vortexmodel.objects.OutgoingNewsArticle import OutgoingNewsArticle
from vortexmodel.get_newsapi.get_news_api import GetNewsApi
from vortexmodel.preprocessing.preprocessing_main import Preprocessing
from vortexmodel.processing.scrape_content import ScrapeContent
from vortexmodel.processing.summarize_content import SummarizeContent


class Processing:
    def __init__(self, user_prompt: str) -> None:
        self.entered_prompt = user_prompt
        self.script_directory = os.path.dirname(os.path.realpath(__file__))
        self.tfidf_json_path = os.environ["TFIDF_SAVE_PATH"]
        with open(self.tfidf_json_path, "r") as file:
            json_content = file.read()
        self.tfidf_vector = json.loads(json_content)
        self.preprocessing_object = Preprocessing(user_prompt)
        self.no_articles = int(os.environ["NO_FINAL_ARTICLES"])

    async def get_news_articles(self, keyword_prompt_str: str):
        """Creates News Api Object. Asynchronously Returns json object with news articles."""
        news_api = GetNewsApi(keyword_prompt_str)
        return await news_api.get_all_news()

    def get_top_articles(self, news_json_object):
        """
        Sorting the articles in descending order based on publishedAt (dates)
        Return Value - Json List of articles of length 10 or less
        """
        # sorting the articles based on publishedAt in descending order
        sorted_articles = sorted(
            news_json_object["articles"],
            key=lambda x: get_parsed_date_article(
                x["publishedAt"]
            ),  # date is in specific format
            reverse=True,
        )
        # if the length is less than the given, we return all the articles
        if len(sorted_articles) < self.no_articles:
            return sorted_articles

        return sorted_articles[: self.no_articles]

    def objectify_articles(self, articles) -> list[IncomingNewsArticle]:
        """
        The incoming list of json is converted to structured objects list
        Return Value - List of object IncomingNewsArticle
        """
        object_list: list[IncomingNewsArticle] = []
        for article_json in articles:
            # Creating an object and appending it in the list
            object_list.append(IncomingNewsArticle(article_json))

        return object_list

    async def summarize_articles(
        self, articles_list: list[IncomingNewsArticle]
    ) -> list[OutgoingNewsArticle]:
        """This function creates a final list of articles that will be sent to the end user"""
        final_list = []
        for article_obj in articles_list:
            # retrieving the raw content for each article
            scrape_content_obj = ScrapeContent(article_obj.get_url())
            scrapped_dict = await scrape_content_obj.get_final_scraped_content()
            # got the final scrapped text for an article
            scrapped_text = scrapped_dict["scrapped_text"]
            # generated a summary based on tfidf
            summary = SummarizeContent(
                scrapped_text, self.tfidf_vector
            ).extract_summary()
            # there are some duplications in the sentences as the data was raw
            line_divided_summary = "\n".join(
                [sentence.strip() for sentence in summary.split(".")]
            )
            line_divided_summary = scrape_content_obj.remove_duplicated_lines(
                line_divided_summary
            )
            # getting the final summary
            final_summary = ".".join(
                [s.strip() for s in line_divided_summary.split("\n")]
            )
            # creating a final outgoing object to be given
            final_obj = OutgoingNewsArticle(
                article_obj.get_title(),
                article_obj.get_url(),
                final_summary,
                article_obj.get_url_to_image(),
                article_obj.get_published_at(),
                article_obj.get_author(),
            )
            final_list.append(final_obj)

        return final_list

    def serialize_outgoing_article_obj(self, object):
        if isinstance(object, OutgoingNewsArticle):
            return object.__dict__
        else:
            raise TypeError(
                f"Object of type {object.__class__.__name__} is not JSON serializable"
            )

    async def processing_main(self):
        """
        This is the main processing function.
        It runs a pipeline of processes which in the end gives us the list of articles with
        abstract summary
        """
        try:
            # Getting the keyword prompt
            # keyword_prompt = self.preprocessing_object.preprocess_prompt()
            # getting all the news articles
            articles = await self.get_news_articles(self.entered_prompt)
            # getting the top 10 articles based on publishedAt property
            top_articles = self.get_top_articles(articles)
            # creating a structured list of objects for articles
            article_obj_list = self.objectify_articles(top_articles)
            summary_list = await self.summarize_articles(article_obj_list)
            print(f"Number of News Articles: {len(summary_list)}")
            with open(os.environ["RESULT_SAVE_PATH"], "w") as result_file:
                result_file.write(
                    json.dumps(
                        summary_list,
                        indent=2,
                        default=self.serialize_outgoing_article_obj,
                    )
                )
            return summary_list
        except HTTPError:
            return {"error": "Please Check Your Internet Connection!"}
        except Exception as error:
            print(error)
