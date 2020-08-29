import os
import sys
import datetime
from antlr4 import *                                                                                

from JSONLexer import JSONLexer                                                         
from JSONParser import JSONParser
from JSONListener import JSONListener                                       

from proto.source import alpha_advantage_parser_config_pb2 as config_pb2
from proto import data_pb2
from data.utils import data_proto_generator


# default maximum historical price count in each trading activity. 
_default_max_historical_price_count = 100
_default_earliest_date = datetime.date.fromisoformat('2018-01-01')

class AlphaAdvantageParser:
  def __init__(self):
    pass

  def parse(self, config: config_pb2.AlphaAdvantageParserConfig):
    assert config.raw_data_dir
    assert config.output_dir

    symbols = self.getSymbolsInRawDataDir(config.raw_data_dir)
    dates = self.getDatesFromConfig(config)
    for symbol in symbols.keys():
      if config.symbols and not symbol in config.symbols:
        continue
      self.parseOneSymbol(symbol, symbols[symbol], dates, self.getMaxHistoricalPriceCount(config))

  def getSymbolsInRawDataDir(self, raw_data_dir:str):
    results = {}
    for root, dirs, files in os.walk(raw_data_dir): 
      for f in files:
        if not f.endswith('.json'):
           continue
        symbol = os.path.splitext(f)[0]
        results.setdefault(symbol, [])
        results[symbol].append('/'.join([root, f]))
    return results

  def getDatesFromConfig(self, config: config_pb2.AlphaAdvantageParserConfig):
    earliest = _default_earliest_date
    latest = datetime.date.today()
    if config.earliest_timestamp: 
      e = config.earliest_timestamp.ToDatetime().date()
      if e > earliest and e < latest: 
        earliest = e

    if config.latest_timestamp:
      l = config.latest_timestamp.ToDatetime().date()
      if l < latest and l > earliest:
        latest = l

    results = []
    d = earliest
    while d <= latest:
      results.append(d.isoformat())
      d = d + datetime.timedelta(1)
    return results

  def parseOneSymbol(self, symbol:str, paths:list, dates:list, max_historical_price_count:int): 
    print('Parse %s from %s for dates %s, max history %d' % (
        symbol, paths, dates, max_historical_price_count))

  def getMaxHistoricalPriceCount(self, config: config_pb2.AlphaAdvantageParserConfig):
    if config.max_historical_price_count and config.max_historical_price_count > 0:
      return config.max_historical_price_count 
    return _default_max_historical_price_count
