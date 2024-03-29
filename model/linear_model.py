import sys
import os
import tensorflow as tf

from model.model_input import ModelInput

class LinearModel(): 
  def __init__(self, model_input: ModelInput):
    self._model_input = model_input
    self._input_layers = []

  def categoricalModel(self):
    self._input_layers.extend(self._model_input.categoricalFeatureInputs.values())
    return tf.keras.layers.Dense(3)(
        self._model_input.categoricalFeatures(self._model_input.categoricalFeatureInputs))

  def timeSerialsModel(self):
    inputs = self._model_input.timeSerialsInputs
    self._input_layers.append(inputs)

    rnn_cell = tf.keras.layers.LSTMCell(5)
    rnn_layer = tf.keras.layers.RNN(rnn_cell)(inputs)

    return rnn_layer

  def model(self):
    categorical_model = self.categoricalModel()
    time_serials_model = self.timeSerialsModel()

    merged_model = tf.keras.layers.concatenate([categorical_model, time_serials_model])
    pred = tf.keras.layers.Dense(1)(merged_model)
    model_full = tf.keras.Model(inputs=self._input_layers, outputs=pred)
    optimizer = tf.keras.optimizers.Adam(learning_rate=5e-4)                                          
    model_full.compile(optimizer, loss=tf.keras.losses.MeanSquaredError())                          

    return model_full
