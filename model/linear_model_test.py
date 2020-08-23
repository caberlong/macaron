import sys

import tensorflow as tf

from model.model_input import ModelInput
from model.linear_model import LinearModel


def main(argv):                                                                                     
  root_dir = '/Users/longchb/Documents/GitHub/macaron/data/store/yahoo_quote/example'
  model_input = ModelInput(root_dir)

  linear_model = LinearModel(model_input).model()
  for features, label in model_input.dataset.take(1):
    print('one data: %s' % features['historical_prices'])
    print('one data label: %s' % label)
  linear_model.fit(model_input.dataset, batch_size=32, epochs=50)
  for features, label in model_input.dataset.take(10):
    print('label vs predict: %f <=> %s' % (label.numpy(), linear_model(features).numpy()))
                                                                                                    
if __name__ == '__main__':                                                                          
  main(sys.argv)
