import sys
import tensorflow as tf

from data.utils.data_proto_generator import DataProtoGenerator
from model.example_generator import ExampleGenerator
from proto import data_pb2


def main(argv):
  data_proto = data_pb2.Data()
  generator = DataProtoGenerator()
  generator.generateDataProto('''
    timelines { 
      fin_entity {
        traits { 
          common_trait.sector : "software";
        }
      }
    }''', data_proto)

  example = tf.train.Example()
  generator = ExampleGenerator()
  generator.generateExample('''
    features {
      feature {
        key: "sector";
        value {
          bytes_list {
            value: $DATA.timelines.fin_entity.traits.common_trait.sector;
          }
        }
      }
    }''', data_proto, example)

  print('example: %s' % example)


if __name__ == '__main__':
	main(sys.argv)
