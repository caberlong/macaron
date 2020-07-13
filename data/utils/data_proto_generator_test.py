import sys
from macaron.data.utils.data_proto_generator import DataProtoGenerator
from data.proto import data_pb2


def main(argv):
  data_proto = data_pb2.Data()
  generator = DataProtoGenerator()
  generator.generateDataProto(
      'fin_entity { traits { common_trait { sector : "software"; } } }', data_proto)
  print('data_proto: %s' % data_proto)


if __name__ == '__main__':
	main(sys.argv)
