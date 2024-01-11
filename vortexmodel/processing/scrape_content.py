from httpx import AsyncClient
from bs4 import BeautifulSoup
from constants.processing_constants import (
    not_required_tag_list,
    required_tag_list,
    unneccessary_content_list,
)
from vortexmodel.processing.scrape_content_trie import Trie


class ScrapeContent:
    """Class that is used to retrieve the scraped text and its html code"""

    def __init__(self, url: str) -> None:
        self.entered_url = url
        self.remove_tags_list = not_required_tag_list
        self.required_content_tags = required_tag_list

    async def fetch_url(self):
        """Calls the api to fetch the data from the url"""
        async with AsyncClient() as client:
            response = await client.get(
                self.entered_url, headers={"User-Agent": "Mozilla/5.0"}
            )
            return response.content

    async def process_html(self, html_bytes) -> BeautifulSoup:
        """
        The html bytes are decoded to html content which is then used to create beautifulSoup
        object.
        Return Value -> beautifulSoup Object
        """
        html_content = html_bytes.decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html_content, "html.parser")
        return soup

    def filter_html_tags(self, beautiful_soup: BeautifulSoup) -> BeautifulSoup:
        """
        Removing all the html tags and content which is not required from soup object
        Return Value -> Beautiful soup object
        """
        for tag in self.remove_tags_list:
            tag_data_list = beautiful_soup.find_all(tag)
            for tag_data in tag_data_list:
                tag_data.extract()

        return beautiful_soup

    def get_required_content(self, beautiful_soup: BeautifulSoup):
        """
        Iterating over a set of tags and retrieving the data from those tags
        Return value -> Dictionary->
        content-> string value which contains the content extracted
        html_code-> BeautifulSoup Object
        """
        content = []
        for tag_name in self.required_content_tags:
            for tag in beautiful_soup.find_all(tag_name):
                content.append(tag.get_text().strip())

        return {"content": content, "html_code": beautiful_soup}

    def remove_unneccesary_words(self, content_string):
        """
        Iterating over list of unneccessary words and removing them from the content
        Return Value -> Content after removing words (str)
        """
        for c in unneccessary_content_list:
            content_string = content_string.lower().replace(c.lower(), "")

        # Remove duplicates while preserving order
        lines = content_string.splitlines()
        unique_lines = []
        seen_lines = set()
        for line in lines:
            if line.strip() and (line not in seen_lines) and len(line.strip()) >= 3:
                unique_lines.append(line)
                seen_lines.add(line)
        return "\n".join(unique_lines)

    def get_formatted_string(self, lines_arr: str) -> str:
        """
        Returns the final format in which we want our output to be
        IMP - Do not make changes here. This may break the code.
        """
        return "\n".join(line for line in lines_arr.splitlines() if line.strip())

    def get_updated_lines_list(self, content_string: str) -> list:
        """
        This is a helper function for functions =>
        1) remove_duplicated_lines
        2) remove_duplicated_phrases
        It splits the content into array of lines.
        Return Value => [[line, line_index]] =>
        a) line => line string,
        b) line_index => index of the line
        """
        lines = content_string.splitlines()  # getting an array of lines
        index = 0  # used to record the position of lines (line number) [0-indexed]
        updated_lines = []
        for line in lines:
            # appending the line along with index of the line
            updated_lines.append([line, index])
            index += 1
        """
        sorting based on the decreasing length of line.
        If length is same then sorted ascending based on the index number
        """
        updated_lines.sort(key=lambda x: (-len(x[0]), x[1]))
        return updated_lines

    def remove_duplicated_lines(self, text):
        """
        Used to remove the duplicated lines in the scraped content
        In the scraped content, there are lines where the content is duplicated upto certain point.
        The longer line has some extra text compared to the shorter line.
        We remove the shorter line from this function.
        Summary => Removing subsequence lines from the scraped content
        """
        trie = Trie()
        unique_lines = []
        updated_lines = self.get_updated_lines_list(text)

        for uline in updated_lines:
            stripped_line = uline[0].strip()
            bool_val, _ = trie.search(stripped_line.strip())
            # if the line does not exist in the trie
            if not bool_val:
                # adding it to trie
                trie.insert(stripped_line)
                # adding to our final string as it is unique
                unique_lines.append(uline)

        # sorting the unique lines based on the index in ascending order
        unique_lines.sort(key=lambda x: x[1])

        final_string = ""
        for string, _ in unique_lines:  # [(string, index_num)]
            final_string += string + "\n"
        return final_string

    def remove_duplicated_phrases(self, content_str):
        """
        This function removes the duplicated phrases from the START of the line which is duplicated upto
        certain character.
        The duplicated content is removed from that line (remains in the first line) and remaining content
        is added to the trie and the final string content
        """
        unique_lines = []
        trie = Trie()
        updated_lines = self.get_updated_lines_list(content_str)

        for uline in updated_lines:
            stripped_line = uline[0].strip()
            bool_val, index_val = trie.search(stripped_line.strip())
            # if the line does not exist in the trie
            if not bool_val:
                # the first index is the title => Title must remain the same
                if uline[1] != 0:
                    final_substr = stripped_line[index_val:]
                else:
                    final_substr = stripped_line

                trie.insert(final_substr.strip())
                # adding to our final string as it is unique
                unique_lines.append([final_substr.strip(), uline[1]])

        # sorting the unique lines based on the index in ascending order
        unique_lines.sort(key=lambda x: x[1])

        final_string = ""
        for string, _ in unique_lines:  # [(string, index_num)]
            final_string += string + "\n"
        return final_string

    async def get_final_scraped_content(self):
        """
        This is the main function which must be called outside of this file to start the pipeline
        Return Value -> Dictionary ->
        scrapped_text->Final Scrapped Text
        html_code-> html code of the scrapped text
        """
        # recieved html_bytes
        html_bytes = await self.fetch_url()
        # converting to html parsed and getting BeautifulSoup object back
        b_soup = await self.process_html(html_bytes)
        # removing the non-required tags and returing the BeautifulSoup object
        filtered_b_soup = self.filter_html_tags(b_soup)
        # getting a dictionary with the scraped text and the beautiful soup (which is same as filtered_b_soup)
        content_dict = self.get_required_content(filtered_b_soup)
        # joining the content
        initial_content_string = "\n".join(content_dict["content"])
        # removing pre-defined unnecessary words
        filtered_content = self.remove_unneccesary_words(initial_content_string)
        # the final content is joined and divided into lines
        necessary_content_string = self.get_formatted_string(filtered_content)
        # removing all the duplicated lines from our content
        unduplicated_content = self.get_formatted_string(
            self.remove_duplicated_lines(necessary_content_string)
        )
        # removing all the duplicated phrases which are at start of the lines
        # final_content = self.get_formatted_string(
        #     self.remove_duplicated_phrases(unduplicated_content)
        # )
        # returning the final scraped content with filtered html tags html page
        return {
            "scrapped_text": unduplicated_content,
            "html_code": content_dict["html_code"].prettify(),
        }
