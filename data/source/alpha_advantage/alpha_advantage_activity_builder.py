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


_time_serials_open_key = '1. open'
_time_serials_high_key = '2. high'
_time_serials_low_key = '3. low'
_time_serials_close_key = '4. close'
_time_serials_volume_key = '6. volume'
_time_serials_dividend_key = '7. dividend amount'
_time_serials_split_key = '8. split coefficient'

# config for generating data proto
_set_data_proto_earning_timestamp = """
  timelines {
    activities {
      earning_activity {
        activity_timestamp {
          start_timestamp {
            seconds : $INT;
          }
        }
      }
    }
  } """
_set_data_proto_earning_quarterly = """
  timelines {
    activities {
      earning_activity {
        quarterly : $BOOL;
      }
    }
  } """
_set_data_proto_total_revenue = """
  timelines {
    activities {
      earning_activity {
        total_revenue : $FLOAT;
      }
    }
  } """
_set_data_proto_net_income = """
  timelines {
    activities {
      earning_activity {
        net_income : $FLOAT;
      }
    }
  } """
_set_data_proto_gross_profit = """
  timelines {
    activities {
      earning_activity {
        gross_profit : $FLOAT;
      }
    }
  } """
_set_data_proto_num_full_time_employees = """                                                       
  timelines {                                                                                       
    fin_entity {
      traits {
        common_trait {
          num_full_time_employees : $INT;                                                             
        }
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

#  Raw data: time_series_daily_adjusted
_set_data_proto_open = """
  timelines {
    activities {
      daily_stock_activity {
        open : $FLOAT;
      }
    }
  } """
_set_data_proto_high = """
  timelines {
    activities {
      daily_stock_activity {
        high : $FLOAT;
      }
    }
  } """
_set_data_proto_low = """
  timelines {
    activities {
      daily_stock_activity {
        low : $FLOAT;
      }
    }
  } """
_set_data_proto_close = """
  timelines {
    activities {
      daily_stock_activity {
        close : $FLOAT;
      }
    }
  } """
_set_data_proto_volume = """
  timelines {
    activities {
      daily_stock_activity {
        volume : $INT;
      }
    }
  } """
_set_data_proto_date_timestamp = """
  timelines {
    activities {
      daily_stock_activity {
        date_timestamp {
          start_timestamp {
            seconds : $INT;
          }
        }
      }
    }
  } """
_set_data_proto_dividend = """
  timelines {
    activities {
      daily_stock_activity {
        dividend : $FLOAT;
      }
    }
  } """
_set_data_proto_split = """
  timelines {
    activities {
      daily_stock_activity {
        split : $FLOAT;
      }
    }
  } """

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

def _timestampContained(data_proto:data_pb2.Data, timestamp:int):
  return ((data_proto.timelines[0].start_timestamp.seconds <= timestamp) and
          (data_proto.timelines[0].end_timestamp.seconds > timestamp))


class AlphaAdvantageActivityBuilder:
  def __init__(self, parser_config:config_pb2.AlphaAdvantageParserConfig):
    self._parser_config = parser_config

  def populateDataProtos(self, path:str, protos:list):
    input = FileStream(path, encoding='utf-8')                                  
    lexer = JSONLexer(input)                                                                  
    token = CommonTokenStream(lexer)                                                                
    parser = JSONParser(token)                                                                     
    tree = parser.json()                                                                     
    walker = ParseTreeWalker()                                                                      
    walker.walk(self.Listener(protos, self._parser_config), tree)

  class Listener(JSONListener):                                                         
    def __init__(self, data_protos: list, parser_config:config_pb2.AlphaAdvantageParserConfig):                                                        
      self._data_protos = data_protos
      self._generator = data_proto_generator.DataProtoGenerator()
      self._keys = []
      self._parser_config = parser_config
      self._current_time_serial_timestamp = None
      self._current_earning_timestamp = None
                                                                                                    
    def enterPair(self, ctx:JSONParser.PairContext):                                               
      key = ctx.STRING().getText()[1:-1]
      value = ctx.value().getText()[1:-1]
      self._keys.append(key)
      if value == 'None':
        return

      # Raw data: income_statement, cash_flow and balance_sheet.
      if key == 'fiscalDateEnding':
        self._current_earning_timestamp = _isoformatTimestamp(value)
        assert self._current_earning_timestamp > _isoformatTimestamp('1980-01-01')
        self.setFundamentals(_set_data_proto_earning_timestamp,
                             self._current_earning_timestamp,
                             new_repeats={'activities': None})
        if self.isQuarterlyReports():
          self.setFundamentals(_set_data_proto_earning_quarterly, True)
        else:
          self.setFundamentals(_set_data_proto_earning_quarterly, False)
        return

      if key == 'totalRevenue':
        assert self._current_earning_timestamp
        self.setFundamentals(_set_data_proto_total_revenue, float(value))
        return
      if key == 'netIncome':
        assert self._current_earning_timestamp
        self.setFundamentals(_set_data_proto_net_income, float(value))
        return
      if key == 'grossProfit':
        assert self._current_earning_timestamp
        self.setFundamentals(_set_data_proto_gross_profit, float(value))
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

      # Raw data: time_series_daily_adjusted
      if re.match(r'^\d{4}-\d{2}-\d{2}$', key):
        self._current_time_serial_timestamp = _isoformatTimestamp(key)
        return
      self.parseTimeSerials(key, value)

    def parseTimeSerials(self, key:str, value:str):
      if key == _time_serials_open_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(
            _set_data_proto_open, float(value), new_repeats={'activities': None})
        self.setTimeSerials(
            _set_data_proto_date_timestamp, self._current_time_serial_timestamp)
      elif key == _time_serials_high_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(_set_data_proto_high, float(value))
      elif key == _time_serials_low_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(_set_data_proto_low, float(value))
      elif key == _time_serials_close_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(_set_data_proto_close, float(value))
      elif key == _time_serials_volume_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(_set_data_proto_volume, int(value))
      elif key == _time_serials_dividend_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(_set_data_proto_dividend, float(value))
      elif key == _time_serials_split_key:
        assert self._current_time_serial_timestamp
        self.setTimeSerials(_set_data_proto_split, float(value))

    def setFundamentals(self, config:str, value, new_repeats:dict = None):
      for data_proto in self._data_protos:
        if self._current_earning_timestamp == _getLastQuarterEarningTimestamp(data_proto):
          self.setFundamental(data_proto, config, value, new_repeats)

    def setFundamental(self, data_proto, config:str, value, new_repeats:dict = None):
      value_key = 'STRING'
      if isinstance(value, int):
        value_key = 'INT'
      elif isinstance(value, float):
        value_key = 'FLOAT'
      elif isinstance(value, bool):
        value_key = 'BOOL'
      self._generator.generateDataProto(config=config,
                                        output_proto=data_proto,
                                        new_repeats=new_repeats,
                                        var_values={value_key:value})

    def setTimeSerials(self, config:str, value, new_repeats:dict = None):
      for data_proto in self._data_protos:
        if _timestampContained(data_proto, self._current_time_serial_timestamp):
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

