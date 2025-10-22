import asyncio

class WordCounterEventDriven:
    def __init__(self):
        self.word_counts = {}
        self.processed_words = 0
    
    async def process_word_event(self, word):
        """Handle a single word processing event"""
        # TODO: Update word_counts for this word
        # Simulate async processing
        await asyncio.sleep(0.001)  # Tiny delay to simulate work
        word = word.lower().replace('.', '').replace(',', '')
        if word in self.word_counts:
            self.word_counts[word] += 1
        else:
            self.word_counts[word] = 1
        self.processed_words += 1
    
    async def process_text_event(self, text):
        """Handle text processing event"""
        self.word_counts = {}
        self.processed_words = 0
        
        # TODO:
        # 1. Split text into words
        # 2. Create async tasks for each word
        # 3. Use asyncio.gather() to process all words
        words = text.split()
        tasks = [self.process_word_event(word) for word in words]
        await asyncio.gather(*tasks)
        
        print(f"Processed {self.processed_words} words")
        return self.word_counts

# Test it
async def main():
    counter = WordCounterEventDriven()
    sample_text = "The quick brown fox jumps over the lazy dog. The dog was very lazy and the fox was very quick."
    result = await counter.process_text_event(sample_text)
    print("Event-driven result:", result)

if __name__ == "__main__":
    asyncio.run(main())
