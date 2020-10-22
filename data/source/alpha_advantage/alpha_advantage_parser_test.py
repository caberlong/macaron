import sys
import datetime

from proto.source import alpha_advantage_parser_config_pb2 as config_pb2
from data.source.alpha_advantage import alpha_advantage_parser
from google.protobuf import timestamp_pb2

_root_dir = '../../store/alpha_advantage'
_raw_data_dir = '/'.join([_root_dir, 'raw/income_statement'])
_output_dir = '/'.join([_root_dir, 'proto'])

def getConfig():
  config = config_pb2.AlphaAdvantageParserConfig()
  config.raw_data_dir = _raw_data_dir
  config.output_dir = _output_dir
  config.earliest_timestamp.FromDatetime(datetime.datetime(2020, 1, 1))
  config.latest_timestamp.FromDatetime(datetime.datetime(2020, 4, 1))
  config.max_historical_price_count = 10
  config.symbols.extend([
    #'AAPL', 'AMAT', 'UBER', 'MU', 'SQ', 'ADSK', 'NOT-IN-DISK'
    'SQ'
  ])
  config.skip_existing = False
  config.print_only = True
  return config

def main(argv):
  parser = alpha_advantage_parser.AlphaAdvantageParser()
  parser.parse(getConfig())


if __name__ == '__main__':
	main(sys.argv)
