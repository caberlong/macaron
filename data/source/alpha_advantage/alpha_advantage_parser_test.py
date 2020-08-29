import sys
import datetime

from proto.source import alpha_advantage_parser_config_pb2 as config_pb2
from data.source.alpha_advantage import alpha_advantage_parser
from google.protobuf import timestamp_pb2

def getConfig():
  config = config_pb2.AlphaAdvantageParserConfig()
  config.raw_data_dir = '/Users/longchb/Documents/GitHub/macaron/data/store/alpha_advantage/raw'
  config.output_dir = '/Users/longchb/Documents/GitHub/macaron/data/store/alpha_advantage/proto'
  config.earliest_timestamp.FromDatetime(datetime.datetime(2020, 1, 1))
  config.latest_timestamp.FromDatetime(datetime.datetime(2020, 3, 3))
  config.max_historical_price_count = 10
  config.symbols.extend([
    'AAPL', 'AMAT', 'UBER', 'MU', 'SQ', 'ADSK', 'NOT-IN-DISK'
  ])
  return config

def main(argv):
  parser = alpha_advantage_parser.AlphaAdvantageParser()
  parser.parse(getConfig())


if __name__ == '__main__':
	main(sys.argv)
