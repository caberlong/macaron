import sys
import os
import time
import requests
import tqdm

from datetime import date
from multiprocessing import Pool
from time import sleep

from proto.source import alpha_advantage_source_config_pb2 as config_pb2

class AlphaAdvantageDownloader:
  def __init__(self, root_dir: str, dry_run: bool=False):
    self._num_processes = 1;
    self._address_prefix = 'https://www.alphavantage.co/query'
    self._root_dir = root_dir
    self._dry_run = dry_run

  def download_one(self, one: tuple):
    (symbol, aa_function, address) = one
    path = '/'.join([
        self._root_dir,
        aa_function.lower(),
        '%s' % date.today(), 
        '.'.join([symbol, 'json'])
    ])
    if os.path.isfile(path) and os.path.getsize(path) > 10000:
      return
    sleep(20)
    r = requests.get(address, allow_redirects=True)
    if self._dry_run:
      print('get %s and write to %s' % (address, path))
      return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
      f = open(path, 'w')
      f.write(r.text)
      f.close()
    except e:
      print(e)

  def getAddress(self, config: config_pb2.AlphaAdvantageSourceConfig):
    params = []
    assert config.api_key
    params.append('='.join(['apikey', config.api_key]))

    assert config.symbol
    params.append('='.join(['symbol', config.symbol]))

    assert config.aa_function
    aa_function = config_pb2.AlphaAdvantageFunction.Name(config.aa_function)
    params.append('='.join(['function', aa_function]))

    if config.output_size:
      params.append('='.join([
          'outputsize', config_pb2.AlphaAdvantageOutputSize.Name(config.output_size).lower()]))

    if config.data_type:
      params.append('='.join([
          'datatype=', config_pb2.AlphaAdvantageDataType.Name(config.data_type).lower()]))
    
    return config.symbol, aa_function, "?".join([self._address_prefix, '&'.join(params)])
    
  def download(self, configs: list):
    addresses = []
    for config in configs:
      addresses.append(self.getAddress(config))
    with Pool(self._num_processes) as p:
      r = list(tqdm.tqdm(p.imap(self.download_one, addresses), total=len(addresses)))
