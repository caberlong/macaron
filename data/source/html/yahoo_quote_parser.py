import sys
from antlr4 import *                                                                                

from YahooQuoteLexer import YahooQuoteLexer                                                         
from YahooQuoteParser import YahooQuoteParser as AntlrParser
from YahooQuoteParserListener import YahooQuoteParserListener                                       

from data.proto.source import yahoo_quote_parser_config_pb2 as config_pb2
from data.proto import data_pb2
from macaron.data.utils import data_proto_generator

SUMMARY_STORE = 'context.dispatcher.stores.QuoteSummaryStore'

def _summaryStore(paths: list):
  return '.'.join([SUMMARY_STORE, '.'.join(paths)])

def _commonTraitConfig(config: str):
  return 'fin_entity { traits { common_trait { %s } } }' % config
    
_jsonKeyToGeneratorConfigMap = { 
  _summaryStore(['summaryProfile', 'longBusinessSummary']):
    (_commonTraitConfig('business_summary : $STRING;'), True),
  _summaryStore(['summaryProfile', 'sector']):
    (_commonTraitConfig('sector : $STRING;'), True),
  _summaryStore(['summaryProfile', 'industry']):
    (_commonTraitConfig('industry : $STRING;'), True),
  _summaryStore(['summaryProfile', 'fullTimeEmployees']):
    (_commonTraitConfig('num_full_time_employees : $NUMBER;'), True)
}
                                                                                                    
class YahooQuoteParser:
  def __init__(self):
    pass

  class Listener(YahooQuoteParserListener):                                                      
    def __init__(self, data: data_pb2.Data):
      self._keys = []
      self._data = data
      self._generator = data_proto_generator.DataProtoGenerator()
                                                                                                      
    def enterPair(self, ctx:AntlrParser.PairContext):                                            
      self._keys.append(ctx.STRING().getText()[1:-1])
                                                                                                      
    def exitPair(self, ctx:AntlrParser.PairContext):                                             
      self._keys.pop()                                                                                
                                                                                                      
    def enterValue(self, ctx:AntlrParser.ValueContext):                                          
      if ctx.TRUE() or ctx.FALSE() or ctx.NULL():
        return
      if ctx.STRING():                                                                                
        self.populate_string_values(ctx.STRING().getText()[1:-1])
      if ctx.NUMBER():                                                                                
        self.populate_number_values(ctx.NUMBER().getText())
        return

    def populate_string_values(self, value: str):
      (config, overwrite) = _jsonKeyToGeneratorConfigMap.get('.'.join(self._keys), (None, None))
      if config:
        self._generator.generateDataProto(
            config=config, data=self._data, overwrite=overwrite, var_values={'STRING':value})

    def populate_number_values(self, value: str):
      (config, overwrite) = _jsonKeyToGeneratorConfigMap.get('.'.join(self._keys), (None, None))
      if config:
        self._generator.generateDataProto(
            config=config, data=self._data, overwrite=overwrite, var_values={'NUMBER':value})
        
                                                                                                      
  def parse(self, config: config_pb2.YahooQuoteParserConfig, data: data_pb2.Data):
    if config.local_file_path:
      input = FileStream(config.local_file_path, encoding='utf-8')                                                     
    lexer = YahooQuoteLexer(input)                                                                    
    token = CommonTokenStream(lexer)
    parser = AntlrParser(token)
    tree = parser.yahoo_quote()                                                                       
    walker = ParseTreeWalker()
    walker.walk(self.Listener(data), tree)
