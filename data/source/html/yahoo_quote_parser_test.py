import sys
from antlr4 import *
from YahooQuoteLexer import YahooQuoteLexer
from YahooQuoteParser import YahooQuoteParser


def main(argv):
    input = FileStream(argv[1], encoding='utf-8')
    lexer = YahooQuoteLexer(input)
    stream = CommonTokenStream(lexer)
    parser = YahooQuoteParser(stream)
    tree = parser.yahoo_quote()
    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)
