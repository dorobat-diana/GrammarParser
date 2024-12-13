from collections import defaultdict

class LL1Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first_sets = defaultdict(set)
        self.follow_sets = defaultdict(set)
        self.parsing_tree = []
        self.node_index = 0
        self.add_node("", "S")

    def add_node(self, parent, children):
        """
        Adds nodes to the parsing tree as a table row.
        :param parent: Parent symbol
        :param children: List of children symbols (can be terminals or non-terminals)
        """
        parent_index = self.get_node_index(parent)

        # Add children as nodes with parent references
        last_sibling = None
        for child in children:
            self.node_index += 1
            current_index = self.node_index

            # Add the node with parent reference
            self.parsing_tree.append({
                "index": current_index,
                "info": child,
                "parent": parent_index,
                "right_sibling": 0  # Default; updated below
            })

            # Update the right_sibling of the last sibling
            if last_sibling is not None:
                self.parsing_tree[last_sibling]["right_sibling"] = current_index-1

            last_sibling = current_index

    def get_node_index(self, info):
        """Retrieve the index of a node based on its info."""
        for node in self.parsing_tree:
            if node["info"] == info.strip():
                return node["index"]
        return 0

    def print_parsing_tree(self):
        """Print the parsing tree as a table."""
        print(f"{'Index':<10}{'Info':<15}{'Parent':<10}{'Right Sibling':<15}")
        print("-" * 50)
        for node in self.parsing_tree:
            print(f"{node['index']:<10}{node['info']:<15}{node['parent']:<10}{node['right_sibling']:<15}")

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
                    self.first_sets[non_terminal].update(current_first)
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
        self.compute_first_sets()
        self.compute_follow_sets()
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
        self.construct_parse_table()
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
                self.add_node(parent, rhs)
                if rhs != "e":  # Don't push ε (empty string) to the stack
                    stack.extend(reversed(list(rhs)))
            else:
                print(f"ERROR: Unexpected token '{current_token}'")
                return False

        print("ERROR: Stack not empty but input exhausted")
        return False
