import sys
import os
import tensorflow as tf

class EmbeddingModel(): 
  def __init__(self, model_input):
    self._feature_layer = feature_layer
    self._dense = tf.keras.layers.Dense(1)

  def call(self, inputs):
    features = self._feature_layer(inputs)
    return self._dense(features)
