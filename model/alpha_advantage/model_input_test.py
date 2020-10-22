import sys                                                                                          
import tensorflow as tf                                                                             
import matplotlib as mpl
import matplotlib.pyplot as plt

from model.alpha_advantage.model_input import ModelInput

mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False

def main(argv):                                                                                     
  root_dir = '/'.join([
      '../../data/store',
      'alpha_advantage',
      'normalized_price_simple_example'
  ])
  dataset = ModelInput(root_dir).dataset
  record = 0
  for features, label in dataset.take(10):
    record = record + 1
    print('\n\nprint %d parsed record ' % record)
    print(repr(features))
    print(repr(label))
    print('last price: %f' % features['historical_prices'][0][0][-1]) 
    if record == 5:
      plt.plot(range(28), features['historical_prices'].numpy())
      plt.legend(['historical_prices'])
      plt.show()

                                                                                                    
if __name__ == '__main__':                                                                          
  main(sys.argv)
