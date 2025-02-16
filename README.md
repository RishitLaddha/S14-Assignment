# Overview

The text_toolkit module provides a set of utilities for processing and analyzing text files. It includes functions to compute word frequency, extract unique words, generate word co-occurrence matrices, and read large text files efficiently using generators. These functions are designed to handle both direct text input and file-based input, ensuring flexibility in various text-processing tasks.
How to Run It

To use the text_toolkit module, first import it and call the desired functions just like the example usage of each fucntion is given below :
import text_toolkit as tt

# Text Toolkit


The `text_toolkit` module provides a set of functions for processing text files. It includes methods for analyzing word frequency, extracting unique words, creating a word co-occurrence matrix, and reading large text files efficiently. Below is a breakdown of each function and how it works, along with example usages.

---

## File Handling with Context Manager

The `FileHandler` class ensures that files are opened and closed properly using a context manager. This prevents memory leaks and ensures the file is properly closed even if an error occurs.

```python
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
```

### Example Usage:
```python
with FileHandler("example.txt") as file:
    for line in file:
        print(line.strip())
```
This reads the file line-by-line and prints each line after stripping leading/trailing spaces.

#### Potential Failures:
- If the file does not exist, it will raise a `FileNotFoundError`.
- If the user lacks permission to read the file, it will raise a `PermissionError`.

---

## Text Generator

The `text_generator` function allows reading a text file efficiently using a generator. This is especially useful for processing large files.

```python
def text_generator(source):
    if isinstance(source, str) and os.path.exists(source):
        with FileHandler(source) as file:
            for line in file:
                yield line.strip()
    else:
        for line in source.split('\n'):
            yield line.strip()
```

### Example Usage:
```python
for line in tt.text_generator("example.txt"):
    print(line)
```
This prints each line of the file. 

#### Potential Failures:
- If the file does not exist, it will not return any data.
- If given a non-string input, it will process it as a string, splitting on `\n`.

---

## Word Frequency Counter

This function counts how frequently each word appears in the given text.

```python
def word_frequency(source, filter_func=None):
    counter = Counter()
    for line in text_generator(source):
        words = re.findall(r'\b\w+\b', line.lower())
        if filter_func:
            words = [word for word in words if filter_func(word)]
        counter.update(words)
    return counter
```

### Example Usage:
```python
freq = tt.word_frequency("example.txt")
print(freq)
```
This prints a dictionary where words are keys and their counts are values.

#### Potential Failures:
- If the text file is empty, it will return an empty dictionary.
- If `filter_func` is provided but incorrect, it may exclude words incorrectly.

---

## Unique Words Extractor

This function extracts all unique words from the text.

```python
def unique_words(source):
    unique_set = set()
    for line in text_generator(source):
        words = re.findall(r'\b\w+\b', line.lower())
        unique_set.update(words)
    return unique_set
```

### Example Usage:
```python
unique = tt.unique_words("example.txt")
print(unique)
```
This prints a set of all unique words in the text file.

#### Potential Failures:
- If the text file is empty, it will return an empty set.
- If the input is not properly formatted, some words may not be captured.

---

## Word Co-occurrence Matrix

This function builds a set of word pairs that appear within a specified window of each other.

```python
def word_cooccurrence_matrix(source, window=2):
    words_list = []
    for line in text_generator(source):
        words = re.findall(r'\b\w+\b', line.lower())
        words_list.extend(words)
    
    cooccurrence_pairs = set()
    
    for i, word in enumerate(words_list):
        for j in range(max(i - window, 0), min(i + window + 1, len(words_list))):
            if i != j:
                cooccurrence_pairs.add((word, words_list[j]))
    
    return cooccurrence_pairs
```

### Example Usage:
```python
cooccurrence_matrix = tt.word_cooccurrence_matrix("example.txt", window=2)
print(cooccurrence_matrix)
```
This prints a set of word pairs that appear together within the given `window` size.

#### Potential Failures:
- If the text contains very few words, the output may be empty.
- If `window` is too large, it may create unexpected associations.

---

## Running Tests

Unit tests are included in `session14_test.py`. To run the tests, use:
```bash
python3 -m unittest session14_test.py
```

### Test Cases Covered
- Word frequency computation
- Unique word extraction
- Word co-occurrence matrix verification
- Text generator handling of large files
- Context manager correctness
- Functional programming aspects

This ensures the correctness and efficiency of the implemented functions.


## Result of running session14_test.py using Actions 

<img width="1279" alt="Screenshot 2025-02-17 at 00 06 59" src="https://github.com/user-attachments/assets/70e0eff6-145a-49d3-9a42-ac6ea03b95b7" />
