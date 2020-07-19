import sys

from google.protobuf import text_format

from proto.source import yahoo_quote_parser_config_pb2
from proto import data_pb2
from data.source.html import yahoo_quote_parser


def main(argv):
  config = yahoo_quote_parser_config_pb2.YahooQuoteParserConfig()
  parser = yahoo_quote_parser.YahooQuoteParser()
  data = data_pb2.Data()

  text_format.Parse('local_file_path: "%s"' % argv[1], config)
  parser.parse(config, data)

  config.local_file_path = argv[2]
  parser.parse(config, data)

  print('Config: %s' % config)
  print('Output data: \n%s\nactivty:\n' % data)


if __name__ == '__main__':
	main(sys.argv)
