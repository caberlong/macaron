import sys
from antlr4 import *                                                                                

from YahooQuoteLexer import YahooQuoteLexer                                                         
from YahooQuoteParser import YahooQuoteParser as AntlrParser
from YahooQuoteParserListener import YahooQuoteParserListener                                       

from data.proto.source import yahoo_quote_parser_config_pb2 as config_pb2
from data.proto import data_pb2
                                                                                                    
                                                                                                    
class YahooQuoteParser:
  def __init__(self):
    pass

  class Listener(YahooQuoteParserListener):                                                      
    def __init__(self, data: data_pb2.Data):
      self._keys = []
      self._data = data_pb2.Data
                                                                                                      
    def enterPair(self, ctx:AntlrParser.PairContext):                                            
      self._keys.append(ctx.STRING().getText()[1:-1])
                                                                                                      
    def exitPair(self, ctx:AntlrParser.PairContext):                                             
      self._keys.pop()                                                                                
                                                                                                      
    def enterValue(self, ctx:AntlrParser.ValueContext):                                          
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
                                                                                                      
                                                                                                      
  def parse(self, config: config_pb2.YahooQuoteParserConfig, data: data_pb2.Data):
    if config.local_file_path:
      input = FileStream(config.local_file_path, encoding='utf-8')                                                     
    lexer = YahooQuoteLexer(input)                                                                    
    token = CommonTokenStream(lexer)
    parser = AntlrParser(token)
    tree = parser.yahoo_quote()                                                                       
    walker = ParseTreeWalker()
    walker.walk(self.Listener(data), tree)
