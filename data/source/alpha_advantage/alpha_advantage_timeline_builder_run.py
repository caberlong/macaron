import sys
import datetime
import tqdm

from proto.source import alpha_advantage_parser_config_pb2 as config_pb2
from data.source.alpha_advantage import alpha_advantage_timeline_builder
from data.source.alpha_advantage import alpha_advantage_downloader_run as downloader
from google.protobuf import timestamp_pb2
from multiprocessing import Pool 

_root_dir = '/Users/longchb/Documents/GitHub/macaron/data/store/alpha_advantage'
_raw_data_dir = '/'.join([_root_dir, 'raw'])
_output_dir = '/'.join([_root_dir, 'timeline'])


def getEarningConfig(symbol:str):
  config = config_pb2.AlphaAdvantageParserConfig()
  config.raw_data_dirs.append('/'.join([_raw_data_dir, 'balance_sheet', '2020-09-06']))
  config.raw_data_dirs.append('/'.join([_raw_data_dir, 'income_statement', '2020-09-06']))
  config.raw_data_dirs.append('/'.join([_raw_data_dir, 'cash_flow', '2020-09-06']))
  config.output_dir = '/'.join([_output_dir, 'earning'])
  config.earliest_timestamp.FromDatetime(datetime.datetime(2000, 1, 1))
  config.latest_timestamp.FromDatetime(datetime.datetime(2020, 9, 2))
  config.symbols.append(symbol)
  config.interval = config_pb2.AlphaAdvantageParserConfig.INTERVAL_MONTH 
  return config

def getTimeSeriesConfig(symbol:str):
  config = config_pb2.AlphaAdvantageParserConfig()
  config.raw_data_dirs.append('/'.join([_raw_data_dir, 'time_series_daily_adjusted', '2020-09-06']))
  config.output_dir = '/'.join([_output_dir, 'time_series'])
  config.earliest_timestamp.FromDatetime(datetime.datetime(2000, 1, 1))
  config.latest_timestamp.FromDatetime(datetime.datetime(2020, 9, 2))
  config.symbols.append(symbol)
  config.interval = config_pb2.AlphaAdvantageParserConfig.INTERVAL_MONTH 
  return config

def parseOne(symbol:str):
  parser = alpha_advantage_timeline_builder.AlphaAdvantageTimelineBuilder()
  parser.parse(getEarningConfig(symbol))
  parser.parse(getTimeSeriesConfig(symbol))

def main(argv):
  symbols = []
  symbols.extend(downloader.high_tech_symbols)
  symbols.extend(downloader.finance_symbols)
  symbols.extend(downloader.bio_symbols)
  symbols.extend(downloader.etfs)

  with Pool(4) as p:
    r = list(tqdm.tqdm(p.imap(parseOne, symbols), total=len(symbols)))


if __name__ == '__main__':
	main(sys.argv)
