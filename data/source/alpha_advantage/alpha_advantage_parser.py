import os
import sys
import datetime
import re
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

_time_serials_open_key = '1. open'
_time_serials_high_key = '2. high'
_time_serials_low_key = '3. low'
_time_serials_close_key = '4. close'
_time_serials_volume_key = '6. volume'
_time_serials_dividend_key = '7. dividend amount'
_time_serials_split_key = '8. split coefficient'


# config for generating data proto
_set_data_proto_symbol = 'timelines { activities { trading_activity { symbol : $STRING; } } }'
_set_data_proto_timestamp = """
  timelines {
    activities {
      trading_activity {
        activity_timestamp {
          start_timestamp {
            seconds : $INT;  
          }
        }
      }
    }
  } """
_set_data_proto_last_quarter_earning_timestamp = """
  timelines {
    activities {
      trading_activity {
        last_quarter_earning_timestamp {
          seconds: $INT;
        }
      }
    }
  } """
_set_data_proto_next_quarter_earning_timestamp = """
  timelines {
    activities {
      trading_activity {
        next_quarter_earning_timestamp {
          seconds: $INT;
        }
      }
    }
  } """
_set_data_proto_total_revenue = """
  timelines {
    activities {
      trading_activity {
        total_revenue : $FLOAT;
      }
    }
  } """
_set_data_proto_next_quarter_total_revenue = """
  timelines {
    activities {
      trading_activity {
        next_quarter_total_revenue : $FLOAT;
      }
    }
  } """
_set_data_proto_net_income = """
  timelines {
    activities {
      trading_activity {
        net_income : $FLOAT;
      }
    }
  } """
_set_data_proto_gross_profit = """
  timelines {
    activities {
      trading_activity {
        gross_profit : $FLOAT;
      }
    }
  } """
_set_data_proto_price = """
  timelines {
    activities {
      trading_activity {
        price : $FLOAT;
      }
    }
  } """
_set_data_proto_shares_outstanding = """
  timelines {
    activities {
      trading_activity {
        shares_outstanding : $INT;
      }
    }
  } """
_set_data_proto_num_full_time_employees = """
  timelines {
    activities {
      trading_activity {
        num_full_time_employees : $INT;
      }
    }
  } """
_set_data_proto_sector = """
  timelines {
    fin_entity {
      traits {
        common_trait {
          sector : $STRING;
        }
      }
    }
  } """
_set_data_proto_industry = """
  timelines {
    fin_entity {
      traits {
        common_trait {
          industry : $STRING;
        }
      }
    }
  } """
_set_data_proto_common_trait_symbol = """
  timelines {
    fin_entity {
      traits {
        common_trait {
          symbol : $STRING;
        }
      }
    }
  } """

# time serials
_set_data_proto_open = """
  timelines {
    activities {
      trading_activity {
        historical_prices {
          open : $FLOAT;
        }
      }
    }
  } """
_set_data_proto_high = """
  timelines {
    activities {
      trading_activity {
        historical_prices {
          high : $FLOAT;
        }
      }
    }
  } """
_set_data_proto_low = """
  timelines {
    activities {
      trading_activity {
        historical_prices {
          low : $FLOAT;
        }
      }
    }
  } """
_set_data_proto_close = """
  timelines {
    activities {
      trading_activity {
        historical_prices {
          close : $FLOAT;
        }
      }
    }
  } """
_set_data_proto_volume = """
  timelines {
    activities {
      trading_activity {
        historical_prices {
          volume : $INT;
        }
      }
    }
  } """
_set_data_proto_historical_timestamp = """
  timelines {
    activities {
      trading_activity {
        historical_prices {
          timestamp {
            seconds : $INT;
          }
        }
      }
    }
  } """
_set_data_proto_dividend = """
  timelines {
    activities {
      trading_activity {
        historical_prices {
          dividend : $FLOAT;
        }
      }
    }
  } """
_set_data_proto_split = """
  timelines {
    activities {
      trading_activity {
        historical_prices {
          split : $FLOAT;
        }
      }
    }
  } """

def _getSymbol(data_proto:data_pb2.Data):                                                   
  return data_proto.timelines[0].fin_entity.traits[0].common_trait.symbol

def _getTimeSerialTimestamp(data_proto:data_pb2.Data):                                                   
  return (data_proto.timelines[0].activities[0]                                                 
      .trading_activity.activity_timestamp.start_timestamp.seconds)                             
                                                                                                
def _getLastQuarterEarningTimestamp(data_proto:data_pb2.Data):                                           
  return (data_proto.timelines[0].activities[0]                                                 
      .trading_activity.last_quarter_earning_timestamp.seconds)                                 
                                                                                                
def _getNextQuarterEarningTimestamp(data_proto):                                           
  return (data_proto.timelines[0].activities[0]                                                 
      .trading_activity.next_quarter_earning_timestamp.seconds)                                 
                                                                                                
def _isoformatTimestamp(isoformat:str):                                                    
  dt = datetime.date.fromisoformat(isoformat)                                                   
  result = int(datetime.datetime(dt.year, dt.month, dt.day).timestamp())                        
  return result 

