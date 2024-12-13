from collections import defaultdict
from tabulate import tabulate
from Grammar import Grammar
from ParserOutput import ParserOutput


class LL1Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first_sets = defaultdict(set)
        self.follow_sets = defaultdict(set)
        self.parser_output = ParserOutput()

    def compute_first_sets(self):
        # Initialize FIRST sets
        for non_terminal in self.grammar.non_terminals:
            self.first_sets[non_terminal] = set()
        changed = True
        while changed:
            changed = False
            # Iterate through all productions
            for non_terminal, productions in self.grammar.productions.items():
                for production in productions:
                    current_first = self.first_of_sequence(production)
                    before_update = self.first_sets[non_terminal].copy()
                    self.first_sets[non_terminal].update(current_first )
                    if before_update != self.first_sets[non_terminal]:
                        changed = True

    def first_of_sequence(self, sequence):
        """
        Compute the FIRST set of a sequence of symbols (X1 X2 ... Xn).
        """
        if sequence == "e":
            return {"e"}

        result = set()
        for symbol in sequence:
            if symbol.isupper():
                result.update(self.first_sets[symbol] - {"e"})
                if "e" not in self.first_sets[symbol]:
                    break
            else:
                result.update(symbol)
                break
        return result

    def compute_follow_sets(self):
        for non_terminal in self.grammar.non_terminals:
            self.follow_sets[non_terminal] = set()
        start_symbol = self.grammar.start_symbol
        self.follow_sets[start_symbol].add("e")
        changed = True
        while changed:
            changed = False
            for non_terminal, productions in self.grammar.productions.items():
                for production in productions:
                    for i, symbol in enumerate(production):
                        if symbol.isupper():  # Only for non-terminals
                            rest = production[i + 1:]
                            before_update = self.follow_sets[symbol].copy()
                            if rest.isupper():
                                first_rest = self.first_sets[rest] - {"e"}
                                # Add FIRST(rest) - {e} to FOLLOW(symbol)
                                self.follow_sets[symbol].update(first_rest)
                                # If ε is in FIRST(rest) or rest is empty, add FOLLOW(non_terminal)
                                if not rest or "e" in self.first_sets[rest]:
                                    self.follow_sets[symbol].update(self.follow_sets[non_terminal])
                            elif not rest:
                                self.follow_sets[symbol].update(self.follow_sets[non_terminal])
                            else:
                                self.follow_sets[symbol].update(rest)
                            if before_update != self.follow_sets[symbol]:
                                changed = True

    def construct_parse_table(self):
        # Initialize table with "err"
        terminals = list(self.grammar.terminals) + ["$"]
        non_terminals = list(self.grammar.non_terminals)
        self.parse_table = defaultdict(lambda: defaultdict(lambda: "err"))

        # Set ($, $) to "acc"
        self.parse_table["$"]["$"] = "acc"

        # Set (a, a) to "pop" for terminals
        for terminal in self.grammar.terminals:
            self.parse_table[terminal][terminal] = "pop"

        # Process productions
        for non_terminal, productions in self.grammar.productions.items():
            for i, production in enumerate(productions, start=1):
                first_set = self.first_of_sequence(production)

                # Add rules for FIRST(alpha)
                for terminal in first_set - {"e"}:
                    self.parse_table[non_terminal][terminal] = (non_terminal + " -> " + production)

                # Add rules for FOLLOW(non_terminal) if ε is in FIRST(alpha)
                if "e" in first_set:
                    self.parse_table[non_terminal]["$"] = (non_terminal + " -> " + production)
                    for terminal in self.follow_sets[non_terminal]:
                        self.parse_table[non_terminal][terminal] = (non_terminal + " -> " + production)

    def parse_tokens(self, _tokens):
        stack = ["$", self.grammar.start_symbol]
        pointer = 0  # Points to the current token
        print("\nParsing Steps:")
        print(f"{'Stack':<30} {'Input':<30} {'Action'}")

        while stack:
            top = stack.pop()
            current_token = _tokens[pointer]

            # Print current state
            print(f"{' '.join(stack):<30} {' '.join(_tokens[pointer:]):<30}", end=" ")

            if top == current_token == "$":
                print("ACCEPT")
                return True  # Successfully parsed
            elif top == current_token:
                print(f"MATCH '{current_token}'")
                pointer += 1  # Move to the next token
            elif top.isupper():  # Non-terminal
                production = self.parse_table[top][current_token]
                if production == "err":
                    print(f"ERROR: No rule for {top} -> {current_token}")
                    return False
                print(f"EXPAND {production}")
                parent, rhs = production.split("->")
                rhs = rhs.strip()
                self.parser_output.add_node(parent,rhs)
                if rhs != "e":  # Don't push ε (empty string) to the stack
                    stack.extend(reversed(list(rhs)))
            else:
                print(f"ERROR: Unexpected token '{current_token}'")
                return False

        print("ERROR: Stack not empty but input exhausted")
        return False

    def print_parse_table(self):
        # Gather headers
        terminals = list(self.grammar.terminals) + ["$"]
        non_terminals = list(self.grammar.non_terminals)
        headers = [""] + terminals  # First column for non-terminals

        # Construct rows
        rows = []
        for non_terminal in non_terminals + ["$"]:
            row = [non_terminal]  # Row starts with the non-terminal
            for terminal in terminals:
                value = self.parse_table[non_terminal][terminal]
                row.append(value)
            rows.append(row)

        # Print table
        print(tabulate(rows, headers, tablefmt="grid"))

    def print_first_sets(self):
        print("First Sets:")
        for non_terminal, first in sorted(self.first_sets.items()):
            print(f"  {non_terminal}: {first}")

    def print_follow_sets(self):
        print("Follow Sets:")
        for non_terminal, follow in sorted(self.follow_sets.items()):
            print(f"  {non_terminal}: {follow}")



