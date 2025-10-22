# Global variable to store results
word_counts = {}

def count_words_procedural(text):
    """Count words using procedural approach"""
    global word_counts
    word_counts = {}  # Reset global state
    
    # TODO: 
    # 1. Convert to lowercase and split into words
    # 2. Loop through words
    # 3. Update global word_counts dictionary
    text = text.lower().replace('.', '').replace(',', '')
    words = text.split()
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    
    return True

# Test it
sample_text = "The quick brown fox jumps over the lazy dog. The dog was very lazy and the fox was very quick."
result = count_words_procedural(sample_text)
if result:
    print("Procedural result:", word_counts)
else:
    print("Error in counting words.")
