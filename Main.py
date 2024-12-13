# Example Usage
from Grammar import Grammar
from LL1Parser import LL1Parser
from ParserOutput import ParserOutput

g = Grammar("g1.txt")
parser = LL1Parser(g)
parser.compute_first_sets()
parser.compute_follow_sets()

# Print sets and parse table
parser.print_first_sets()
parser.print_follow_sets()

parser.construct_parse_table()
parser.print_parse_table()

# Tokens to parse
tokens = ["a", "*", "(", "a", "+", "a", ")", "$"]
success = parser.parse_tokens(tokens)
if success:
    print("Input successfully parsed!")
    parser.parser_output.print_tree()
else:
    print("Input rejected.")
