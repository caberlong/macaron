import sys

import tensorflow as tf

from model.model_input import ModelInput
from model.linear_model import LinearModel


def main(argv):                                                                                     
  root_dir = '../data/store/alpha_advantage/example'
  model_input = ModelInput(root_dir)

  for features, label in model_input.dataset.take(1):
    print('one data: %s' % features['historical_prices'])
    print('one data label: %s' % label)

  linear_model = LinearModel(model_input).model()
  linear_model.fit(model_input.dataset, batch_size=16, epochs=10)
  for features, label in model_input.dataset.take(10):
    print('label vs predict: %f <=> %s' % (label.numpy(), linear_model(features).numpy()))
                                                                                                    
if __name__ == '__main__':                                                                          
  main(sys.argv)
