import sys
import os
import tensorflow as tf

_feature_description = {
    'sector'            : tf.io.FixedLenFeature((), tf.string, default_value=''),
    'industry'          : tf.io.FixedLenFeature((), tf.string, default_value=''),
    'price'             : tf.io.FixedLenFeature((), tf.float32, default_value=0),
    'total_revenue_b'   : tf.io.FixedLenFeature((), tf.float32, default_value=0),
    'gross_profit_b'    : tf.io.FixedLenFeature((), tf.float32, default_value=0),
    'market_cap_b'      : tf.io.FixedLenFeature((), tf.float32, default_value=0),
    'num_employees'     : tf.io.FixedLenFeature((), tf.int64, default_value=0),
    'historical_high'   : tf.io.FixedLenSequenceFeature((), tf.float32, allow_missing=True),
    'historical_low'    : tf.io.FixedLenSequenceFeature((), tf.float32, allow_missing=True),
    'historical_close'  : tf.io.FixedLenSequenceFeature((), tf.float32, allow_missing=True),
    'historical_volume' : tf.io.FixedLenSequenceFeature((), tf.int64, allow_missing=True),
}

def _readTFRecord(serialized_example):
  return tf.io.parse_single_example(serialized_example, _feature_description)

def _filterByTensorSize(tensors):
  return tf.math.greater(tf.math.count_nonzero(tensors['historical_high']), 200)

def _filterZeros(tensor):
  mask = tf.cast(tensor, dtype=tf.bool)
  return tf.boolean_mask(tensor, mask)

def _resizeHistoricals(tensors):
  return ({
    'sector': tensors['sector'],
    'industry': tensors['industry'],
    'price': tensors['price'],
    'total_revenue_b': tensors['total_revenue_b'],
    'gross_profit_b': tensors['gross_profit_b'],
    'market_cap_b': tensors['market_cap_b'],
    'num_employees': tensors['num_employees'],
    'historical_high': tf.slice(_filterZeros(tensors['historical_high']), [0], [200]),
    'historical_low': tf.slice(_filterZeros(tensors['historical_low']), [0], [200]),
    'historical_close': tf.slice(_filterZeros(tensors['historical_close']), [0], [200]),
    'historical_volume': tf.slice(_filterZeros(tensors['historical_volume']), [0], [200]),
  })

class ModelInput:
  def __init__(self, root_dir:str):
    self._root_dir = root_dir

  def getAllPaths(self):
    paths = []
    for date in os.scandir(self._root_dir):
      if not date.is_dir:
        continue
      date_dir = '/'.join([self._root_dir, date.name])
      for f in os.scandir(date_dir):
        segs = f.name.split('.')
        if len(segs) < 2 or not segs[1] == 'tfrecords':
          continue
        paths.append(f.path)
    return paths

  def parseDataset(self):
    dataset = tf.data.TFRecordDataset(self.getAllPaths())
    dataset = dataset.map(_readTFRecord)
    dataset = dataset.filter(_filterByTensorSize)
    dataset = dataset.map(_resizeHistoricals)
    return dataset
