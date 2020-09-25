import sys
import datetime
import tqdm
import os
import tensorflow as tf

from data.source.alpha_advantage import alpha_advantage_downloader_run as downloader
from data.example.alpha_advantage.normalized_example_generator import NormalizedExampleGenerator
from multiprocessing import Pool 

_root_dir = '/Users/longchb/Documents/GitHub/macaron/data/store/alpha_advantage'
_timeline_data_dir = '/'.join([_root_dir, 'timeline'])
_output_dir = '/'.join([_root_dir, 'normalized_price_simple_example'])

_start_timestamp = datetime.datetime(2010, 1, 1).timestamp()
_end_timestamp = datetime.datetime(2020, 9, 6).timestamp()
_length = 28

def generateOneSymbol(symbol:str):
  parent_dir = _output_dir
  os.makedirs(parent_dir, exist_ok=True)
  output_path = '/'.join([parent_dir, '.'.join([symbol, 'tfrecords'])])
  if os.path.isfile(output_path) and os.path.getsize(output_path) > 128:
    return

  examples = NormalizedExampleGenerator(
      root_dir=_timeline_data_dir,
      symbol=symbol,
      start_timestamp=_start_timestamp,
      end_timestamp=_end_timestamp,
      length=_length
  ).getSimpleExamples()

  with tf.io.TFRecordWriter(output_path) as writer:
    for example in examples:
      writer.write(example.SerializeToString())

def main(argv):
  symbols = []
  symbols.extend(downloader.high_tech_symbols)
  symbols.extend(downloader.finance_symbols)
  symbols.extend(downloader.bio_symbols)
  symbols.extend(downloader.etfs)

  with Pool(4) as p:
    r = list(tqdm.tqdm(p.imap(generateOneSymbol, symbols), total=len(symbols)))


if __name__ == '__main__':
	main(sys.argv)
