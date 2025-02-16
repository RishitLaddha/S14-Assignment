import re
import os
from collections import Counter, defaultdict
from itertools import islice

# Context Manager for File Handling
class FileHandler:
    def __init__(self, file_path, mode='r', encoding='utf-8'):
        self.file_path = file_path
        self.mode = mode
        self.encoding = encoding
    
    def __enter__(self):
        self.file = open(self.file_path, self.mode, encoding=self.encoding)
        return self.file
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

# Generator for Reading Large Text Files
def text_generator(source):
    if isinstance(source, str) and os.path.exists(source):
        with FileHandler(source) as file:
            for line in file:
                yield line.strip()
    else:
        for line in source.split('\n'):
            yield line.strip()

# Word Frequency Counter
def word_frequency(source, filter_func=None):
    counter = Counter()
    for line in text_generator(source):
        words = re.findall(r'\b\w+\b', line.lower())
        if filter_func:
            words = [word for word in words if filter_func(word)]
        counter.update(words)
    return counter


# Unique Word Extractor
def unique_words(source):
    unique_set = set()
    for line in text_generator(source):
        words = re.findall(r'\b\w+\b', line.lower())
        unique_set.update(words)
    return unique_set

# Word Co-occurrence Matrix
def word_cooccurrence_matrix(source, window=2):
    words_list = []
    
    for line in text_generator(source):
        words = re.findall(r'\b\w+\b', line.lower())
        words_list.extend(words)
    
    cooccurrence_pairs = set()  # Use a set to store unique word pairs
    
    for i, word in enumerate(words_list):
        for j in range(max(i - window, 0), min(i + window + 1, len(words_list))):
            if i != j:  # Avoid self-cooccurrence
                cooccurrence_pairs.add((word, words_list[j]))
    
    return cooccurrence_pairs  # Return a set of word tuples

# # Example Usage:
# if __name__ == "__main__":
#     text_data = "This is a sample text. This text is for testing."
#     file_path = "sample.txt"
    
#     print("Word Frequencies:", word_frequency(text_data))
#     print("Unique Words:", unique_words(text_data))
#     print("Word Co-occurrences:", word_cooccurrence_matrix(text_data))
