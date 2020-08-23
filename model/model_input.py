import sys
import os
import tensorflow as tf
from tensorflow import feature_column                                                               
from tensorflow.keras import layers
from tensorflow.data import Dataset

_num_days = 100

_feature_description = {
    'sector'            : tf.io.FixedLenFeature((1,), tf.string, default_value=''),
    'industry'          : tf.io.FixedLenFeature((1,), tf.string, default_value=''),
    'price'             : tf.io.FixedLenFeature((1,), tf.float32, default_value=0),
    'total_revenue_b'   : tf.io.FixedLenFeature((1,), tf.float32, default_value=0),
    'gross_profit_b'    : tf.io.FixedLenFeature((1,), tf.float32, default_value=0),
    'market_cap_b'      : tf.io.FixedLenFeature((1,), tf.float32, default_value=0),
    'num_employees'     : tf.io.FixedLenFeature((1,), tf.int64, default_value=0),
    'historical_high'   : tf.io.FixedLenSequenceFeature((), tf.float32, allow_missing=True),
    'historical_low'    : tf.io.FixedLenSequenceFeature((), tf.float32, allow_missing=True),
    'historical_close'  : tf.io.FixedLenSequenceFeature((), tf.float32, allow_missing=True),
    'historical_volume' : tf.io.FixedLenSequenceFeature((), tf.int64, allow_missing=True),
}

_sector_vocabs = ['Technology', 'Healthcare', 'Financial Services']                                 
                                                                                                    
_industry_vocabs = [                                                                                
  'Consumer Electronics',                                                                           
  'Drug Manufacturers\xe2\x80\x94General',                                                          
  'Medical Devices',                                                                                
  'Information Technology Services',                                                                
  'Software\xe2\x80\x94Infrastructure',                                                             
  'Semiconductors',                                                                                 
  'Software\xe2\x80\x94Application',                                                                
  'Medical Instruments & Supplies',                                                                 
  'Semiconductor Equipment & Materials',                                                            
  'Healthcare Plans',                                                                               
  'Electronic Components',                                                                          
  'Banks\xe2\x80\x94Diversified',                                                                   
  'Communication Equipment',                                                                        
  'Computer Hardware',                                                                              
  'Diagnostics & Research',                                                                         
  'Medical Care Facilities',                                                                        
  'Insurance\xe2\x80\x94Life',                                                                      
  'Credit Services',
  'Biotechnology',                                                                                  
  'Financial Data & Stock Exchanges',                                                               
  'Health Information Services',                                                                    
  'Pharmaceutical Retailers',                                                                       
  'Drug Manufacturers\xe2\x80\x94Specialty & Generic',                                              
]

def _readTFRecord(serialized_example):
  return tf.io.parse_single_example(serialized_example, _feature_description)

def _filterByTensorSize(tensors):
  return tf.math.greater(tf.math.count_nonzero(tensors['historical_high']), _num_days)

def _filterZeros(tensor):
  mask = tf.cast(tensor, dtype=tf.bool)
  return tf.boolean_mask(tensor, mask)

def _toSparse(tensor):
  return tf.sparse.from_dense(tensor)

def _resizeHistoricals(tensors):
  return ({
    'sector': tensors['sector'],
    'industry': tensors['industry'],
    'price': tensors['price'],
    'total_revenue_b': tensors['total_revenue_b'],
    'gross_profit_b': tensors['gross_profit_b'],
    'market_cap_b': tensors['market_cap_b'],
    'num_employees': tensors['num_employees'],
    'historical_high': tf.slice(_filterZeros(tensors['historical_high']), [1], [_num_days]),
    'historical_low': tf.slice(_filterZeros(tensors['historical_low']), [1], [_num_days]),
    'historical_close': tf.slice(_filterZeros(tensors['historical_close']), [1], [_num_days]),
    'historical_volume': tf.slice(_filterZeros(tensors['historical_volume']), [1], [_num_days]),
  })

def _concatHistoricals(tensors):
  return ({
    'sector': tensors['sector'],
    'industry': tensors['industry'],
    'price': tensors['price'],
    'total_revenue_b': tensors['total_revenue_b'],
    'gross_profit_b': tensors['gross_profit_b'],
    'market_cap_b': tensors['market_cap_b'],
    'num_employees': tensors['num_employees'],
    'historical_prices': tf.reshape(tf.stack([
        tensors['historical_high'],
        tensors['historical_low'],
        tensors['historical_close'],
        tf.cast(tensors['historical_volume'], tf.float32)], axis=1), [1, 100, 4]),
  })


