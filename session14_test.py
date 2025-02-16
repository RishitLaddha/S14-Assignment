import unittest
import text_toolkit as tt  # The student's module
import os


class TestTextToolkit(unittest.TestCase):
    
    def setUp(self):
        # Sample text data for testing
        self.text_data = """Hello world! This is a test.
                            Hello again, world!
                            Testing word frequencies."""
        self.text_path = 'sample_text.txt'
        
        # Write sample text to a file for file-based tests
        with open(self.text_path, 'w') as f:
            f.write(self.text_data)

    def tearDown(self):
        # Clean up the file created for tests
        if os.path.exists(self.text_path):
            os.remove(self.text_path)

    # Test for word_frequency function
    def test_word_frequency(self):
        # Test with string input
        freq = tt.word_frequency(self.text_data)
        expected = {'hello': 2, 'world': 2, 'this': 1, 'is': 1, 'a': 1, 'test': 1, 
                    'again': 1, 'testing': 1, 'word': 1, 'frequencies': 1}
        self.assertEqual(freq, expected)

        # Test with file input
        freq_file = tt.word_frequency(self.text_path)
        self.assertEqual(freq_file, expected)

    # Test for unique_words function
    def test_unique_words(self):
        # Test with string input
        unique = tt.unique_words(self.text_data)
        expected = {'hello', 'world', 'this', 'is', 'a', 'test', 
                    'again', 'testing', 'word', 'frequencies'}
        self.assertEqual(set(unique), expected)

        # Test with file input
        unique_file = tt.unique_words(self.text_path)
        self.assertEqual(set(unique_file), expected)

    # Test for word_cooccurrence_matrix function
    def test_word_cooccurrence_matrix(self):
        # Test with string input
        cooccurrence = tt.word_cooccurrence_matrix(self.text_data, window=2)
        self.assertIn(('hello', 'world'), cooccurrence)
        self.assertIn(('world', 'this'), cooccurrence)

        # Test with file input
        cooccurrence_file = tt.word_cooccurrence_matrix(self.text_path, window=2)
        self.assertIn(('hello', 'world'), cooccurrence_file)
        self.assertIn(('world', 'this'), cooccurrence_file)

    # Test for text_generator function
    def test_text_generator(self):
        # Test with string input
        text_gen = tt.text_generator(self.text_data)
        self.assertTrue(hasattr(text_gen, '__iter__'))
        self.assertTrue(hasattr(text_gen, '__next__'))

        lines = list(text_gen)
        self.assertEqual(len(lines), 3)

        # Test with file input
        text_gen_file = tt.text_generator(self.text_path)
        self.assertTrue(hasattr(text_gen_file, '__iter__'))
        self.assertTrue(hasattr(text_gen_file, '__next__'))

        lines_file = list(text_gen_file)
        self.assertEqual(len(lines_file), 3)

    # Test for handling large text files using generators
    def test_large_file_handling(self):
        # Write a large text file for testing
        large_text = 'word ' * 10000  # 10,000 words
        large_text_path = 'large_text.txt'
        with open(large_text_path, 'w') as f:
            f.write(large_text)

        # Ensure the generator can handle large files
        gen = tt.text_generator(large_text_path)
        self.assertTrue(hasattr(gen, '__iter__'))
        self.assertTrue(hasattr(gen, '__next__'))

        # Ensure that each line in the large file is processed
        lines = list(gen)
        self.assertEqual(len(lines), 1)

        # Clean up large file
        if os.path.exists(large_text_path):
            os.remove(large_text_path)

    # Test for context manager usage
    def test_context_manager(self):
        # This test ensures that files are opened and closed correctly with context managers
        with self.assertRaises(ValueError):
            with open(self.text_path, 'r') as f:
                # Simulate an error during file processing
                raise ValueError("Simulated error")

        # Ensure that the file is still closed after the error
        self.assertTrue(f.closed)

    # Test for scope, closure, and functional parameters
    def test_closure_and_scope(self):
        # Test any functions that use closures, lambdas, or functional parameters
        # Example: word frequency function might use a functional parameter for filtering words
        def word_filter(word):
            return len(word) > 4  # Filter words longer than 4 characters
        
        freq_filtered = tt.word_frequency(self.text_data, filter_func=word_filter)
        expected_filtered = {'hello': 2, 'world': 2, 'again': 1, 'testing': 1, 'frequencies': 1}
        self.assertEqual(freq_filtered, expected_filtered)


# Run all the tests
if __name__ == '__main__':
    unittest.main()
