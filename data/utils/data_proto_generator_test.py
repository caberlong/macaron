import sys
from macaron.data.utils.data_proto_generator import DataProtoGenerator


def main(argv):
	generator = DataProtoGenerator()
	print('generated proto %s' % generator.generateDataProto('x = 3.0; field1 { field2: $x; }'))


if __name__ == '__main__':
	main(sys.argv)
