class WordCounter:
    def __init__(self):
        self.word_counts = {}
    
    def add_word(self, word):
        """Add a single word to the count"""
        if word in self.word_counts:
            self.word_counts[word] += 1
        else:
            self.word_counts[word] = 1
    
    def count_words(self, text):
        """Count all words in the text"""
        self.word_counts = {}  # Reset
        # TODO:
        # 1. Split text into words
        # 2. Call add_word() for each word
        words = text.lower()
        words = words.replace('.', '').replace(',', '').split(" ")
        for word in words:
            self.add_word(word)
        return self.word_counts
    
    def get_word_count(self, word):
        """Get count for a specific word"""
        # TODO: Return count for word, or 0 if not found
        return self.word_counts.get(word.lower(), 0)

# Test it
counter = WordCounter()
sample_text = "The quick brown fox jumps over the lazy dog. The dog was very lazy and the fox was very quick."
result = counter.count_words(sample_text)
print("OOP result:", result)
print("Count of 'the':", counter.get_word_count('the'))
