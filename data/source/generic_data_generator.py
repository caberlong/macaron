import sys
import importlib

from google.protobuf import text_format
from proto import data_pb2
from proto import data_source_config_pb2


class GenericDataGenerator:
  def __init__(self, config: str):
    """Config is a text format of DataSourceConfig proto.""" 
    self._config = data_source_config_pb2.DataSourceConfig()
    text_format.Parse(config, self._config)
    self._generator = self._create_generator()

  def _create_generator(self):
    """Returns generator class.""" 
    [module_name, class_name] = self._config.class_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    generator_class = getattr(module, class_name)
    return generator_class(self._config.class_options)

  def populate_data(self, raw_inputs: str, data_proto: data_pb2.Data):
    return self._generator.populate_data(raw_inputs, data_proto)
