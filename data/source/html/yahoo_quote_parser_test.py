import sys
from antlr4 import *
from YahooQuoteLexer import YahooQuoteLexer
from YahooQuoteParser import YahooQuoteParser
from YahooQuoteParserListener import YahooQuoteParserListener


class PrintListener(YahooQuoteParserListener):
	def __init__(self):
		self._keys = []

	def enterPair(self, ctx:YahooQuoteParser.PairContext):
		self._keys.append(ctx.STRING().getText())

	def exitPair(self, ctx:YahooQuoteParser.PairContext):
		self._keys.pop()

	def enterValue(self, ctx:YahooQuoteParser.ValueContext):
		if ctx.STRING():
			print("leaf string: keys=%s, value=%s" % ('.'.join(self._keys), ctx.STRING().getText()))
		if ctx.NUMBER():
			print("leaf number: keys=%s, value=%s" % ('.'.join(self._keys), ctx.NUMBER().getText()))
		if ctx.TRUE():
			print("leaf TRUE: keys=%s, value=%s" % ('.'.join(self._keys), ctx.TRUE().getText()))
		if ctx.FALSE():
			print("leaf FALSE: keys=%s, value=%s" % ('.'.join(self._keys), ctx.FALSE().getText()))
		if ctx.NULL():
			print("leaf NULL: keys=%s, value=%s" % ('.'.join(self._keys), ctx.NULL().getText()))


def main(argv):
	input = FileStream(argv[1], encoding='utf-8')
	lexer = YahooQuoteLexer(input)
	stream = CommonTokenStream(lexer)
	parser = YahooQuoteParser(stream)
	tree = parser.yahoo_quote()
	walker = ParseTreeWalker();
	listener = PrintListener();
	walker.walk(listener, tree);


if __name__ == '__main__':
	main(sys.argv)
