import sys                                                                                          
from antlr4 import *                                                                                
from JSONLexer import JSONLexer                                                                     
from JSONParser import JSONParser                                                                   
from JSONListener import JSONListener
                                                                                                    

class PrintListener(JSONListener):
  def __init__(self):
    pass

  def enterPair(self, ctx:JSONParser.PairContext):
    print("pair: %s: %s" % (ctx.STRING().getText(), ctx.value().getText()))


def main(argv):
	input = FileStream(argv[1], encoding='utf-8')
	lexer = JSONLexer(input)
	stream = CommonTokenStream(lexer)
	parser = JSONParser(stream)
	tree = parser.json()
	walker = ParseTreeWalker();
	listener = PrintListener();
	walker.walk(listener, tree);


if __name__ == '__main__':
	main(sys.argv)
