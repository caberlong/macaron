import sys
import os
import tensorflow as tf
from tensorflow.data import Dataset

_feature_description = {
    'label_price'        : tf.io.FixedLenFeature((1,), tf.float32, default_value=0),
    'historical_prices'  : tf.io.FixedLenSequenceFeature((), tf.float32, allow_missing=True),
    'historical_highs'   : tf.io.FixedLenSequenceFeature((), tf.float32, allow_missing=True),
    'historical_lows'    : tf.io.FixedLenSequenceFeature((), tf.float32, allow_missing=True),
    'historical_volumes' : tf.io.FixedLenSequenceFeature((), tf.float32, allow_missing=True),
    'fed_rates'          : tf.io.FixedLenSequenceFeature((), tf.float32, allow_missing=True),
}

_int32_base = 100

def _readTFRecord(serialized_example):
  return tf.io.parse_single_example(serialized_example, _feature_description)

def _featureTensors(tensors):
  return ({
    'historical_prices': tf.reshape(tf.stack([_toInt32(tensors['historical_prices']),
                                              _toInt32(tensors['historical_highs']),
                                              _toInt32(tensors['historical_lows']),
                                              _toInt32(tensors['historical_volumes']),
                                              _toInt32(tensors['fed_rates'])], axis=1), [1, 28, 5])
  })

def _labelTensor(tensors):
  return _toInt32(tensors['label_price'])

def _toInt32(tensor):
  return tf.math.floor(tf.multiply(tensor, _int32_base))

class ModelInput:
  def __init__(self, root_dir:str):
    self._dataset = self._parseDataset(root_dir)
    self._dataset.shuffle(1000)
    self._train_size = (int)(self._dataset.reduce(0, lambda x, _: x + 1).numpy() * 0.8)
    self._timeSeriesInputs = self._getTimeSeriesInputs()
    self._base = 100

  def _getAllPaths(self, root_dir):
    paths = []
    for f in os.scandir(root_dir):
      segs = f.name.split('.')
      if len(segs) < 2 or not segs[1] == 'tfrecords':
        continue
      paths.append(f.path)
    return paths

  def _getFeatures(self, dataset):
    return dataset.map(_featureTensors)

  def _getLabel(self, dataset):
    return dataset.map(_labelTensor)

  def _parseDataset(self, root_dir:str):
    dataset = tf.data.TFRecordDataset(self._getAllPaths(root_dir)).map(_readTFRecord)
    return tf.data.Dataset.zip((self._getFeatures(dataset), self._getLabel(dataset)))

  def _getTimeSeriesInputs(self):
    return tf.keras.Input(shape=(None, 5), name='historical_prices', dtype=tf.float32)

  def parseInferenceExample(example:tf.train.Example):
    tensors = tf.io.parse_single_example(
        example.SerializeToString(), _feature_description)
    return _featureTensors(tensors)

  @property
  def dataset(self):
    return self._dataset

  @property
  def dataset_train(self):
    return self._dataset.take(self._train_size)

  @property
  def dataset_test(self):
    return self._dataset.skip(self._train_size)

  @property
  def timeSeriesInputs(self):
    return self._timeSeriesInputs
