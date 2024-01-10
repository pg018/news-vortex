import os
import re
from vortexmodel.get_newsapi.get_news_api import GetNewsApi
from vortexmodel.processing.scrape_content import ScrapeContent


class GenerateTrainingData:
    def __init__(self, query: str) -> None:
        self.script_directory = os.path.dirname(
            os.path.abspath(__file__)
        )  # Get the directory of the current script (i.e training_data)
        self.entered_query = query
        self.entered_examples_cnt = int(os.environ["EXAMPLE_NUM_PER_QUERY_GEN_DATA"])

    async def get_articles_url(self):
        """
        Call the news api for articles with query.
        Return Value - Returns a list of IncomingNewsArticle object. Returns entered_examples_cnt articles
        """
        articles_result = await GetNewsApi(self.entered_query).get_all_news()
        final_article_list_url: list[str] = []

        for article_json in articles_result["articles"]:
            # Creating an object and appending it in the list
            final_article_list_url.append(article_json["url"])

        # if already less than the required count
        if len(final_article_list_url) < self.entered_examples_cnt:
            return final_article_list_url
        return final_article_list_url[: self.entered_examples_cnt]

    def extract_number_from_scrapped_file(self, file_name):
        """
        Extracts the unique number in file name scrapped_text_{number}.txt
        Return Value => int (file number identifier)
        """
        match = re.match(r"scrapped_text_(\d+)\.txt", file_name)
        if match:
            return int(match.group(1))
        return 0  # Return 0 for filenames that don't match the pattern

    async def store_scraped_text(self, articles_url_list):
        """
        articles_url_list => list of strings of urls
        The urls are called iteratively and scrapped. The scrapped content is stored in a file.
        The scrapped content file and html file are stored in seperate files respectively.
        Return Value => boolean => Returns true if operation successfully performed
        """
        # path to data folder
        data_folder = os.path.join(self.script_directory, "data")
        # path to content folder in the data folder
        content_folder = os.path.join(data_folder, "content")
        html_folder = os.path.join(data_folder, "html_files")
        # if folder does not exist, creating it
        if not os.path.exists(content_folder):
            os.makedirs(content_folder)
        if not os.path.exists(html_folder):
            os.makedirs(html_folder)
        # getting all the scraped file_names till now
        all_file_name_list = [
            f
            for f in os.listdir(content_folder)
            if os.path.isfile(os.path.join(content_folder, f))
        ]
        # sorting the file names based on the number at the end
        sorted_file_name_list = sorted(
            all_file_name_list, key=self.extract_number_from_scrapped_file
        )
        print("Number of files = " + str(len(sorted_file_name_list)))
        if len(sorted_file_name_list) == 0:
            file_number = 0
        else:
            # extracting the number of the last file
            file_number = self.extract_number_from_scrapped_file(
                sorted_file_name_list[-1]
            )
        for i in range(len(articles_url_list)):
            scrape_obj = ScrapeContent(articles_url_list[i])
            # getting the scraped content for a specific url
            scraped_content_dict = await scrape_obj.get_final_scraped_content()
            # the unique identifier number for the current scrapped content's file
            unique_number = file_number + i + 1
            scrapped_file_path = os.path.join(
                content_folder,
                f"scrapped_text_{unique_number}.txt",
            )
            html_file_path = os.path.join(
                html_folder,
                f"html_{unique_number}.html",
            )
            # storing the html files and scrapped content only if the length is greater than 0
            if len(scraped_content_dict["scrapped_text"].strip()) > 0:
                # for checking if any file has less than 100 characters.
                # also an indicator that the file has been generated
                print(
                    f"{file_number + i + 1} {len(scraped_content_dict['scrapped_text'].strip()) < 100}"
                )
                with open(scrapped_file_path, "w", encoding="utf-8") as file:
                    file.write(scraped_content_dict["scrapped_text"])
                with open(html_file_path, "w", encoding="utf-8") as file:
                    file.write(scraped_content_dict["html_code"])
        return True

    async def generate_data(self):
        """
        This is the main function of the class used as pipeline to run all the tasks to produce
        the training data...
        """
        try:
            all_articles = await self.get_articles_url()
            content = await self.store_scraped_text(all_articles)
            return content
        except UnicodeDecodeError:
            print("Decoding Error")
