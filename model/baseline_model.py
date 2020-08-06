import sys
import os
import tensorflow as tf

class BaselineModel(tf.keras.Model): 
  def __init__(self):
    super(BaselineModel, self).__init__()

  def call(self, inputs):
    return inputs['historical_low'][0]
