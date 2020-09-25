import sys
import os
import tensorflow as tf

from model.alpha_advantage.model_input import ModelInput

class SimpleLSTMModel(): 
  def __init__(self, model_input: ModelInput):
    self._model_input = model_input

  def model(self):
    price = self._model_input.timeSeriesInputs
    input_layer = [price]

    rnn_cell = tf.keras.layers.LSTMCell(20)
    rnn_layer = tf.keras.layers.RNN(rnn_cell)(price)
    pred = tf.keras.layers.Dense(1)(rnn_layer)

    model_full = tf.keras.Model(inputs=input_layer, outputs=pred)
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-6)
    model_full.compile(optimizer, loss=tf.keras.losses.MeanSquaredError())

    return model_full
