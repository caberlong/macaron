import sys

from data.proto.source import yahoo_quote_parser_config_pb2 as config_pb2
from data.proto import data_pb2
from macaron.data.source.html import yahoo_quote_downloader

def getConfigs(ticks: list):
  configs = []
  pages = [
    config_pb2.YahooQuoteParserConfig.SUMMARY_PAGE,
    config_pb2.YahooQuoteParserConfig.HISTORY_PAGE,
    config_pb2.YahooQuoteParserConfig.PROFILE_PAGE,
  ]
  for tick in ticks:
    config = config_pb2.YahooQuoteParserConfig()
    config.tick = tick
    config.page_types.extend(pages)
    configs.append(config)
  return configs


def main(argv):
  downloader = yahoo_quote_downloader.YahooQuoteDownloader('/tmp/macaron')
  downloader.download(getConfigs([
      'MSFT', 'GOOG', 'AMZN', 'TSLA', 'GDX', 'GLD'
  ]))


if __name__ == '__main__':
	main(sys.argv)
