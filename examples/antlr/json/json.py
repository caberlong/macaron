import sys
from antlr4 import *
from JSONLexer import JSONLexer
from JSONParser import JSONParser


def main(argv):
    input = FileStream(argv[1])
    lexer = JSONLexer(input)
    stream = CommonTokenStream(lexer)
    parser = JSONParser(stream)
    tree = parser.json()
    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)
