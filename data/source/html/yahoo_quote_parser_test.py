import sys

from google.protobuf import text_format

from data.proto.source import yahoo_quote_parser_config_pb2
from data.proto import data_pb2
from macaron.data.source.html import yahoo_quote_parser


def main(argv):
  config = yahoo_quote_parser_config_pb2.YahooQuoteParserConfig()
  parser = yahoo_quote_parser.YahooQuoteParser()
  fin_entity = data_pb2.Data()
  activity = data_pb2.Data()

  text_format.Parse('local_file_path: "%s"' % argv[1], config)
  parser.parse(config, fin_entity, activity)

  config.local_file_path = argv[2]
  parser.parse(config, fin_entity, activity)

  print('Config: %s' % config)
  print('Output data: fin_entity:\n%s\nactivty:\n' % fin_entity, activity)


if __name__ == '__main__':
	main(sys.argv)
