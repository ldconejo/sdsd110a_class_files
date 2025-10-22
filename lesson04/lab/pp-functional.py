from functools import reduce
from collections import defaultdict

def count_words_functional(text):
    """Count words using functional programming approach"""
    
    # Step 1: Transform text to list of words
    def text_to_words(text):
        # TODO: Return list of lowercase words
        pass
    
    # Step 2: Count words using reduce
    def count_reducer(counts, word):
        # TODO: Add word to counts dictionary and return
        # Hint: You can modify and return the same dict (it's okay here)
        pass
    
    # TODO: Create functional pipeline:
    # text → words → counts
    words = text_to_words(text)
    counts = reduce(count_reducer, words, {})
    return counts

# Alternative functional approach using built-ins
def count_words_functional_v2(text):
    """Even more functional approach"""
    from collections import Counter
    # TODO: One-liner using Counter and list comprehension
    pass

# Test it
sample_text = "The quick brown fox jumps over the lazy dog. The dog was very lazy and the fox was very quick."
result = count_words_functional(sample_text)
print("Functional result:", result)
