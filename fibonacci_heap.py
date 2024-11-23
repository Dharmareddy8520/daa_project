class FibonacciNode:
    def __init__(self, key):
        if not isinstance(key, (int, float)):
            raise ValueError("Key must be a numeric value.")
        if key <= 0:
            raise ValueError("Only positive numbers are allowed.")
        self.key = key
        self.degree = 0
        self.mark = False
        self.parent = None
        self.child = None
        self.left = self
        self.right = self


class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.total_nodes = 0
        self.root_list = []
        self.node_map = {}

    def is_empty(self):
        return self.total_nodes == 0

    def build(self):
        """Reset the heap to an empty state."""
        self.min_node = None
        self.total_nodes = 0
        self.root_list = []
        self.node_map = {}
        return True

    def insert(self, key):
        """Insert a new key into the heap."""
        if key <= 0:
            raise ValueError("Only positive numbers are allowed.")
        if key in self.node_map:
            raise ValueError(f"Duplicate keys are not allowed. Duplicate Key: {int(key)}")

        new_node = FibonacciNode(key)
        self.node_map[key] = new_node

        if self.min_node is None:
            self.min_node = new_node
            self.root_list = [new_node]
        else:
            self._add_to_root_list(new_node)
            if new_node.key < self.min_node.key:
                self.min_node = new_node

        self.total_nodes += 1
        return new_node

    def _add_to_root_list(self, node):
        """Add a node to the root list."""
        if not self.root_list:
            self.root_list = [node]
            node.left = node
            node.right = node
        else:
            last = self.root_list[-1]
            first = self.root_list[0]
            node.left = last
            node.right = first
            last.right = node
            first.left = node
            self.root_list.append(node)

    def find_min(self):
        """Return the minimum key without removing it."""
        if self.min_node is None:
            raise ValueError("Heap is empty.")
        return self.min_node.key

    def extract_min(self):
        """Remove and return the minimum key."""
        if self.min_node is None:
            raise ValueError("Heap is empty.")

        min_node = self.min_node
        min_key = min_node.key

        # Add all children to the root list
        if min_node.child:
            child = min_node.child
            children = []
            while True:
                next_child = child.right
                child.parent = None
                children.append(child)
                if child == min_node.child.left:
                    break
                child = next_child
            self.root_list.extend(children)

        # Remove the min node
        self.root_list.remove(min_node)
        del self.node_map[min_key]  # Ensure the key is removed from node_map

        if self.root_list:
            self._update_root_list_links()
            self.min_node = self.root_list[0]
            self._consolidate()
        else:
            self.min_node = None

        self.total_nodes -= 1
        return min_key

    def _update_root_list_links(self):
        """Update circular links in the root list."""
        for i in range(len(self.root_list)):
            self.root_list[i].left = self.root_list[i - 1]
            self.root_list[i].right = self.root_list[(i + 1) % len(self.root_list)]

    def _consolidate(self):
        """Consolidate trees of the same degree."""
        max_degree = int(self.total_nodes ** 0.5) + 1
        degree_table = [None] * max_degree

        nodes_to_process = self.root_list.copy()
        for node in nodes_to_process:
            degree = node.degree
            while degree_table[degree]:
                other = degree_table[degree]
                if node.key > other.key:
                    node, other = other, node
                self._link(other, node)
                degree_table[degree] = None
                degree += 1
            degree_table[degree] = node

        self.min_node = None
        self.root_list = [node for node in degree_table if node is not None]
        self._update_root_list_links()

        if self.root_list:
            self.min_node = min(self.root_list, key=lambda x: x.key)

    def _link(self, child, parent):
        """Make child a child of parent."""
        self.root_list.remove(child)

        if parent.child is None:
            parent.child = child
            child.left = child
            child.right = child
        else:
            child.right = parent.child.right
            child.left = parent.child
            parent.child.right.left = child
            parent.child.right = child

        child.parent = parent
        parent.degree += 1
        child.mark = False

    def decrease_key(self, old_key, new_key):
        """Decrease the key of a node."""
        if new_key != float('-inf') and new_key <= 0:
            raise ValueError("Only positive numbers are allowed (except for deletion).")
        if new_key >= old_key:
            raise ValueError("New key must be less than current key.")
        if old_key not in self.node_map:
            raise ValueError("Key not found in heap.")

        node = self.node_map[old_key]
        del self.node_map[old_key]
        self.node_map[new_key] = node
        node.key = new_key

        parent = node.parent
        if parent and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)

        if node.key < self.min_node.key:
            self.min_node = node

    def _cut(self, node, parent):
        """Cut a node from its parent."""
        if parent.child == node:
            if node.right == node:
                parent.child = None
            else:
                parent.child = node.right

        node.left.right = node.right
        node.right.left = node.left
        parent.degree -= 1

        self._add_to_root_list(node)
        node.parent = None
        node.mark = False

    def _cascading_cut(self, node):
        """Perform cascading cut operation."""
        parent = node.parent
        if parent:
            if not node.mark:
                node.mark = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)

    def delete(self, key):
        """Delete a node with the given key."""
        if key not in self.node_map:
            raise ValueError("Key not found in heap.")

        self.decrease_key(key, float('-inf'))
        self.extract_min()

    def merge(self, other_heap):
        """Merge another Fibonacci heap into this one."""
        if not isinstance(other_heap, FibonacciHeap):
            raise ValueError("Can only merge with another Fibonacci heap.")

        if other_heap.is_empty():
            return

        for key, node in other_heap.node_map.items():
            if key not in self.node_map and key > 0:  # Avoid duplicate or non-positive keys
                self.node_map[key] = node
                self.root_list.append(node)  # Add to root list only if valid

        self._update_root_list_links()

        if not self.min_node or (other_heap.min_node and other_heap.min_node.key < self.min_node.key):
            self.min_node = other_heap.min_node

        self.total_nodes += other_heap.total_nodes

    def show_tree(self):
        """Display the Fibonacci heap as a text-based tree structure."""
        if self.is_empty():
            print("Heap is empty.")
            return

        def get_node_str(node):
            mark = '*' if node.mark else ''
            min_marker = '(min)' if node == self.min_node else ''
            return f"[{node.key}{mark}{min_marker}]"

        def print_subtree(node, prefix="", is_last=True):
            connector = "└── " if is_last else "├── "
            print(prefix + connector + get_node_str(node))

            if node.child:
                new_prefix = prefix + ("    " if is_last else "│   ")
                children = []
                current = node.child
                while True:
                    children.append(current)
                    current = current.right
                    if current == node.child:
                        break
                for i, child in enumerate(children):
                    print_subtree(child, new_prefix, i == len(children) - 1)

        print("Root List:")
        for i, root in enumerate(self.root_list):
            print_subtree(root, "", i == len(self.root_list) - 1)

        print("\nHeap Statistics:")
        print(f"Total nodes: {self.total_nodes}")
        print(f"Minimum key: {self.min_node.key if self.min_node else 'None'}")
        print(f"Number of roots: {len(self.root_list)}")
        marked_nodes = sum(1 for node in self.node_map.values() if node.mark)
        print(f"Marked nodes: {marked_nodes}")


