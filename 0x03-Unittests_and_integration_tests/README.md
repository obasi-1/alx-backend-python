**Project: Unit Testing Utilities**

This project demonstrates how to write unit tests for a utility function in Python using the unittest framework and the parameterized library.

**Files**

utils.py

This module contains the utility function access_nested_map.

access_nested_map(nested_map, path): This function is designed to access a value within a nested dictionary (or map) using a sequence of keys (the path). It safely traverses the nested structure and returns the desired value.

test_utils.py

This file contains the unit tests for the access_nested_map function.

TestAccessNestedMap: A test class that inherits from unittest.

TestCase.test_access_nested_map: A test method that uses the @parameterized.expand decorator to test the access_nested_map function with multiple sets of inputs. This allows for concise and readable tests for various scenarios.

**Requirements**

Python 3.7+

parameterized library

**Installation**

Clone the repository or download the files.

Install the necessary library:
pip install parameterized

**Running the Tests**

To execute the unit tests, navigate to the project directory in your terminal and run the following command:

python -m unittest test_utils.py

You should see an output indicating that the tests have run successfully.
