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
    
# Key: json path 
# Value: (config, overwrite)
_jsonKeyToGeneratorConfigMap = { 
  # profile
  _summaryStore(['summaryProfile', 'longBusinessSummary']):
    (_commonTraitConfig('business_summary : $STRING;'), True),
  _summaryStore(['summaryProfile', 'sector']):
    (_commonTraitConfig('sector : $STRING;'), True),
  _summaryStore(['summaryProfile', 'industry']):
    (_commonTraitConfig('industry : $STRING;'), True),
  _summaryStore(['summaryProfile', 'fullTimeEmployees']):
    (_commonTraitConfig('num_full_time_employees : $NUMBER;'), True),

  # price
  _summaryStore(['price', 'marketCap', 'raw']):
    (_commonTraitConfig('market_cap : $NUMBER;'), True),
  _summaryStore(['price', 'symbol']):
    (_commonTraitConfig('symbol : $STRING;'), True),
  _summaryStore(['price', 'quoteType']):
    (_commonTraitConfig('quote_type : $STRING;'), True),

  # financial data
  _summaryStore(['financialData', 'currentPrice', 'raw']):
    (_commonTraitConfig('current_price : $NUMBER;'), True),
  _summaryStore(['financialData', 'profitMargins', 'raw']):
    (_commonTraitConfig('profit_margin : $NUMBER;'), True),
  _summaryStore(['financialData', 'grossMargins', 'raw']):
    (_commonTraitConfig('gross_margin : $NUMBER;'), True),
  _summaryStore(['financialData', 'operatingMargins', 'raw']):
    (_commonTraitConfig('operating_margin : $NUMBER;'), True),
  _summaryStore(['financialData', 'operatingCashflow', 'raw']):
    (_commonTraitConfig('operating_cash_flow : $NUMBER;'), True),
  _summaryStore(['financialData', 'ebitdaMargins', 'raw']):
    (_commonTraitConfig('ebitda_margin : $NUMBER;'), True),
  _summaryStore(['financialData', 'ebitda', 'raw']):
    (_commonTraitConfig('ebitda : $NUMBER;'), True),
  _summaryStore(['financialData', 'totalCash', 'raw']):
    (_commonTraitConfig('total_cash : $NUMBER;'), True),
  _summaryStore(['financialData', 'totalDebt', 'raw']):
    (_commonTraitConfig('total_debt : $NUMBER;'), True),
  _summaryStore(['financialData', 'totalRevenue', 'raw']):
    (_commonTraitConfig('total_revenue : $NUMBER;'), True),
  _summaryStore(['financialData', 'grossProfits', 'raw']):
    (_commonTraitConfig('gross_profit : $NUMBER;'), True),
  _summaryStore(['financialData', 'freeCashflow', 'raw']):
    (_commonTraitConfig('free_cash_flow : $NUMBER;'), True),
  _summaryStore(['financialData', 'revenueGrowth', 'raw']):
    (_commonTraitConfig('revenue_growth : $NUMBER;'), True),
  _summaryStore(['financialData', 'earningsGrowth', 'raw']):
    (_commonTraitConfig('earnings_growth : $NUMBER;'), True),
  _summaryStore(['financialData', 'numberOfAnalystOpinions', 'raw']):
    (_commonTraitConfig('num_analyst_opinions : $NUMBER;'), True),
  _summaryStore(['financialData', 'targetLowPrice', 'raw']):
    (_commonTraitConfig('target_low_price : $NUMBER;'), True),
  _summaryStore(['financialData', 'targetMeanPrice', 'raw']):
    (_commonTraitConfig('target_mean_price : $NUMBER;'), True),
  _summaryStore(['financialData', 'targetMedianPrice', 'raw']):
    (_commonTraitConfig('target_median_price : $NUMBER;'), True),
  _summaryStore(['financialData', 'targetHighPrice', 'raw']):
    (_commonTraitConfig('target_high_price : $NUMBER;'), True),
  _summaryStore(['financialData', 'recommendationKey']):
    (_commonTraitConfig('recommendation_key : $STRING;'), True),
  _summaryStore(['financialData', 'debtToEquity', 'raw']):
    (_commonTraitConfig('debt_to_equity : $NUMBER;'), True),
  _summaryStore(['financialData', 'returnOnAssets', 'raw']):
    (_commonTraitConfig('return_on_assets : $NUMBER;'), True),
  _summaryStore(['financialData', 'returnOnEquity', 'raw']):
    (_commonTraitConfig('return_on_equity : $NUMBER;'), True),
  _summaryStore(['financialData', 'financialCurrency']):
    (_commonTraitConfig('currency : $STRING;'), True),
  _summaryStore(['financialData', 'earningsGrowth', 'raw']):
    (_commonTraitConfig('earning_growth : $NUMBER;'), True),
  _summaryStore(['financialData', 'totalCashPerShare', 'raw']):
    (_commonTraitConfig('total_cash_per_share : $NUMBER;'), True),
  _summaryStore(['financialData', 'revenuePerShare', 'raw']):
    (_commonTraitConfig('revenue_per_share : $NUMBER;'), True),
  _summaryStore(['financialData', 'currentRatio', 'raw']):
    (_commonTraitConfig('current_ratio : $NUMBER;'), True),
  _summaryStore(['financialData', 'quickRatio', 'raw']):
    (_commonTraitConfig('quick_ratio : $NUMBER;'), True),
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