def _featureTensors(tensors):
  return ({
    'sector': tensors['sector'],
    'industry': tensors['industry'],
    'total_revenue_b': tensors['total_revenue_b'],
    'gross_profit_b': tensors['gross_profit_b'],
    'market_cap_b': tensors['market_cap_b'],
    'num_employees': tensors['num_employees'],
    'historical_prices': tensors['historical_prices'],
  })

def _labelTensor(tensors):
  return tensors['price']

class ModelInput:
  def __init__(self, root_dir:str):
    self._dataset = self._parseDataset(root_dir)
    self._categoricalFeatures, self._categoricalFeatureInputs = self._buildCategoricalFeatures()
    self._timeSerialsInputs = self._getTimeSerialsInputs()

  def _getAllPaths(self, root_dir):
    paths = []
    for date in os.scandir(root_dir):
      if not date.is_dir:
        continue
      date_dir = '/'.join([root_dir, date.name])
      for f in os.scandir(date_dir):
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
    dataset = tf.data.TFRecordDataset(self._getAllPaths(root_dir))
    dataset = dataset.map(_readTFRecord)
    dataset = dataset.filter(_filterByTensorSize)
    dataset = dataset.map(_resizeHistoricals)
    dataset = dataset.map(_concatHistoricals)
    return tf.data.Dataset.zip((self._getFeatures(dataset), self._getLabel(dataset)))

  def _buildCategoricalFeatures(self):
    feature_columns = []
    inputs = {}
    sector = feature_column.categorical_column_with_vocabulary_list(                               
      'sector', _sector_vocabs)
    inputs['sector'] = tf.keras.Input(shape=(1,), name='sector', dtype=tf.string)
    feature_columns.append(feature_column.indicator_column(sector))

    industry = feature_column.categorical_column_with_vocabulary_list(                               
      'industry', _industry_vocabs)
    inputs['industry'] = tf.keras.Input(shape=(1,), name='industry', dtype=tf.string)
    feature_columns.append(feature_column.indicator_column(industry))

    total_revenue = feature_column.numeric_column('total_revenue_b')
    inputs['total_revenue_b'] = tf.keras.Input(shape=(1,), name='total_revenue_b', dtype=tf.float32)
    feature_columns.append(total_revenue)

    gross_profit = feature_column.numeric_column('gross_profit_b')
    inputs['gross_profit_b'] = tf.keras.Input(shape=(1,), name='gross_profit_b', dtype=tf.float32)
    feature_columns.append(gross_profit)

    market_cap = feature_column.numeric_column('market_cap_b')
    inputs['market_cap_b'] = tf.keras.Input(shape=(1,), name='market_cap_b', dtype=tf.float32)
    feature_columns.append(market_cap)

    num_employees = feature_column.numeric_column('num_employees')
    inputs['num_employees'] = tf.keras.Input(shape=(1,), name='num_employees', dtype=tf.int32)
    feature_columns.append(num_employees)

    return tf.keras.layers.DenseFeatures(feature_columns), inputs

  def _getTimeSerialsInputs(self):
    #historical_high = feature_column.sequence_numeric_column('historical_high', shape=(_num_days,))
    #inputs['historical_high'] = tf.keras.Input(
    #    shape=(_num_days,), name='historical_high', sparse=True, dtype=tf.float32)
    #feature_columns.append(historical_high)

    #historical_low = feature_column.numeric_column('historical_low')
    #feature_columns.append(historical_low)

    historical_prices = tf.keras.Input(shape=(None, 4), name='historical_prices', dtype=tf.float32)

    #historical_volume = feature_column.numeric_column('historical_volume')
    #feature_columns.append(historical_volume)

    return historical_prices

  @property
  def dataset(self):
    return self._dataset

  @property
  def categoricalFeatures(self):
    return self._categoricalFeatures

  @property
  def categoricalFeatureInputs(self):
    return self._categoricalFeatureInputs

  @property
  def timeSerialsInputs(self):
    return self._timeSerialsInputs
