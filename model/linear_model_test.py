import sys

import tensorflow as tf

from model.model_input import ModelInput
from model.linear_model import LinearModel


def main(argv):                                                                                     
  root_dir = '/Users/longchb/Documents/GitHub/macaron/data/store/yahoo_quote/example'
  model_input = ModelInput(root_dir)
  train = model_input.dataset

  linear_model = LinearModel(model_input.featureLayer)
  optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
  linear_model.compile(optimizer, loss=tf.keras.losses.MeanSquaredError())
  linear_model.fit(train, epochs=50, batch_size=32)
                                                                                                    
if __name__ == '__main__':                                                                          
  main(sys.argv)
