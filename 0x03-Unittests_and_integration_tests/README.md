# Test Suite for `test_utils.py`

This document provides an overview of the test suite implemented in the `test_utils.py` file. The file contains unit tests for utility functions defined in `utils.py`. These tests ensure that the functions behave as expected under various scenarios.

## Functions Tested

### 1. `access_nested_map`
This function retrieves a value from a nested dictionary using a sequence of keys.

**Example Usage:**
```python
nested_map = {"a": {"b": {"c": 1}}}
result = access_nested_map(nested_map, ["a", "b", "c"])
# result = 1
```

#### Test Cases:
- **Valid Inputs:**
  - Retrieve a value at a single key.
  - Retrieve a nested dictionary.
  - Retrieve a deeply nested value.

- **Invalid Inputs:**
  - Raise `KeyError` when a key does not exist.
  - Ensure the exception message matches the missing key.

### 2. `get_json`
This function retrieves JSON data from a given URL.

**Example Usage:**
```python
url = "http://example.com"
response = get_json(url)
# response = {"payload": True}
```

#### Test Cases:
- Mock the `requests.get` function to avoid actual HTTP calls.
- Ensure the mocked function is called with the correct URL.
- Verify that the returned JSON matches the expected payload.

### 3. `memoize`
This decorator caches the result of a method call to avoid redundant computations.

**Example Usage:**
```python
class MyClass:
    @memoize
    def a_property(self):
        print("Computing...")
        return 42

obj = MyClass()
result = obj.a_property
# Output: "Computing..."
result = obj.a_property
# No output (cached result)
```

#### Test Cases:
- Mock the method being memoized.
- Ensure the method is only called once even if accessed multiple times.
- Verify that the returned value is correct.

---

## Test Suite Structure

### 1. `TestAccessNestedMap`
- Contains parameterized tests for valid and invalid inputs.
- Uses `@parameterized.expand` to define multiple test scenarios.
- Uses `assertRaises` to validate exceptions.

### 2. `TestGetJson`
- Mocks the `requests.get` function using `unittest.mock.patch`.
- Uses `MagicMock` to simulate the behavior of the HTTP response object.
- Validates that the `get_json` function works as intended.

### 3. `TestMemoize`
- Defines a test class with a memoized property.
- Uses `patch.object` to mock the method being memoized.
- Ensures the method is only called once and the cached result is correct.

---

## Running the Tests
To run the test suite, execute the following command:
```bash
python3 -m unittest test_utils.py
```

---

## Pycodestyle Validation
This test suite adheres to PEP 8 coding standards. Use the following command to validate:
```bash
pycodestyle test_utils.py
```

Ensure the code passes without any warnings or errors.

---

## Notes
- The tests utilize `unittest` and `parameterized` for structured and flexible test cases.
- Mocking is extensively used to isolate tests from external dependencies.
- Follow the comments in the code for clarity on each test case.

