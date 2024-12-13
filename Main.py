# Example Usage
from Grammar import Grammar
from LL1Parser import LL1Parser
from ParserOutput import ParserOutput

g = Grammar("g1.txt")
parser = LL1Parser(g)

# Tokens to parse
tokens = ["a", "*", "(", "a", "+", "a", ")", "$"]
success = parser.parse_tokens(tokens)
parser_output= ParserOutput(parser)
if success:
    print("Input successfully parsed!")
    parser_output.print_all()
    parser_output.save_all_to_file("g1")
else:
    print("Input rejected.")
