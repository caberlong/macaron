import sys

from proto.source import alpha_advantage_source_config_pb2 as config_pb2
from proto import data_pb2
from data.source.alpha_advantage import alpha_advantage_downloader

_api_key = 'API_KEY'

def getConfigs(symbols: list):
  configs = []
  for symbol in symbols:
    config = config_pb2.AlphaAdvantageSourceConfig()
    config.symbol = symbol
    config.aa_function = config_pb2.AlphaAdvantageFunction.TIME_SERIES_DAILY
    config.output_size = config_pb2.AlphaAdvantageOutputSize.FULL
    config.api_key = _api_key
    configs.append(config)
  return configs


def main(argv):
  downloader = alpha_advantage_downloader.AlphaAdvantageDownloader(
      '/tmp/macaron/alpha_advantage', dry_run=True)
  downloader.download(getConfigs([
      'MSFT', 'GOOG', 'AMZN',
  ]))


if __name__ == '__main__':
	main(sys.argv)
