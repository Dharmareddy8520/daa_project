
# Fibonacci Heap Implementation

## Overview

This Python program implements a Fibonacci Heap, a data structure that supports priority queue operations like insert, extract minimum, decrease key, delete, and merge. This implementation allows you to interact with the Fibonacci Heap through a command-line interface.

The Fibonacci Heap supports the following operations:
1. **Build**: Create an empty Fibonacci Heap.
2. **Insert**: Insert a positive key into the heap.
3. **Find Min**: Retrieve the minimum key in the heap.
4. **Extract Min**: Remove the node with the minimum key.
5. **Decrease Key**: Decrease the value of a specific key.
6. **Delete**: Remove a specific key from the heap.
7. **Merge**: Merge two Fibonacci Heaps into one.

### Additional features:
- **Error Handling**: Prevents invalid operations such as inserting duplicate or negative keys.
- **Show Tree**: Displays the current structure and statistics of the heap.

## Requirements

- Python 3.6 or later
- Required libraries:
  - `unittest` (standard Python library)

## Running the Program

### Step 1: Clone or Download the Repository
Download the source code file that contains the Fibonacci Heap implementation. You can copy the code and save it in a Python file named `fibonacci_heap.py`.

### Step 2: Open a Command Line Interface
Navigate to the directory where you saved the `daa-project/fibonacci_heap.py` file using your terminal or command prompt.

### Step 3: Execute the Program
Run the program by executing the following command:

```bash
python fibonacci_heap.py
```

### Step 4: Run the Test Suite
To validate the implementation, execute the test script:

```bash
python test_fibonacci_heap.py
```

## Project Structure

```project/
├── fibonacci_heap.py
├── test_fibonacci_heap.py
├── screenshots/         # Your folder containing images
│   ├── screenshot1.png
│   ├── screenshot2.png
├── README.md
```
## Known Constraints

- Only positive keys are allowed (negative keys will raise a `ValueError`).
- Duplicate keys are not permitted.

## Future Enhancements

- Add a graphical visualization of the Fibonacci Heap.
- Optimize memory usage for handling larger datasets.

## Contributors

**Group 1** –
- Pramit Man Shrestha
- Dharma Reddy Pandem
- Yaso Deepika Morumpudi
- Khawaja Fahad
