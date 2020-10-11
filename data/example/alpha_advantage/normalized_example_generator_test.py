import sys
import datetime
import matplotlib.pyplot as plt
import numpy as np

from data.example.alpha_advantage.normalized_example_generator import NormalizedExampleGenerator

_length=10
_max_plot=2

def plot(examples):
  cnt = 0
  t = np.arange(0, 10, 1)
  for example in examples:
    cnt = cnt + 1
    if cnt > _max_plot: 
      break
    # s = 'example_' + str(cnt)
    plt.plot(t, example)
  plt.show()

def main(argv):
  root_dir = '/'.join([
    '/Users/longchb/Documents/GitHub/macaron/data/store',
    'alpha_advantage',
    'timeline'
  ])
  generator = NormalizedExampleGenerator(
      root_dir=root_dir,
      symbol='AAPL',
      start_timestamp=datetime.datetime(2020, 9, 5).timestamp(),
      end_timestamp=datetime.datetime(2020, 10, 2).timestamp(),
      length=_length
  )
  # generator.printFedRateMap()
  examples = generator.getSimpleExamples()
  # plot(examples)
  for example in examples:
    print('%s' % example)


if __name__ == '__main__':
	main(sys.argv)
