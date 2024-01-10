import math


class CustomTFIDF:
    def __init__(self, document_list: list[str]) -> None:
        """
        Initialize the CustomTFIDF object with a list of documents.

        Args:
            document_list (list of str): List of raw document texts.

        Returns:
            None
        """
        self.docs_list = document_list

    def compute_tf(self, word, document):
        """
        Calculate the Term Frequency (TF) of a word in a document.
        Args:
            word (str): The word to calculate TF for.
            document (str): The document containing the word.
        Returns:
            float: The calculated TF value.
        """
        return document.count(word) / len(document)

    def compute_idf(self, word):
        """
        Calculate the Inverse Document Frequency (IDF) of a word.
        Args:
            word (str): The word to calculate IDF for.
        Returns:
            float: The calculated IDF value.
        """
        no_docs = len(self.docs_list)
        df = sum([1 for document in self.docs_list if word in document])
        return math.log(no_docs / (df + 1))

    def compute_tfidf(self, word, document):
        """
        Calculate the TF-IDF score of a word in a document.
        Args:
            word (str): The word to calculate TF-IDF for.
            document (str): The document containing the word.
        Returns:
            float: The calculated TF-IDF score.
        """
        tf = self.compute_tf(word, document)
        idf = self.compute_idf(word)
        return tf * idf

    def create_tfidf_vector(self):
        """
        Create a TF-IDF vector for the given list of documents.
        Returns:
            dict: TF-IDF vector with words as keys and lists of TF-IDF scores as values.
        """
        unique_words = set(
            word for document in self.docs_list for word in document.split()
        )

        tfidf_vector = {
            word: [self.compute_tfidf(word, document) for document in self.docs_list]
            for word in unique_words
        }
        return tfidf_vector
