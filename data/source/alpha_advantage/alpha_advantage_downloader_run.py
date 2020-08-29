import sys

from proto.source import alpha_advantage_source_config_pb2 as config_pb2
from data.source.alpha_advantage import alpha_advantage_downloader

_api_key = 'VFDAX0Q6EFSOXLUV'

_high_tech_symbols = [
  'AAPL', 'MSFT', 'TSM', 'INTC', 'NVDA', 'ADBE', 'CSCO', 'SAP', 'ORCL', 'CRM',
  'ASML', 'ACN', 'AVGO', 'TXN', 'IBM', 'SHOP', 'QCOM', 'SNE', 'FIS', 'NOW',
  'INTU', 'FISV', 'AMD', 'VMW', 'AMAT', 'UBER', 'MU', 'SQ', 'ADSK', 'LRCX',
  'INFY', 'DELL', 'ADI', 'WDAY', 'TEAM', 'DOCU', 'NXPI', 'CTSH', 'ERIC', 'SPLK',
  'KLAC', 'APH', 'SNPS', 'TEL', 'CDNS', 'MCHP', 'STM', 'DDOG', 'HPQ', 'ANSS',
]
_finance_symbols = [
  'V', 'JPM', 'MA', 'BAC', 'PYPL', 'C', 'LFC', 'WFC', 'RY', 'HSBC', 'MS',
  'BLK', 'TD', 'SPGI',
]
_bio_symbols = [
  'JNJ', 'UNH', 'NVS', 'MRK', 'PFE', 'ABBV', 'ABT', 'LLY', 'TMO', 'NVO',
  'AZN', 'AMGN', 'BMY', 'DHR', 'SNY', 'MDT', 'DHR-PA', 'GSK', 'GILD', 'CVS',
  'BDX', 'VRTX', 'ISRG', 'SYK', 'ZTS', 'ANTM', 'CI', 'REGN', 'ILMN', 'TAK',
  'HUM', 'BSX', 'EW', 'BIIB', 'PHG', 'BAX', 'DXCM', 'CNC', 'VEEV', 'HCA',
  'WBA', 'SGEN', 'MRNA', 'ALC', 'IDXX', 'A', 'IQV', 'RMD', 'ZBH', 'RPRX',
]

def getConfigs(aa_function: config_pb2.AlphaAdvantageFunction):
  configs = []
  symbols = []
  symbols.extend(_high_tech_symbols)
  symbols.extend(_finance_symbols)
  symbols.extend(_bio_symbols)
  for symbol in symbols:
    config = config_pb2.AlphaAdvantageSourceConfig()
    config.symbol = symbol
    config.aa_function = aa_function
    config.output_size = config_pb2.AlphaAdvantageOutputSize.FULL
    config.api_key = _api_key
    configs.append(config)
  return configs


def main(argv):
  assert argv[1]
  if argv[2] == 'dry_run':
    dry_run = True
  else:
    dry_run = False
  aa_functions = [
    config_pb2.AlphaAdvantageFunction.TIME_SERIES_DAILY,
    config_pb2.AlphaAdvantageFunction.INCOME_STATEMENT,
    config_pb2.AlphaAdvantageFunction.BALANCE_SHEET,
    config_pb2.AlphaAdvantageFunction.CASH_FLOW
  ]
  configs = []
  for aa_function in aa_functions:
    configs.extend(getConfigs(aa_function))
  alpha_advantage_downloader.AlphaAdvantageDownloader(argv[1], dry_run=dry_run).download(configs)


if __name__ == '__main__':
	main(sys.argv)
