import unittest
from fibonacci_heap import FibonacciHeap  # Ensure your FibonacciHeap code is in a file named `fibonacci_heap.py`

class TestFibonacciHeap(unittest.TestCase):

    def setUp(self):
        """Set up a new Fibonacci Heap instance for each test."""
        self.heap = FibonacciHeap()

    def test_build(self):
        """Test building an empty heap."""
        self.heap.build()
        self.assertTrue(self.heap.is_empty())
        self.assertEqual(self.heap.total_nodes, 0)

    def test_insert(self):
        """Test inserting positive keys into the heap."""
        self.heap.insert(10)
        self.assertEqual(self.heap.find_min(), 10)
        self.heap.insert(5)
        self.assertEqual(self.heap.find_min(), 5)
        with self.assertRaises(ValueError):  # Only positive keys allowed
            self.heap.insert(-1)
        with self.assertRaises(ValueError):  # Duplicate keys not allowed
            self.heap.insert(5)

    def test_find_min(self):
        """Test finding the minimum key."""
        self.heap.insert(20)
        self.heap.insert(15)
        self.heap.insert(5)
        self.assertEqual(self.heap.find_min(), 5)

    def test_extract_min(self):
        """Test extracting the minimum key."""
        self.heap.insert(20)
        self.heap.insert(15)
        self.heap.insert(5)
        self.assertEqual(self.heap.extract_min(), 5)
        self.assertEqual(self.heap.find_min(), 15)

    def test_decrease_key(self):
        """Test decreasing a key in the heap."""
        self.heap.insert(20)
        self.heap.insert(15)
        self.heap.insert(10)
        self.heap.decrease_key(15, 5)
        self.assertEqual(self.heap.find_min(), 5)
        with self.assertRaises(ValueError):  # New key must be less than the old key
            self.heap.decrease_key(20, 25)
        with self.assertRaises(ValueError):  # Key not found
            self.heap.decrease_key(50, 10)

    def test_delete(self):
        """Test deleting a key from the heap."""
        self.heap.insert(10)
        self.heap.insert(20)
        self.heap.insert(5)
        self.heap.delete(20)
        self.assertEqual(self.heap.find_min(), 5)
        with self.assertRaises(ValueError):  # Key not found
            self.heap.delete(50)

    def test_merge(self):
        """Test merging two heaps."""
        self.heap.insert(10)
        self.heap.insert(20)
        other_heap = FibonacciHeap()
        other_heap.insert(5)
        other_heap.insert(15)
        self.heap.merge(other_heap)
        self.assertEqual(self.heap.find_min(), 5)
        with self.assertRaises(ValueError):  # Duplicate key from merged heap
            other_heap.insert(5)

    def test_show_tree(self):
        """Test that the tree structure displays correctly."""
        self.heap.insert(10)
        self.heap.insert(20)
        self.heap.show_tree()  # This test ensures no exceptions; output verification is manual.


if __name__ == "__main__":
    # Run tests with verbosity level 2 to display detailed results in the terminal
    unittest.main(verbosity=2)
