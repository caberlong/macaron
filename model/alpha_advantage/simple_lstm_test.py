import sys

from model.alpha_advantage.model_input import ModelInput
from model.alpha_advantage.simple_lstm import SimpleLSTMModel


def main(argv):                                                                                     
  root_dir = '/'.join([
      '/Users/longchb/Documents/GitHub/macaron/data/store',
      'alpha_advantage',
      'normalized_price_simple_example'
  ])
  model_input = ModelInput(root_dir)
  simple_lstm = SimpleLSTMModel(model_input)
  simple_lstm.model().fit(model_input.dataset, epochs=20, batch_size=32)
                                                                                                    
if __name__ == '__main__':                                                                          
  main(sys.argv)

# Results:

# Baseline 3.7473e-04
# Valina LSTM: 20 epochs 0.0051
# + open/close/volume: 20 epochs 5.5889e-04
