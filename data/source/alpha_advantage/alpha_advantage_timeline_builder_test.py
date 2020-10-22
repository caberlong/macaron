import sys
import datetime

from proto.source import alpha_advantage_parser_config_pb2 as config_pb2
from data.source.alpha_advantage import alpha_advantage_timeline_builder
from google.protobuf import timestamp_pb2

_root_dir = '../../store/alpha_advantage'
_raw_data_dir = '/'.join([_root_dir, 'raw'])
_output_dir = '/'.join([_root_dir, 'timeline'])

def getConfig():
  config = config_pb2.AlphaAdvantageParserConfig()
  config.raw_data_dirs.append('/'.join([_raw_data_dir, 'balance_sheet']))
  config.raw_data_dirs.append('/'.join([_raw_data_dir, 'income_statement']))
  config.raw_data_dirs.append('/'.join([_raw_data_dir, 'cash_flow']))
  config.output_dir = '/'.join([_output_dir, 'earning'])
  config.earliest_timestamp.FromDatetime(datetime.datetime(2020, 7, 1))
  config.latest_timestamp.FromDatetime(datetime.datetime(2020, 10, 2))
  config.symbols.extend([
    #'AAPL', 'AMAT', 'UBER', 'MU', 'SQ', 'ADSK', 'NOT-IN-DISK'
    'AAPL'
  ])
  config.skip_existing = True
  config.print_only = True
  config.interval = config_pb2.AlphaAdvantageParserConfig.INTERVAL_MONTH
  return config

def main(argv):
  builder = alpha_advantage_timeline_builder.AlphaAdvantageTimelineBuilder()
  builder.parse(getConfig())


if __name__ == '__main__':
	main(sys.argv)
