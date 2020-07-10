import sys
from macaron.data.utils.data_proto_generator import DataProtoGenerator
from data.proto import data_pb2


def main(argv):
	data_proto = data_pb2.Data()
	generator = DataProtoGenerator()
	generator.generateDataProto('x = 3.0; field1 { field2: $x; }', data_proto)


if __name__ == '__main__':
	main(sys.argv)
