import sys
from macaron.data.source import generic_data_generator
from macaron.data.utils import data_proto_generator
from data.proto import data_pb2                                                                     


class TestDataGenerator:
  def __init__(self, options):
    pass 

  def populate_data(self, raw_inputs: str, data_proto: data_pb2.Data):
    data_proto_generator.DataProtoGenerator().generateDataProto(raw_inputs, data_proto) 


def main(argv):
  data_source = generic_data_generator.GenericDataGenerator(
      'class_name: "macaron.data.source.generic_data_generator_test.TestDataGenerator"')

  data = data_pb2.Data()
  data_source.populate_data('fin_entity { name: "test_name"; }', data)


if __name__ == '__main__':
  main(sys.argv)
