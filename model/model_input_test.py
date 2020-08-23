import sys                                                                                          
import tensorflow as tf                                                                             
import matplotlib as mpl
import matplotlib.pyplot as plt

from model.model_input import ModelInput

mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False

def main(argv):                                                                                     
  root_dir = '/Users/longchb/Documents/GitHub/macaron/data/store/yahoo_quote/example'
  dataset = ModelInput(root_dir).dataset
  record = 0
  for features, label in dataset.take(10):
    record = record + 1
    print('\n\nprint %d parsed record ' % record)
    print(repr(features))
    if record == 5:
      plt.plot(range(10), features['historical_high'].numpy())
      plt.plot(range(10), features['historical_low'].numpy())
      plt.plot(range(10), features['historical_close'].numpy())
      plt.legend(['high', 'low', 'close'])
      plt.show()

                                                                                                    
if __name__ == '__main__':                                                                          
  main(sys.argv)
