import os
from nltk import sent_tokenize


class SummarizeContent:
    def __init__(self, content: str, tfidf_vector: dict) -> None:
        self.content = content
        self.tfidf_vector = tfidf_vector
        self.no_sentences = int(os.environ["NO_SENTENCE_IN_SUMMARY"])

    def extract_sentence_score(self, sentence: str):
        """Calculates the TF-IDF score for a sentence and returns number"""
        sentence_score = sum(
            self.tfidf_vector.get(word, [0])[0] for word in sentence.split()
        )
        return sentence_score

    def extract_summary(self):
        """Main function that is used to extract the summary of a content based on the TF-IDF Score"""
        content = sent_tokenize(self.content)
        sentence_summaries = []
        original_indices = []  # Keep track of original indices

        for index, sentence in enumerate(content):
            sentence_score = self.extract_sentence_score(sentence)
            # storing with index for the order
            sentence_summaries.append((index, sentence, sentence_score))
            original_indices.append(index)  # Store original index

        sentence_summaries.sort(key=lambda x: x[2], reverse=True)
        final_summary = [
            sentence for _, sentence, _ in sentence_summaries[: self.no_sentences]
        ]

        # Sort final_summary by original indices
        final_summary = sorted(
            final_summary, key=lambda x: original_indices[final_summary.index(x)]
        )

        return " ".join(final_summary)
