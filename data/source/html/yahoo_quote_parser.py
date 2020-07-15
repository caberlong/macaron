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
  return ('fin_entity { traits { common_trait { %s } } }' % config, data_pb2.Data.FIN_ENTITY)

def _tradingActivityConfig(config: str):
  return ('timeline { activities { trading_activity { %s } } }' % config, data_pb2.Data.TIMELINE)
    
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

  # trading activity
  _summaryStore(['summaryProfile', 'fullTimeEmployees']):
    (_tradingActivityConfig('num_full_time_employees : $NUMBER;'), True),
  _summaryStore(['price', 'marketCap', 'raw']):
    (_tradingActivityConfig('market_cap : $NUMBER;'), True),
  _summaryStore(['price', 'symbol']):
    (_tradingActivityConfig('symbol : $STRING;'), True),
  _summaryStore(['price', 'quoteType']):
    (_tradingActivityConfig('quote_type : $STRING;'), True),
  _summaryStore(['financialData', 'currentPrice', 'raw']):
    (_tradingActivityConfig('price : $NUMBER;'), True),
  _summaryStore(['financialData', 'profitMargins', 'raw']):
    (_tradingActivityConfig('profit_margin : $NUMBER;'), True),
  _summaryStore(['financialData', 'grossMargins', 'raw']):
    (_tradingActivityConfig('gross_margin : $NUMBER;'), True),
  _summaryStore(['financialData', 'operatingMargins', 'raw']):
    (_tradingActivityConfig('operating_margin : $NUMBER;'), True),
  _summaryStore(['financialData', 'operatingCashflow', 'raw']):
    (_tradingActivityConfig('operating_cash_flow : $NUMBER;'), True),
  _summaryStore(['financialData', 'ebitdaMargins', 'raw']):
    (_tradingActivityConfig('ebitda_margin : $NUMBER;'), True),
  _summaryStore(['financialData', 'ebitda', 'raw']):
    (_tradingActivityConfig('ebitda : $NUMBER;'), True),
  _summaryStore(['financialData', 'totalCash', 'raw']):
    (_tradingActivityConfig('total_cash : $NUMBER;'), True),
  _summaryStore(['financialData', 'totalDebt', 'raw']):
    (_tradingActivityConfig('total_debt : $NUMBER;'), True),
  _summaryStore(['financialData', 'totalRevenue', 'raw']):
    (_tradingActivityConfig('total_revenue : $NUMBER;'), True),
  _summaryStore(['financialData', 'grossProfits', 'raw']):
    (_tradingActivityConfig('gross_profit : $NUMBER;'), True),
  _summaryStore(['financialData', 'freeCashflow', 'raw']):
    (_tradingActivityConfig('free_cash_flow : $NUMBER;'), True),
  _summaryStore(['financialData', 'revenueGrowth', 'raw']):
    (_tradingActivityConfig('revenue_growth : $NUMBER;'), True),
  _summaryStore(['financialData', 'earningsGrowth', 'raw']):
    (_tradingActivityConfig('earnings_growth : $NUMBER;'), True),
  _summaryStore(['financialData', 'numberOfAnalystOpinions', 'raw']):
    (_tradingActivityConfig('num_analyst_opinions : $NUMBER;'), True),
  _summaryStore(['financialData', 'targetLowPrice', 'raw']):
    (_tradingActivityConfig('target_low_price : $NUMBER;'), True),
  _summaryStore(['financialData', 'targetMeanPrice', 'raw']):
    (_tradingActivityConfig('target_mean_price : $NUMBER;'), True),
  _summaryStore(['financialData', 'targetMedianPrice', 'raw']):
    (_tradingActivityConfig('target_median_price : $NUMBER;'), True),
  _summaryStore(['financialData', 'targetHighPrice', 'raw']):
    (_tradingActivityConfig('target_high_price : $NUMBER;'), True),
  _summaryStore(['financialData', 'recommendationKey']):
    (_tradingActivityConfig('recommendation_key : $STRING;'), True),
  _summaryStore(['financialData', 'debtToEquity', 'raw']):
    (_tradingActivityConfig('debt_to_equity : $NUMBER;'), True),
  _summaryStore(['financialData', 'returnOnAssets', 'raw']):
    (_tradingActivityConfig('return_on_assets : $NUMBER;'), True),
  _summaryStore(['financialData', 'returnOnEquity', 'raw']):
    (_tradingActivityConfig('return_on_equity : $NUMBER;'), True),
  _summaryStore(['financialData', 'financialCurrency']):
    (_tradingActivityConfig('currency : $STRING;'), True),
  _summaryStore(['financialData', 'earningsGrowth', 'raw']):
    (_tradingActivityConfig('earning_growth : $NUMBER;'), True),
  _summaryStore(['financialData', 'totalCashPerShare', 'raw']):
    (_tradingActivityConfig('total_cash_per_share : $NUMBER;'), True),
  _summaryStore(['financialData', 'revenuePerShare', 'raw']):
    (_tradingActivityConfig('revenue_per_share : $NUMBER;'), True),
  _summaryStore(['financialData', 'currentRatio', 'raw']):
    (_tradingActivityConfig('current_ratio : $NUMBER;'), True),
  _summaryStore(['financialData', 'quickRatio', 'raw']):
    (_tradingActivityConfig('quick_ratio : $NUMBER;'), True),
}
                                                                                                    
