import sys
import tensorflow as tf

from data.example.example_generator import ExampleGenerator
from proto import data_pb2


def main(argv):
  data = data_pb2.Data()
  f = open(argv[1], "rb")
  data.ParseFromString(f.read())
  f.close()

  example = ExampleGenerator().generateExample(data)
  print('Example output: %s ' % example)


if __name__ == '__main__':
	main(sys.argv)
