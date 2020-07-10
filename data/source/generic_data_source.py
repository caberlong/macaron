import sys

from google.protobuf import text_format
from data.proto import data_pb2
from data.proto import data_source_config_pb2


class GenericDataSource:
  def __init__(self, config: str):
    data = data_pb2.Data()
    text_format.Parse(' fin_entity { id : 12345 }', data)
    print('data: %s' % data)
    
    self._config = data_source_config_pb2.DataSourceConfig()
    text_format.Parse(config, self._config)
    print('config %s' % self._config)
