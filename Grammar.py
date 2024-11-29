from collections import defaultdict

class Grammar:
    def __init__(self, grammar_file):
        self.non_terminals = set()
        self.terminals = set()
        self.productions = defaultdict(list)
        self.start_symbol = None
        self.read_grammar(grammar_file)

    def read_grammar(self, grammar_file):
        with open(grammar_file, 'r') as file:
            lines = file.readlines()

        # Parse the grammar sections
        section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Non-terminals:"):
                section = "non_terminals"
                self.non_terminals = set(line[len("Non-terminals:"):].strip().split())
            elif line.startswith("Terminals:"):
                section = "terminals"
                self.terminals = set(line[len("Terminals:"):].strip().split())
            elif line.startswith("Productions:"):
                section = "productions"
            elif line.startswith("Start:"):
                section = "start"
                self.start_symbol = line[len("Start:"):].strip()
            elif section == "productions":
                head, body = line.split("->")
                head = head.strip()
                productions = [prod.strip() for prod in body.split("|")]
                self.productions[head].extend(productions)

    def get_non_terminals(self):
        return self.non_terminals

    def get_terminals(self):
        return self.terminals

    def get_productions(self):
        return dict(self.productions)

    def get_productions_for_non_terminal(self, non_terminal):
        return self.productions.get(non_terminal, [])

    def is_cfg(self):
        if self.start_symbol not in self.non_terminals:
            return False
        # Check if all production heads are single non-terminals
        for head in self.productions:
            if head not in self.non_terminals:
                return False  # Head must be a single non-terminal
            if len(head.split()) > 1:
                return False  # Head must not be a sequence
        # Check if production bodies are valid strings of terminals and non-terminals
        for bodies in self.productions.values():
            for body in bodies:
                for symbol in body:
                    if symbol not in self.non_terminals and symbol not in self.terminals and symbol != "e":
                        return False
        return True

    # Print functions for convenience
    def print_non_terminals(self):
        print("Non-terminals:", self.get_non_terminals())

    def print_terminals(self):
        print("Terminals:", self.get_terminals())

    def print_productions(self):
        print("Productions:")
        for head, bodies in self.get_productions().items():
            print(f"  {head} -> {' | '.join(bodies)}")

    def print_productions_for_non_terminal(self, non_terminal):
        productions = self.get_productions_for_non_terminal(non_terminal)
        if productions:
            print(f"Productions for {non_terminal}: {' | '.join(productions)}")
        else:
            print(f"No productions found for {non_terminal}")

    def print_cfg_check(self):
        print("Is the grammar context-free?", self.is_cfg())


# Example usage:
# g = Grammar("g1.txt")
# g.print_productions()
# g.print_terminals()
# g.print_non_terminals()
# g.print_productions_for_non_terminal("A")
# g.print_productions_for_non_terminal("D")
# g.print_cfg_check()
