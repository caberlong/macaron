import sys
import os
import tensorflow as tf

class LinearModel(tf.keras.Model): 
  def __init__(self, feature_layer):
    super(LinearModel, self).__init__()
    self._feature_layer = feature_layer
    self._dense = tf.keras.layers.Dense(1)

  def call(self, inputs):
    features = self._feature_layer(inputs)
    return self._dense(features)
