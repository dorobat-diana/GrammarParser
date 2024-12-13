from collections import defaultdict
from tabulate import tabulate
from Grammar import Grammar

class ParserOutput:
    def __init__(self, parser):
        self.parser = parser  # A parser object that contains parsing-related information

    def print_tree(self):
        """
        Print the parsing tree in a human-readable format.
        """
        print("Parsing Tree:")
        for obj in self.parser.parsing_tree:
            print(f"{obj}")

    def save_tree_to_file(self, filename):
        """
        Saves the parsing tree to a file in a readable format.
        :param filename: Name of the file to save the tree.
        """
        with open(filename, 'w') as file:
            file.write("Parsing Tree:\n")
            for obj in self.parser.parsing_tree:
                file.write(f"{obj}\n")

    def print_parse_table(self):
        """
        Print the parsing table in a tabular format.
        """
        terminals = list(self.parser.grammar.terminals) + ["$"]
        non_terminals = list(self.parser.grammar.non_terminals)
        headers = [""] + terminals

        rows = []
        for non_terminal in non_terminals + ["$"]:
            row = [non_terminal]
            for terminal in terminals:
                value = self.parser.parse_table[non_terminal][terminal]
                row.append(value)
            rows.append(row)

        print(tabulate(rows, headers, tablefmt="grid"))

    def save_parse_table_to_file(self, filename):
        """
        Saves the parsing table to a file in a tabular format.
        :param filename: Name of the file to save the parse table.
        """
        terminals = list(self.parser.grammar.terminals) + ["$"]
        non_terminals = list(self.parser.grammar.non_terminals)
        headers = [""] + terminals

        rows = []
        for non_terminal in non_terminals + ["$"]:
            row = [non_terminal]
            for terminal in terminals:
                value = self.parser.parse_table[non_terminal][terminal]
                row.append(value)
            rows.append(row)

        with open(filename, 'w') as file:
            file.write(tabulate(rows, headers, tablefmt="grid"))

    def print_first_sets(self):
        """
        Print the first sets of the grammar.
        """
        print("First Sets:")
        for non_terminal, first in sorted(self.parser.first_sets.items()):
            print(f"  {non_terminal}: {first}")

    def save_first_sets_to_file(self, filename):
        """
        Saves the first sets of the grammar to a file.
        :param filename: Name of the file to save the first sets.
        """
        with open(filename, 'w') as file:
            file.write("First Sets:\n")
            for non_terminal, first in sorted(self.parser.first_sets.items()):
                file.write(f"  {non_terminal}: {first}\n")

    def print_follow_sets(self):
        """
        Print the follow sets of the grammar.
        """
        print("Follow Sets:")
        for non_terminal, follow in sorted(self.parser.follow_sets.items()):
            print(f"  {non_terminal}: {follow}")

    def save_follow_sets_to_file(self, filename):
        """
        Saves the follow sets of the grammar to a file.
        :param filename: Name of the file to save the follow sets.
        """
        with open(filename, 'w') as file:
            file.write("Follow Sets:\n")
            for non_terminal, follow in sorted(self.parser.follow_sets.items()):
                file.write(f"  {non_terminal}: {follow}\n")

    def print_all(self):
        """
        Print all available outputs (tree, parse table, first sets, and follow sets).
        """
        self.print_tree()
        print()
        self.print_parse_table()
        print()
        self.print_first_sets()
        print()
        self.print_follow_sets()

    def save_all_to_file(self, base_filename):
        """
        Save all outputs to files with a common base filename and appropriate suffixes.
        :param base_filename: The base filename for saving outputs.
        """
        self.save_tree_to_file(f"{base_filename}_parsing_tree.txt")
        self.save_parse_table_to_file(f"{base_filename}_parse_table.txt")
        self.save_first_sets_to_file(f"{base_filename}_first_sets.txt")
        self.save_follow_sets_to_file(f"{base_filename}_follow_sets.txt")
