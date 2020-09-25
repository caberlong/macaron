import os
import sys
import datetime

from proto.source import alpha_advantage_parser_config_pb2 as config_pb2
from proto import data_pb2
from data.utils import data_proto_generator
from data.source.alpha_advantage import alpha_advantage_activity_builder as aa_activity_builder


# default maximum historical price count in each trading activity. 
_earliest_timestamp = datetime.datetime(2000, 1, 1).timestamp()
_latest_timestamp = datetime.datetime.now().timestamp()

# config for generating data proto
_set_data_proto_symbol = 'timelines { activities { trading_activity { symbol : $STRING; } } }'
_set_data_proto_timeline_start = """
  timelines {
    start_timestamp {
      seconds : $INT;  
    }
  } """
_set_data_proto_timeline_end = """
  timelines {
    end_timestamp {
      seconds : $INT;  
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

def _getDataProtoOutputPath(
    parser_config:config_pb2.AlphaAdvantageParserConfig, timestamp:int, symbol:str):
  top_dir = "unknown"
  dt = datetime.datetime.fromtimestamp(timestamp)
  if parser_config.interval == config_pb2.AlphaAdvantageParserConfig.INTERVAL_YEAR:
    top_dir = "yearly"
    dt_dir = dt.strftime("%Y")
  elif parser_config.interval == config_pb2.AlphaAdvantageParserConfig.INTERVAL_MONTH:
    top_dir = "monthly"
    dt_dir = dt.strftime("%Y-%m")
  elif parser_config.interval == config_pb2.AlphaAdvantageParserConfig.INTERVAL_DAY:
    top_dir = "daily"
    dt_dir = dt.strftime("%Y-%m-%d")
  return '/'.join([parser_config.output_dir, top_dir, dt_dir, '.'.join([symbol, 'proto'])])

def _getNextTimestamp(timestamp:int, interval:config_pb2.AlphaAdvantageParserConfig.Interval):
  dt = datetime.datetime.fromtimestamp(timestamp)
  if interval == config_pb2.AlphaAdvantageParserConfig.INTERVAL_YEAR:
    return datetime.datetime(dt.year + 1, 1, 1).timestamp() 
  if interval == config_pb2.AlphaAdvantageParserConfig.INTERVAL_MONTH:
    if dt.month == 12:
      return datetime.datetime(dt.year + 1, 1, 1).timestamp()
    else:
      return datetime.datetime(dt.year, dt.month + 1, 1).timestamp()
  if (interval == None) or (interval == config_pb2.AlphaAdvantageParserConfig.INTERVAL_DAY):
    dt = dt + datetime.timedelta(days=1)
    return datetime.datetime(dt.year, dt.month, dt.day).timestamp()

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

class AlphaAdvantageTimelineBuilder:
  def __init__(self):
    self._generator = data_proto_generator.DataProtoGenerator()
    pass

  def parse(self, parser_config:config_pb2.AlphaAdvantageParserConfig):
    assert parser_config.raw_data_dirs
    assert parser_config.output_dir

    symbols = self.getSymbolsInRawDataDir(parser_config.raw_data_dirs)
    timestamps = self.getActivityTimestamps(parser_config)
    for symbol in symbols.keys():
      if parser_config.symbols and not symbol in parser_config.symbols:
        continue
      protos = self.parseOneSymbol(symbol, symbols[symbol], timestamps, parser_config)
      for proto in protos:
        self.outputProto(parser_config, symbol, proto, parser_config.print_only)

  def getSymbolsInRawDataDir(self, raw_data_dirs:list):
    results = {}
    for raw_data_dir in raw_data_dirs:
      for root, dirs, files in os.walk(raw_data_dir): 
        for f in files:
          if not f.endswith('.json'):
             continue
          symbol = os.path.splitext(f)[0]
          results.setdefault(symbol, [])
          results[symbol].append('/'.join([root, f]))
    return results

  def getActivityTimestamps(self, config: config_pb2.AlphaAdvantageParserConfig):
    ''' Generate activity timestamps from the given config. '''
    earliest = _earliest_timestamp
    if config.earliest_timestamp: 
      earliest = config.earliest_timestamp.seconds
    latest = _latest_timestamp
    if config.latest_timestamp: 
      latest = config.latest_timestamp.seconds
      
    results = []
    timestamp = earliest
    while timestamp < latest:
      next_timestamp = _getNextTimestamp(timestamp, config.interval) 
      results.append((timestamp, next_timestamp))
      timestamp = next_timestamp
    return results

  def parseOneSymbol(
      self,
      symbol:str,
      raw_paths:list,
      timestamps:list,
      parser_config:config_pb2.AlphaAdvantageParserConfig): 
    protos = []
    output_dir = parser_config.output_dir
    activity_builder = aa_activity_builder.AlphaAdvantageActivityBuilder(parser_config)
    for (start_timestamp, end_timestamp) in timestamps:
      output_path = _getDataProtoOutputPath(parser_config, start_timestamp, symbol)
      if os.path.isfile(output_path) and os.path.getsize(output_path) > 128:  
        if parser_config.skip_existing:
          continue
        else:
          data_proto = _readDataProto(output_path)
      else:
        data_proto = self.createDataProto(symbol, start_timestamp, end_timestamp)
      protos.append(data_proto)
    if not protos:
      return protos
    for raw_path in raw_paths:
      activity_builder.populateDataProtos(raw_path, protos)
    return protos

  def outputProto(self,
                  parser_config:config_pb2.AlphaAdvantageParserConfig,
                  symbol:str,
                  proto:data_pb2.Data,
                  print_only:bool): 
    output_path = _getDataProtoOutputPath(parser_config,
                                          proto.timelines[0].start_timestamp.seconds,
                                          symbol)
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

  def createDataProto(self, symbol:str, start_timestamp:int, end_timestamp:int):
    data_proto = data_pb2.Data() 
    self._generator.generateDataProto(                                                          
        config=_set_data_proto_common_trait_symbol,
        output_proto=data_proto,
        var_values={'STRING':symbol})
    self._generator.generateDataProto(                                                          
        config=_set_data_proto_timeline_start,
        output_proto=data_proto,
        var_values={'INT':start_timestamp})
    self._generator.generateDataProto(                                                          
        config=_set_data_proto_timeline_end,
        output_proto=data_proto,
        var_values={'INT':end_timestamp})
    return data_proto
