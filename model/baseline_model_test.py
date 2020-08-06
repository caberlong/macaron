import sys

import tensorflow as tf

from model.model_input import ModelInput
from model.baseline_model import BaselineModel


def main(argv):                                                                                     
  root_dir = '/Users/longchb/Documents/GitHub/macaron/data/store/yahoo_quote/example'
  model_input = ModelInput(root_dir)
  train = model_input.dataset

  baseline_model = BaselineModel()
  optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
  baseline_model.compile(optimizer, loss=tf.keras.losses.MeanSquaredError())
  baseline_model.fit(train, epochs=10, batch_size=32)
                                                                                                    
if __name__ == '__main__':                                                                          
  main(sys.argv)
