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
    return tf.keras.layers.Dense(10)(
        self._model_input.categoricalFeatures(self._model_input.categoricalFeatureInputs))

  def timeSerialsModel(self):
    inputs = self._model_input.timeSerialsInputs
    print('sequential inputs are: %s' % inputs)
    self._input_layers.append(inputs)

    rnn_cell = tf.keras.layers.LSTMCell(10)
    rnn_layer = tf.keras.layers.RNN(rnn_cell)(inputs)

    #return tf.slice(tf.keras.layers.Dense(10)(rnn_layer), [0, 0], [1, 1])
    return tf.keras.layers.Dense(10)(rnn_layer)

  def model(self):
    categorical_model = self.categoricalModel()
    time_serials_model = self.timeSerialsModel()

    #print("categorical_model: %s, time serials_model: %s" % (categorical_model, time_serials_model))

    merged_model = tf.keras.layers.concatenate([categorical_model, time_serials_model])
    #pre_preds = tf.keras.layers.Dense(10)(merged_model)
    #pre_preds = tf.keras.layers.BatchNormalization()(pre_preds)
    #pre_preds = tf.keras.layers.Dense(1)(pre_preds)
    #pre_preds = tf.keras.layers.BatchNormalization()(pre_preds)
    #pred = tf.keras.layers.Dense(1,activation='sigmoid')(pre_preds)
    model_full = tf.keras.Model(inputs=self._input_layers, outputs=merged_model)
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)                                          
    model_full.compile(optimizer, loss=tf.keras.losses.MeanSquaredError())                          

    return model_full
