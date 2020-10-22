import sys
import tensorflow as tf
import datetime as datetime

from model.alpha_advantage.model_input import ModelInput
from model.alpha_advantage.simple_lstm import SimpleLSTMModel
from data.example.alpha_advantage.normalized_example_generator import NormalizedExampleGenerator

_data_store_root = '../../data/store' 

class Predictor:
  def __init__(self):
    self._model = self.loadModel()
    self._timeline_dir = '/'.join([_data_store_root, 'alpha_advantage', 'timeline'])                                                                                                
    self._example_generator = NormalizedExampleGenerator(root_dir=self._timeline_dir)                                                                            

  def loadModel(self):
    model_input = ModelInput('/'.join([
        _data_store_root,
        'alpha_advantage',
        'normalized_price_simple_example'
    ]))
    latest = tf.train.latest_checkpoint('/'.join([_data_store_root, 'model_510_2']))
    simple_lstm = SimpleLSTMModel(model_input)
    optimizer = tf.keras.optimizers.Adam(learning_rate=2.0e-2)                                        
    simple_lstm.model.compile(optimizer, loss=tf.keras.losses.MeanSquaredError())
    status = simple_lstm.model.load_weights(latest)
    status.expect_partial()
    return simple_lstm

  def predict(self, symbol:str, dt:datetime):
    example, scale = self._example_generator.getInferenceExampleAtDate('AAPL', dt.timestamp())
    if not example:
      return None
    results = self._model.model.predict(ModelInput.parseInferenceExample(example), batch_size=1)
    return results[0][0] * scale

  def getClosePrice(self, symbol:str, dt:datetime):
    return self._example_generator.getClosePriceAtDate(symbol, dt.timestamp())
