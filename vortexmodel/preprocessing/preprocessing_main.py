import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# nltk.download("punkt")
# nltk.download("stopwords")
# nltk.download("averaged_perceptron_tagger")


class Preprocessing:
    def __init__(self, entered_prompt: str) -> None:
        """Entered Prompt is the prompt entered by the user."""
        self.user_prompt = entered_prompt

    def is_valid_query(self) -> bool:
        """
        Checks if length of prompt is greater than 0
        Return Value -> boolean
        """
        return len(self.user_prompt.strip()) > 0

    def extract_keywords(self) -> list[str]:
        """
        This function filters out the keywords from the prompt.
        Return Value -> Returns a list of keywords
        """
        # tokenizes the input text into individual words using the fn
        tokens = word_tokenize(self.user_prompt)
        # pos (parts of speech) assigns grammatical label (tag) to each token to indicate pos(noun, adj..)
        tagged_tokens = pos_tag(tokens=tokens)  # [(word, tag)...]
        keywords: list[str] = []
        for word, tag in tagged_tokens:
            if tag in ["NN", "NNS", "NNP", "NNPS"]:  # nouns and proper nouns
                keywords.append(word)

        return keywords

    def consolidate_keywords(self, keywords_list: list[str]) -> str:
        """Joins the keywords into a single string"""
        return " ".join(keywords_list)

    def preprocess_prompt(self) -> str:
        """
        This is the main function that is called in this class. It is responsible for pipelining
        the pre processing the prompt.
        Return Value - Returns string which contains the main keywords after validations
        """
        if self.is_valid_query() == False:
            return "Invalid Prompt"
        main_keywords = self.extract_keywords()
        keywords_string = self.consolidate_keywords(main_keywords)
        print(keywords_string)
        return keywords_string


if __name__ == "__main__":
    prompt = input("Enter the prompt for Pre-Processing: ")
    preprocess = Preprocessing(prompt)
    preprocess.preprocess_prompt()
