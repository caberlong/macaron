import sys

import tensorflow as tf

from model.alpha_advantage.model_input import ModelInput
from model.alpha_advantage.baseline_model import BaselineModel


def main(argv):                                                                                     
  root_dir = '/'.join([
      '../../data/store',
      'alpha_advantage',
      'normalized_price_simple_example'
  ])
  model_input = ModelInput(root_dir)

  baseline_model = BaselineModel()
  optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
  baseline_model.compile(optimizer, loss=tf.keras.losses.MeanSquaredError())
  baseline_model.fit(model_input.dataset_train,
                     epochs=1,
                     batch_size=32,
                     validation_data=model_input.dataset_test)
                                                                                                    
if __name__ == '__main__':                                                                          
  main(sys.argv)
