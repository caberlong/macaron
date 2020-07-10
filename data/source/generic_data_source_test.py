import sys
from macaron.data.source import generic_data_source


def main(argv):
  data_source = generic_data_source.GenericDataSource('class_name: "my_class"')


if __name__ == '__main__':
  main(sys.argv)
