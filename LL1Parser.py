from collections import defaultdict

from Grammar import Grammar


class LL1Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first_sets = defaultdict(set)
        self.follow_sets = defaultdict(set)

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
                    self.first_sets[non_terminal].update(current_first - {"e"})
                    if "e" in current_first:
                        self.first_sets[non_terminal].add("e")
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

    def print_first_sets(self):
        print("First Sets:")
        for non_terminal, first in sorted(self.first_sets.items()):
            print(f"  {non_terminal}: {first}")

    def print_follow_sets(self):
        print("Follow Sets:")
        for non_terminal, follow in sorted(self.follow_sets.items()):
            print(f"  {non_terminal}: {follow}")



# Example Usage
g = Grammar("g1.txt")
parser = LL1Parser(g)
parser.compute_first_sets()
parser.compute_follow_sets()

# Print sets and parse table
parser.print_first_sets()
parser.print_follow_sets()

# Example parsing
tokens = ["a", "*", "(", "a", "+", "a", ")", "$"]  # Example token stream
