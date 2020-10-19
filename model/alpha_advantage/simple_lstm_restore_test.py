import sys
import tensorflow as tf

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
  checkpoint_filepath = '/Users/longchb/Documents/GitHub/macaron/data/store/model_510_2'

  latest = tf.train.latest_checkpoint(checkpoint_filepath)
  optimizer = tf.keras.optimizers.Adam(learning_rate=2.0e-2)
  simple_lstm.model.compile(optimizer, loss=tf.keras.losses.MeanSquaredError())
  status = simple_lstm.model.load_weights(latest)
  status.assert_existing_objects_matched()

  checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
      filepath=checkpoint_filepath,
      save_weights_only=True,
      monitor='val_loss',
      mode='min',
      save_best_only=True)
  simple_lstm.model.fit(model_input.dataset_train,
                        epochs=30,
                        batch_size=32,
                        validation_data=model_input.dataset_test,
                        callbacks=[checkpoint_callback])
                                                                                                    
if __name__ == '__main__':                                                                          
  main(sys.argv)

# Results:

# Baseline 3.7473e-04
# Valina LSTM: 20 epochs 0.0051
# + open/close/volume: 20 epochs 5.5889e-04
# + open/close/volume + fed interest rate: 20 epochs 6.33-04
