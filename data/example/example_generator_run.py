import sys
import os
import tqdm
import tensorflow as tf

from multiprocessing import Pool
from data.example.example_generator import ExampleGenerator 
from proto import data_pb2

def convertOne(one_tick:tuple):
  (dir_example, date, tick, path) = one_tick
  data = data_pb2.Data()
  f = open(path, 'rb')
  data.ParseFromString(f.read())
  f.close()

  generator = ExampleGenerator()
  example = generator.generateExample(data)
  parent_dir = '/'.join([dir_example, date])
  os.makedirs(parent_dir, exist_ok=True)
  output_path = '/'.join([parent_dir, '.'.join([tick, 'tfrecords'])])
  with tf.io.TFRecordWriter(output_path) as writer:
    writer.write(example.SerializeToString())

def getProtosInOneDate(dir_proto:str, dir_example:str, date:str, protos:list):
  files = [(f.name, f.path) for f in os.scandir('/'.join([dir_proto, date])) if f.is_file]
  for (name, path) in files:
    segs = name.split('.')
    if not os.stat(path).st_size or segs[1] != 'proto':
      continue
    protos.append((dir_example, date, segs[0], path))

def getProtosToConvert(dir_proto:str, dir_example:str):
  """Returns all protos need to be converted."""
  protos = []
  proto_dates = [f.name for f in os.scandir(dir_proto) if f.is_dir()]
  example_dates = set([f.name for f in os.scandir(dir_example) if f.is_dir()])
  for date in proto_dates:
    if date in example_dates:
      continue
    print('Convert proto to tf train examples for date %s' % date)
    getProtosInOneDate(dir_proto, dir_example, date, protos)
  return protos

def main(argv):
  dir_proto = argv[1]
  dir_example = argv[2]
  assert dir_proto and dir_example

  protos = getProtosToConvert(dir_proto, dir_example)
  if len(argv) == 4 and argv[3] == 'dry_run':
    for proto in protos:
      (dir_example, date, tick, path) = proto
      print('%s:%s' % (date, tick))
      print('\t%s' % path)
    return

  num_process = 4
  with Pool(num_process) as p:
    r = list(tqdm.tqdm(p.imap(convertOne, protos), total=len(protos)))

if __name__ == '__main__':
	main(sys.argv)
