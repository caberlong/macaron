import sys
from macaron.data.utils.data_proto_generator import DataProtoGenerator
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
    }
    timelines { 
      fin_entity {
        traits { 
          common_trait.sector : "software2";
        }
      }
    }''', data_proto, new_repeats = ['timelines'])

  data_proto2 = data_pb2.Data()
  generator2 = DataProtoGenerator()
  generator2.generateDataProto(
    'timelines { fin_entity { traits { ' + 
    'common_trait.sector : $INPUT.timelines.fin_entity.traits.common_trait.sector ; } } }',
     data_proto2,
    var_values = {'INPUT': data_proto},
    new_repeats = ['traits'])
  print('data_proto: %s' % data_proto)
  print('data_proto2: %s' % data_proto2)


if __name__ == '__main__':
	main(sys.argv)
