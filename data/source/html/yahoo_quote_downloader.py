import sys
import os
import time
import requests
import tqdm

from datetime import date
from multiprocessing import Pool

from proto.source import yahoo_quote_parser_config_pb2 as config_pb2

class YahooQuoteDownloader:
  def __init__(self, root_dir: list, dry_run: bool=False):
    self._num_processes = 4;
    self._address_prefix = "https://finance.yahoo.com/quote"
    self._root_dir = '/'.join([root_dir, '%s' % date.today()])
    self._dry_run = dry_run

  def download_one(self, one: tuple):
    (tick, page_type, address) = one
    r = requests.get(address, allow_redirects=True)
    path = '/'.join([self._root_dir, '.'.join([tick, page_type, 'html'])])
    if self._dry_run:
      print('get %s and write to %s' % (address, path))
      return
    os.makedirs(self._root_dir, exist_ok=True)
    try:
      f = open(path, 'w')
      f.write(r.text)
      f.close()
    except e:
      print(e)

  def getAddresses(self, configs: list):
    addresses = []
    for config in configs:
      assert config.tick
      for page in config.page_types:
        addresses.append((
            config.tick,
            config_pb2.YahooQuoteParserConfig.PageType.Name(page),
            self.getAddress(config.tick, page)))
    return addresses

  def getAddress(self, tick: str, page: config_pb2.YahooQuoteParserConfig.PageType):
    if page == config_pb2.YahooQuoteParserConfig.SUMMARY_PAGE:
      type_segment = ""
    elif page == config_pb2.YahooQuoteParserConfig.HISTORY_PAGE:
      type_segment = "history"
    elif page == config_pb2.YahooQuoteParserConfig.STATISTICS_PAGE:
      type_segment = "key-statistics"
    elif page == config_pb2.YahooQuoteParserConfig.PROFILE_PAGE:
      type_segment = "profile"
    elif page == config_pb2.YahooQuoteParserConfig.ANALYSIS_PAGE:
      type_segment = "analysis"
    else:
      raise
    return "/".join([self._address_prefix, tick, type_segment])
    
  def download(self, configs: list):
    addrs = self.getAddresses(configs)
    with Pool(self._num_processes) as p:
      r = list(tqdm.tqdm(p.imap(self.download_one, addrs), total=len(addrs)))
