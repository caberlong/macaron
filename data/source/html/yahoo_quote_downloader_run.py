import sys

from proto.source import yahoo_quote_parser_config_pb2 as config_pb2
from proto import data_pb2
from data.source.html import yahoo_quote_downloader

_high_tech_ticks = [
  'AAPL', 'MSFT', 'TSM', 'INTC', 'NVDA', 'ADBE', 'CSCO', 'SAP', 'ORCL', 'CRM',
  'ASML', 'ACN', 'AVGO', 'TXN', 'IBM', 'SHOP', 'QCOM', 'SNE', 'FIS', 'NOW',
  'INTU', 'FISV', 'AMD', 'VMW', 'AMAT', 'UBER', 'MU', 'SQ', 'ADSK', 'LRCX',
  'INFY', 'DELL', 'ADI', 'WDAY', 'TEAM', 'DOCU', 'NXPI', 'CTSH', 'ERIC', 'SPLK',
  'KLAC', 'APH', 'SNPS', 'TEL', 'CDNS', 'MCHP', 'STM', 'DDOG', 'HPQ', 'ANSS',
]
_page_types = [
  config_pb2.YahooQuoteParserConfig.SUMMARY_PAGE,
  config_pb2.YahooQuoteParserConfig.HISTORY_PAGE,
  config_pb2.YahooQuoteParserConfig.PROFILE_PAGE,
  config_pb2.YahooQuoteParserConfig.ANALYSIS_PAGE,
  config_pb2.YahooQuoteParserConfig.STATISTICS_PAGE,
]

def getConfigs():
  configs = []
  ticks = []
  ticks.extend(_high_tech_ticks)
  for tick in ticks:
    config = config_pb2.YahooQuoteParserConfig()
    config.tick = tick
    config.page_types.extend(_page_types)
    configs.append(config)
  return configs


def main(argv):
  assert argv[1]
  if argv[2] == 'dry_run':
    dry_run = True
  else:
    dry_run = False
  yahoo_quote_downloader.YahooQuoteDownloader(argv[1], dry_run=dry_run).download(getConfigs())


if __name__ == '__main__':
	main(sys.argv)