class YahooQuoteParser:
  def __init__(self):
    pass

  class Listener(YahooQuoteParserListener):                                                      
    def __init__(self, fin_entity: data_pb2.Data, activity: data_pb2.Data):
      self._keys = []
      self._fin_entity = fin_entity
      self._activity = activity
      self._generator = data_proto_generator.DataProtoGenerator()
                                                                                                      
    def enterPair(self, ctx:AntlrParser.PairContext):                                            
      self._keys.append(ctx.STRING().getText()[1:-1])
                                                                                                      
    def exitPair(self, ctx:AntlrParser.PairContext):                                             
      self._keys.pop()                                                                                
                                                                                                      
    def enterValue(self, ctx:AntlrParser.ValueContext):                                          
      if ctx.TRUE() or ctx.FALSE() or ctx.NULL():
        return
      if ctx.STRING():                                                                                
        self.populateStringValues(ctx.STRING().getText()[1:-1])
      if ctx.NUMBER():                                                                                
        self.populateNumberValues(ctx.NUMBER().getText())
        return

    def populateStringValues(self, value: str):
      ((config, data_type), overwrite) = _jsonKeyToGeneratorConfigMap.get(
          '.'.join(self._keys), ((None, None), None))
      if config:
        self._generator.generateDataProto(
            config=config,
            data=self.getDataByType(data_type),
            overwrite=overwrite,
            var_values={'STRING':value})

    def populateNumberValues(self, value: str):
      ((config, data_type), overwrite) = _jsonKeyToGeneratorConfigMap.get(
          '.'.join(self._keys), ((None, None), None))
      if config:
        self._generator.generateDataProto(
            config=config,
            data=self.getDataByType(data_type),
            overwrite=overwrite,
            var_values={'NUMBER':value})

    def getDataByType(self, data_type: data_pb2.Data.DataType):
      if data_type == data_pb2.Data.FIN_ENTITY:
        return self._fin_entity
      if data_type == data_pb2.Data.TIMELINE:
        return self._activity
      raise
        
                                                                                                      
  def parse(self,
            config: config_pb2.YahooQuoteParserConfig,
            fin_entity: data_pb2.Data,
            activity: data_pb2.Data):
    if config.local_file_path:
      input = FileStream(config.local_file_path, encoding='utf-8')                                                     
    lexer = YahooQuoteLexer(input)                                                                    
    token = CommonTokenStream(lexer)
    parser = AntlrParser(token)
    tree = parser.yahoo_quote()                                                                       
    walker = ParseTreeWalker()
    walker.walk(self.Listener(fin_entity, activity), tree)
