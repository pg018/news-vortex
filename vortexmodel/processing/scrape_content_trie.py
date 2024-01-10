class TrieNode:
    """Node of a trie structure"""

    def __init__(self):
        self.children = {}
        # initially set as true for satisfying our requirements
        # we are comparing each character
        # IMP - Do not alter this
        self.is_end_of_word = True


class Trie:
    """Trie Data Structure used in scraping of incoming content"""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Inserting new content in the trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, line):
        """
        A line is entered as parameter. used to search character wise
        Return Value => Returns False if a single character does not match along with the
        index where it does not match
        """
        node = self.root
        index = 0
        for char in line:
            if char not in node.children:
                return False, index
            index += 1
            node = node.children[char]

        return node.is_end_of_word, 0
