import sys
import tensorflow as tf
import datetime as datetime

from model.alpha_advantage.model_input import ModelInput
from model.alpha_advantage.simple_lstm import SimpleLSTMModel
from data.example. import SimpleLSTMModel

_data_store_root = '/Users/longchb/Documents/GitHub/macaron/data/store' 

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
    simple_lstm = SimpleLSTMModel(model_input)
    simple_lstm.model().load_weights('/'.join([_data_store_root, 'model_510']))
    return simple_lstm

  def predict(self, symbol:str, date:datetime.date):
    
