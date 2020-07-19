import sys
import os
import tqdm

from multiprocessing import Pool
from data.source.html import yahoo_quote_parser
from proto.source import yahoo_quote_parser_config_pb2 as config_pb2
from proto import data_pb2

PAGE_TYPES = set(['SUMMARY_PAGE', 'HISTORY_PAGE'])

def parseOne(one_tick:tuple):
  (dir_proto, date, tick, paths) = one_tick
  parser = yahoo_quote_parser.YahooQuoteParser()
  data = data_pb2.Data()
  config = config_pb2.YahooQuoteParserConfig()
  for path in paths:
    config.local_file_path = path
    parser.parse(config, data)
  parent_dir = '/'.join([dir_proto, date])
  os.makedirs(parent_dir, exist_ok=True)
  file_name = '.'.join([tick, 'proto'])
  path = '/'.join([parent_dir, file_name])
  try:
    f = open(path, "wb")
    f.write(data.SerializeToString())
    f.close()
  except e:
    print(e)

def getRawHtmlsInOneDate(dir_raw:str, dir_proto:str, date:str, raws:list):
  htmls = [(f.name, f.path) for f in os.scandir('/'.join([dir_raw, date])) if f.is_file]
  ticks = {}
  for (name, path) in htmls:
    segs = name.split('.')
    if len(segs) != 3 or segs[2] != 'html':
      continue
    if not segs[1] in PAGE_TYPES:
      continue;
    tick = segs[0]
    if not tick in ticks:
      ticks[tick] = []
    ticks[tick].append(path)
  for (tick, paths) in ticks.items():
    raws.append((dir_proto, date, tick, ticks[tick]))

def getRawHtmlsToParse(dir_raw:str, dir_proto:str):
  """Returns all raw htmls need to be parsed."""
  raws = []
  raw_dates = [f.name for f in os.scandir(dir_raw) if f.is_dir()]
  proto_dates = set([f.name for f in os.scandir(dir_proto) if f.is_dir()])
  for date in raw_dates:
    if date in proto_dates:
      continue
    print('Parsing raw html for %s' % date)
    getRawHtmlsInOneDate(dir_raw, dir_proto, date, raws)
  return raws

def main(argv):
  dir_raw = argv[1]
  dir_proto = argv[2]
  assert dir_raw and dir_proto

  raws = getRawHtmlsToParse(dir_raw, dir_proto)
  if len(argv) == 4 and argv[3] == 'dry_run':
    for raw in raws:
      (dir_proto, date, tick, paths) = raw
      print('%s:%s' % (date, tick))
      for path in paths:
        print('\t%s' % path)
    return

  num_process = 4
  with Pool(num_process) as p:
    r = list(tqdm.tqdm(p.imap(parseOne, raws), total=len(raws)))

if __name__ == '__main__':
	main(sys.argv)
