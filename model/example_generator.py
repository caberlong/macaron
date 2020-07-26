import sys
import tensorflow as tf

from proto import data_pb2
from data.utils.data_proto_generator import DataProtoGenerator

class ExampleGenerator:
  def __init__(self):
    pass

  def generateExample(self, config:str, data:data_pb2.Data, example:tf.train.Example):
    generator = DataProtoGenerator()
    generator.generateDataProto(config, example, var_values = {'DATA': data})
