import sys
import os
import tensorflow as tf

class BaselineModel(tf.keras.Model): 
  def __init__(self):
    super(BaselineModel, self).__init__()

  def call(self, inputs):
    ''' the historical price index * numer_of_feature because historical price is the first one'''
    return inputs['historical_prices'][0][-1][0]
