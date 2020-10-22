import sys
import datetime
import tqdm

from proto.source import alpha_advantage_parser_config_pb2 as config_pb2
from data.source.alpha_advantage import alpha_advantage_parser
from data.source.alpha_advantage import alpha_advantage_downloader_run as downloader
from google.protobuf import timestamp_pb2
from multiprocessing import Pool 

_root_dir = '../../store/alpha_advantage'
_raw_data_dir = '/'.join([_root_dir, 'raw/overview'])
_output_dir = '/'.join([_root_dir, 'proto'])


def getConfig(symbol:str):
  config = config_pb2.AlphaAdvantageParserConfig()
  config.raw_data_dir = _raw_data_dir
  config.output_dir = _output_dir
  config.earliest_timestamp.FromDatetime(datetime.datetime(2016, 1, 1))
  config.latest_timestamp.FromDatetime(datetime.datetime(2020, 9, 2))
  config.max_historical_price_count = 28
  config.symbols.append(symbol)
  return config

def parseOne(symbol:str):
  parser = alpha_advantage_parser.AlphaAdvantageParser()
  parser.parse(getConfig(symbol))

def main(argv):
  symbols = []
  symbols.extend(downloader.high_tech_symbols)
  symbols.extend(downloader.finance_symbols)
  symbols.extend(downloader.bio_symbols)

  with Pool(4) as p:
    r = list(tqdm.tqdm(p.imap(parseOne, symbols), total=len(symbols)))


if __name__ == '__main__':
	main(sys.argv)