def _getDataProtoOutputPath(output_dir:str, symbol:str, date_isoformat:str):
  return '/'.join([output_dir, date_isoformat, '.'.join([symbol, 'proto'])])

def _readDataProto(output_path:str):
  data = data_pb2.Data()                                                                            
  if not os.path.isfile(output_path):
    return None
  try:
    f = open(output_path, 'rb')
    data.ParseFromString(f.read())                                                                    
    f.close()  
    return data
  except e:
    print('%s' % e)

def _getMaxHistoricalPriceCount(config: config_pb2.AlphaAdvantageParserConfig):              
  if config.max_historical_price_count and config.max_historical_price_count > 0:                 
    return config.max_historical_price_count                                                      
  return _default_max_historical_price_count 

class AlphaAdvantageParser:
  def __init__(self):
    self._generator = data_proto_generator.DataProtoGenerator()
    pass

  def parse(self, parser_config: config_pb2.AlphaAdvantageParserConfig):
    assert parser_config.raw_data_dir
    assert parser_config.output_dir

    symbols = self.getSymbolsInRawDataDir(parser_config.raw_data_dir)
    dates = self.getDatesFromConfig(parser_config)
    for symbol in symbols.keys():
      if parser_config.symbols and not symbol in parser_config.symbols:
        continue
      protos = self.parseOneSymbol(symbol, symbols[symbol], dates, parser_config)
      for proto in protos:
        self.outputProto(parser_config.output_dir, proto, parser_config.print_only)

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
      results.append(d)
      d = d + datetime.timedelta(1)
    return results

  def parseOneSymbol(
      self,
      symbol:str,
      paths:list,
      dates:list,
      parser_config:config_pb2.AlphaAdvantageParserConfig): 
    protos = []
    output_dir = parser_config.output_dir
    for date in dates:
      output_path = _getDataProtoOutputPath(parser_config.output_dir, symbol, date.isoformat())
      if os.path.isfile(output_path) and os.path.getsize(output_path) > 128:  
        if parser_config.skip_existing:
          continue
        else:
          data_proto = _readDataProto(output_path)
      else:
        data_proto = self.createDataProto(symbol, date)
      protos.append(data_proto)
    if not protos:
      return protos
    for path in paths:
      self.populateDataProtos(path, protos, parser_config)
    return protos

  def outputProto(self, output_dir:str, proto:data_pb2.Data, print_only:bool): 
    output_path = self.getDataProtoOutputPath(output_dir, proto)
    if print_only:
      print('write to %s' % output_path)
      print('%s' % proto) 
      return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:                                                                                            
      f = open(output_path, 'wb')                                                                           
      f.write(proto.SerializeToString())
      f.close()                                                                                     
    except e:                                                                                       
      print(e)

  def getDataProtoOutputPath(self, output_dir:str, proto:data_pb2.Data):
    date_isoformat = datetime.datetime.fromtimestamp(
        _getTimeSerialTimestamp(proto)).date().isoformat()
    return _getDataProtoOutputPath(output_dir, _getSymbol(proto), date_isoformat)

  def createDataProto(self, symbol:str, date:datetime.date):
    data_proto = data_pb2.Data() 
    self._generator.generateDataProto(                                                          
        config=_set_data_proto_symbol,
        output_proto=data_proto,
        var_values={'STRING':symbol})
    self._generator.generateDataProto(                                                          
        config=_set_data_proto_common_trait_symbol,
        output_proto=data_proto,
        var_values={'STRING':symbol})
    timestamp = int(datetime.datetime(date.year, date.month, date.day).timestamp())
    self._generator.generateDataProto(                                                          
        config=_set_data_proto_timestamp,
        output_proto=data_proto,
        var_values={'INT':timestamp})
    return data_proto

  class Listener(JSONListener):                                                         
    def __init__(self, data_protos: list, parser_config:config_pb2.AlphaAdvantageParserConfig):                                                        
      self._data_protos = data_protos
      self._generator = data_proto_generator.DataProtoGenerator()
      self._current_earning_timestamp = None
      self._current_time_serial_timestamp = None
      self._keys = []
      self._parser_config = parser_config
      self._max_historical_price_count = _getMaxHistoricalPriceCount(parser_config)
                                                                                                    
    def enterPair(self, ctx:JSONParser.PairContext):                                               
      key = ctx.STRING().getText()[1:-1]
      value = ctx.value().getText()[1:-1]
      self._keys.append(key)
      if value == 'None':
        return
      if key == 'fiscalDateEnding':
        self._current_earning_timestamp = _isoformatTimestamp(value)
        assert self._current_earning_timestamp > _isoformatTimestamp('1980-01-01')
        return
      if re.match(r'^\d{4}-\d{2}-\d{2}$', key):
        self._current_time_serial_timestamp = _isoformatTimestamp(key)
        return
      if (key == 'totalRevenue') and self.isQuarterlyReports():
        self.parseTotalRevenue(value)
        return
      if (key == 'netIncome') and self.isQuarterlyReports():
        assert self._current_earning_timestamp
        self.setFundamentals(_set_data_proto_net_income, float(value))
        return
      if (key == 'grossProfit') and self.isQuarterlyReports():
        assert self._current_earning_timestamp
        self.setFundamentals(_set_data_proto_gross_profit, float(value))
        return
      if key == 'SharesOutstanding':
        self.setTraits(_set_data_proto_shares_outstanding, int(value))
        return
      if key == 'FullTimeEmployees':
        self.setTraits(_set_data_proto_num_full_time_employees, int(value))
        return
      if key == 'Sector':
        self.setTraits(_set_data_proto_sector, value)
        return
      if key == 'Industry':
        self.setTraits(_set_data_proto_industry, value)
        return

      self.parseTimeSerials(key, value)

    def parseTimeSerials(self, key:str, value:str):
      if key == _time_serials_open_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(
            _set_data_proto_open, float(value), new_repeats={'historical_prices': None})
        self.setTimeSerials(
            _set_data_proto_historical_timestamp, self._current_time_serial_timestamp)
      elif key == _time_serials_high_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(_set_data_proto_high, float(value))
      elif key == _time_serials_low_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(_set_data_proto_low, float(value))
      elif key == _time_serials_close_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(_set_data_proto_close, float(value))
        self.setPrice(float(value))
      elif key == _time_serials_volume_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(_set_data_proto_volume, int(value))
      elif key == _time_serials_dividend_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(_set_data_proto_dividend, float(value))
      elif key == _time_serials_split_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(_set_data_proto_split, float(value))

    def parseTotalRevenue(self, value:str):
      assert self._current_earning_timestamp
      self.setQuarterEarningTimestamps(self._current_earning_timestamp)
      self.setFundamentals(_set_data_proto_total_revenue, float(value))
      self.setNextQuarterFundamentals(_set_data_proto_next_quarter_total_revenue, float(value))

    def setQuarterEarningTimestamps(self, timestamp):
      for data_proto in self._data_protos:
        if _getTimeSerialTimestamp(data_proto) > timestamp:
          if timestamp > _getLastQuarterEarningTimestamp(data_proto):
            self.setFundamental(
                data_proto, _set_data_proto_last_quarter_earning_timestamp, timestamp)
        if _getTimeSerialTimestamp(data_proto) < timestamp:
          if (not _getNextQuarterEarningTimestamp(data_proto) or
              (timestamp < _getNextQuarterEarningTimestamp(data_proto))):
            self.setFundamental(
                data_proto, _set_data_proto_next_quarter_earning_timestamp, timestamp)

    def setFundamentals(self, config:str, value):
      for data_proto in self._data_protos:
        if self._current_earning_timestamp == _getLastQuarterEarningTimestamp(data_proto):
          self.setFundamental(data_proto, config, value)

    def setNextQuarterFundamentals(self, config:str, value):
      for data_proto in self._data_protos:
        if self._current_earning_timestamp == _getNextQuarterEarningTimestamp(data_proto):
          self.setFundamental(data_proto, config, value)

    def setFundamental(self, data_proto, config:str, value):
      value_key = 'STRING'
      if isinstance(value, int):
        value_key = 'INT'
      elif isinstance(value, float):
        value_key = 'FLOAT'
      self._generator.generateDataProto(                                                          
          config=config, output_proto=data_proto, var_values={value_key:value})

    def setPrice(self, value):
      for data_proto in self._data_protos:
        if self._current_time_serial_timestamp == _getTimeSerialTimestamp(data_proto):
          self.setFundamental(data_proto, _set_data_proto_price, value)

    def setTimeSerials(self, config:str, value, new_repeats:dict = None):
      for data_proto in self._data_protos:
        if ((self._current_time_serial_timestamp < _getTimeSerialTimestamp(data_proto)) and
            (self._current_time_serial_timestamp + self._max_historical_price_count * 24 * 3600 >=
             _getTimeSerialTimestamp(data_proto))):
          self.setTimeSerial(data_proto, config, value, new_repeats)

    def setTimeSerial(self, data_proto, config:str, value, new_repeats):
      if isinstance(value, int):
        value_key = 'INT'
      elif isinstance(value, float):
        value_key = 'FLOAT'
      self._generator.generateDataProto(                                                          
          config=config,
          output_proto=data_proto,
          new_repeats=new_repeats,
          var_values={value_key:value})

    def setTraits(self, config:str, value):
      for data_proto in self._data_protos:
        self.setFundamental(data_proto, config, value)
                                                                                                    
    def exitPair(self, ctx:JSONParser.PairContext):
      self._keys.pop()
      pass

    def isQuarterlyReports(self):
      return 'quarterlyReports' in self._keys

  def populateDataProtos(
      self, path:str, protos:list, parser_config:config_pb2.AlphaAdvantageParserConfig):
    input = FileStream(path, encoding='utf-8')                                  
    lexer = JSONLexer(input)                                                                  
    token = CommonTokenStream(lexer)                                                                
    parser = JSONParser(token)                                                                     
    tree = parser.json()                                                                     
    walker = ParseTreeWalker()                                                                      
    walker.walk(self.Listener(protos, parser_config), tree)
    
