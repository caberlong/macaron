import sys
from antlr4 import *
from YAHOOQUOTELexer import YAHOOQUOTELexer
from YAHOOQUOTEParser import YAHOOQUOTEParser


def main(argv):
    input = FileStream(argv[1], encoding='utf-8')
    lexer = YAHOOQUOTELexer(input)
    stream = CommonTokenStream(lexer)
    parser = YAHOOQUOTEParser(stream)
    tree = parser.yahoo_quote()
    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)
