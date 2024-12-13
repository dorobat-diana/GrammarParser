from collections import defaultdict

class ParserOutput:
    def __init__(self):
        self.parsing_tree = []  # A list to hold the parsing tree nodes

    def add_node(self, parent, children):
        """
        Adds a node to the parsing tree.
        :param parent: Parent symbol
        :param children: List of children symbols (can be terminals or non-terminals)
        """
        self.parsing_tree.append((parent, children))

    def print_tree(self):
        """
        Print the parsing tree in a human-readable format.
        """
        print("Parsing Tree:")
        for parent, children in self.parsing_tree:
            print(f"{parent} -> {' '.join(children)}")

    def save_tree_to_file(self, filename):
        """
        Saves the parsing tree to a file in a readable format.
        :param filename: Name of the file to save the tree.
        """
        with open(filename, 'w') as file:
            file.write("Parsing Tree:\n")
            for parent, children in self.parsing_tree:
                file.write(f"{parent} -> {' '.join(children)}\n")
