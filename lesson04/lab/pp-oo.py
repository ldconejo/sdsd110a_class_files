class WordCounter:
    def __init__(self):
        self.word_counts = {}
    
    def add_word(self, word):
        """Add a single word to the count"""
        # TODO: Update self.word_counts
        pass
    
    def count_words(self, text):
        """Count all words in the text"""
        self.word_counts = {}  # Reset
        # TODO:
        # 1. Split text into words
        # 2. Call add_word() for each word
        return self.word_counts
    
    def get_word_count(self, word):
        """Get count for a specific word"""
        # TODO: Return count for word, or 0 if not found
        pass

# Test it
counter = WordCounter()
sample_text = "The quick brown fox jumps over the lazy dog. The dog was very lazy and the fox was very quick."
result = counter.count_words(sample_text)
print("OOP result:", result)
print("Count of 'the':", counter.get_word_count('the'))
