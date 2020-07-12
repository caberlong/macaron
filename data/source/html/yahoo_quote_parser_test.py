import sys

from google.protobuf import text_format

from data.proto.source import yahoo_quote_parser_config_pb2
from data.proto import data_pb2
from macaron.data.source.html import yahoo_quote_parser


def main(argv):
  config = yahoo_quote_parser_config_pb2.YahooQuoteParserConfig()
  text_format.Parse('local_file_path: "%s"' % argv[1], config)
  parser = yahoo_quote_parser.YahooQuoteParser()
  data = data_pb2.Data()
  parser.parse(config, data)
  print('Config: %s' % config)
  print('Output data: %s' % data)


if __name__ == '__main__':
	main(sys.argv)
