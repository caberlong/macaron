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

class AlphaAdvantageParser:
  def __init__(self):
    self._generator = data_proto_generator.DataProtoGenerator()
    pass

  def parse(self, config: config_pb2.AlphaAdvantageParserConfig):
    assert config.raw_data_dir
    assert config.output_dir

    symbols = self.getSymbolsInRawDataDir(config.raw_data_dir)
    dates = self.getDatesFromConfig(config)
    for symbol in symbols.keys():
      if config.symbols and not symbol in config.symbols:
        continue
      protos = self.parseOneSymbol(
          symbol, symbols[symbol], dates, self.getMaxHistoricalPriceCount(config))
      for proto in protos:
        self.outputProto(config.output_dir, proto)

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

  def parseOneSymbol(self, symbol:str, paths:list, dates:list, max_historical_price_count:int): 
    protos = []
    for date in dates:
      data_proto = self.createDataProto(symbol, date)
      protos.append(data_proto)
    for path in paths:
      self.populateDataProtos(path, protos, max_historical_price_count)
    return protos

  def outputProto(self, output_dir:str, proto:data_pb2.Data): 
    output_path = self.getDataProtoOutputPath(output_dir, proto)
    if os.path.isfile(output_path) and os.path.getsize(output_path) > 1000:  
      return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:                                                                                            
      f = open(output_path, 'wb')                                                                           
      f.write(proto.SerializeToString())
      f.close()                                                                                     
    except e:                                                                                       
      print(e)

  def getDataProtoOutputPath(self, output_dir:str, proto:data_pb2.Data):
    return '/'.join([
      output_dir,
      datetime.datetime.fromtimestamp(_getTimeSerialTimestamp(proto)).date().isoformat(),
      '.'.join([_getSymbol(proto), 'proto'])
    ])

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

  def getMaxHistoricalPriceCount(self, config: config_pb2.AlphaAdvantageParserConfig):
    if config.max_historical_price_count and config.max_historical_price_count > 0:
      return config.max_historical_price_count 
    return _default_max_historical_price_count

  class Listener(JSONListener):                                                         
    def __init__(self, data_protos: list, max_historical_price_count:int):                                                        
      self._data_protos = data_protos
      self._generator = data_proto_generator.DataProtoGenerator()
      # for fundamentals
      self._current_earning_timestamp = None
      # for time serials
      self._current_time_serial_timestamp = None
      self._keys = []
      self._max_historical_price_count = max_historical_price_count
                                                                                                    
    def enterPair(self, ctx:JSONParser.PairContext):                                               
      key = ctx.STRING().getText()[1:-1]
      value = ctx.value().getText()[1:-1]
      self._keys.append(key)
      if key == 'fiscalDateEnding':
        self._current_earning_timestamp = _isoformatTimestamp(value)
        assert self._current_earning_timestamp > _isoformatTimestamp('1980-01-01')
      elif re.match(r'^\d{4}-\d{2}-\d{2}$', key):
        self._current_time_serial_timestamp = _isoformatTimestamp(key)
      elif (key == 'totalRevenue') and self.isQuarterlyReports():
        assert self._current_earning_timestamp
        self.setQuarterEarningTimestamps(self._current_earning_timestamp)
        self.setFundamentals(_set_data_proto_total_revenue, float(value))
        self.setNextQuarterFundamentals(_set_data_proto_next_quarter_total_revenue, float(value))
      elif (key == 'netIncome') and self.isQuarterlyReports():
        assert self._current_earning_timestamp
        self.setFundamentals(_set_data_proto_net_income, float(value))
      elif (key == 'grossProfit') and self.isQuarterlyReports():
        assert self._current_earning_timestamp
        self.setFundamentals(_set_data_proto_gross_profit, float(value))
      elif key == 'Sector':
        self.setTraits(_set_data_proto_sector, value)
      elif key == 'Industry':
        self.setTraits(_set_data_proto_industry, value)
      # time serials
      elif key == _time_serials_open_key:
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

  def populateDataProtos(self, path:str, protos:list, max_historical_price_count:int):
    input = FileStream(path, encoding='utf-8')                                  
    lexer = JSONLexer(input)                                                                  
    token = CommonTokenStream(lexer)                                                                
    parser = JSONParser(token)                                                                     
    tree = parser.json()                                                                     
    walker = ParseTreeWalker()                                                                      
    walker.walk(self.Listener(protos, max_historical_price_count), tree)                        
    