def main():
    heap = FibonacciHeap()

    while True:
        print("\nFibonacci Heap Operations:")
        print("1. Build empty heap")
        print("2. Insert node")
        print("3. Find minimum")
        print("4. Extract minimum")
        print("5. Decrease key")
        print("6. Delete node")
        print("7. Merge heaps")
        print("8. Show tree")
        print("9. Exit")

        try:
            choice = input("Choose an operation: ").strip()

            if choice == "1":
                heap.build()
                print("Empty heap built successfully.")

            elif choice == "2":
                key = float(input("Enter key to insert: "))
                heap.insert(key)
                print(f"Inserted key: {key}")

            elif choice == "3":
                min_key = heap.find_min()
                print(f"Minimum key: {min_key}")

            elif choice == "4":
                min_key = heap.extract_min()
                print(f"Extracted minimum key: {min_key}")

            elif choice == "5":
                old_key = float(input("Enter current key: "))
                new_key = float(input("Enter new key: "))
                heap.decrease_key(old_key, new_key)
                print(f"Decreased key from {old_key} to {new_key}")

            elif choice == "6":
                key = float(input("Enter key to delete: "))
                heap.delete(key)
                print(f"Deleted key: {key}")

            elif choice == "7":
                other_heap = FibonacciHeap()
                print("Building another heap...")
                n = int(input("How many keys to insert in the new heap? "))
                for _ in range(n):
                    key = float(input("Enter key: "))
                    other_heap.insert(key)
                heap.merge(other_heap)
                print("Heaps merged successfully.")

            elif choice == "8":
                heap.show_tree()

            elif choice == "9":
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
