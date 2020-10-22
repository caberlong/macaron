import sys
import glob
import datetime
import tensorflow as tf
import csv

from proto import data_pb2
from proto import timeline_pb2
from proto.activity import activity_pb2
from data.utils.data_proto_generator import DataProtoGenerator

_simpleExampleActivityLength = 28
_simpleExampleLabelLength = 3
_interest_rate_file = '../../store/misc/fed-funds-rate.csv'

def _getActivityTimestamp(activity:activity_pb2.Activity):
  if activity.HasField('earning_activity'):
    return activity.earning_activity.activity_timestamp.start_timestamp.seconds
  elif activity.HasField('daily_stock_activity'):
    return activity.daily_stock_activity.date_timestamp.start_timestamp.seconds
  else:
    raise

def _getActivityTimestampIsoFormat(activity:activity_pb2.Activity):
  timestamp = _getActivityTimestamp(activity)
  return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

def _getActivityKey(activity:activity_pb2.Activity):
  if activity.HasField('earning_activity'):
    activity_type = 'earning_activity' 
  elif activity.HasField('daily_stock_activity'):
    activity_type = 'daily_stock_activity' 
  else:
    raise
  return ':'.join([activity_type, _getActivityTimestampIsoFormat(activity)])

def _getFedInterestRate(timestamp:int, rate_map:map):
  dt = datetime.datetime.fromtimestamp(timestamp)
  isofmt = dt.strftime('%Y-%m-%d')
  if isofmt in rate_map:
    return rate_map[isofmt]
  return _getFedInterestRate((dt - datetime.timedelta(days=1)).timestamp(), rate_map)

def _mergeTimelines(data:data_pb2.Data):
  activity_map = {}
  for timeline in data.timelines:
    for activity in timeline.activities:
      activity_map[_getActivityKey(activity)] = activity
  del data.timelines[0].activities[:]
  data.timelines[0].activities.extend(activity_map.values())
  data.timelines[0].activities.sort(reverse=True, key=_getActivityTimestamp)
  return data

def _inRange(tuple1, tuple2):
  start1, end1 = tuple1
  start2, end2 = tuple2
  return (start1 <= end2) and (end1 >= start2)

def _getDateRangeOfPath(path:str, root_dir:str):
  segs = path[len(root_dir)+1:].split('/')
  if segs[1] == 'monthly':
    start = datetime.datetime.fromisoformat(segs[2] + '-01')
    if start.month == 12:
      end = datetime.datetime(start.year + 1, 1, 1)
    else:
      end = datetime.datetime(start.year, start.month + 1, 1)
  elif segs[1] == 'daily':
    start = datetime.datetime.fromisoformat(segs[2])
    end = start + datetime.timedelta(days=1)
  elif segs[1] == 'yearly':
    start = datetime.datetime.fromisoformat(segs[2] + '-01-01')
    end = datetime.datetime(start.year + 1, 1, 1)
  else:
    raise
  return start.timestamp(), end.timestamp()

def _normalizedPricesToExample(prices:list, key:str, generator, example:tf.train.Example):
  config = '''
    features {
      feature {
        key: "%s";
        value {
          float_list {
            value: $FLOAT;
          }
        }
      }
    }
  ''' % key
  generator.configurate(config);
  for price in prices:
    generator.generateDataProto(example, 
                                new_repeats={'value':1}, 
                                var_values={'FLOAT':price})

def _labelPriceToExample(label_price, generator, example:tf.train.Example):
  config = '''
    features {
      feature {
        key: "label_price";
        value {
          float_list {
            value: $FLOAT;
          }
        }
      }
    }
  '''
  generator.configurate(config);
  generator.generateDataProto(example, var_values={'FLOAT':label_price})

def _getFedInterestRates(csv_path:str):
  fed_rate_map = {}
  with open(csv_path, 'r') as f:
    reader = csv.reader(f)
    for row in list(reader):
      fed_rate_map[row[0]] = float(row[1])
  return fed_rate_map

class NormalizedExampleGenerator:
  def __init__(self, 
               root_dir:str,
               symbol:str = None,
               start_timestamp:int = None,
               end_timestamp:int = None,
               length:int = _simpleExampleActivityLength,
               label_length: int = _simpleExampleLabelLength):
    self._root_dir = root_dir
    self._generator = DataProtoGenerator()
    self._length = length
    self._label_length = label_length
    self._fed_rate_map = _getFedInterestRates(_interest_rate_file)
    self._merged_timeline = None
    if symbol:
      self._merged_timeline = self.getMergedTimeline(
          root_dir, symbol, start_timestamp, end_timestamp)

  def printFedRateMap(self):
    print(self._fed_rate_map)

  def getMergedTimeline(self, root_dir:str, symbol:str, start_timestamp:int, end_timestamp:int):
    '''Merge all timelines for the symbol between the timestamp'''
    pattern = '/'.join([
      root_dir,
      '*', # data type
      '*', # time period type
      '*', # time period value
      '.'.join([symbol, 'proto'])
    ])
    data = data_pb2.Data()
    for path in glob.glob(pattern):
      if not _inRange((_getDateRangeOfPath(path, root_dir)), (start_timestamp, end_timestamp)):
        continue
      with open(path, "rb") as f:
        d = data_pb2.Data()
        d.ParseFromString(f.read())
        data.timelines.extend(d.timelines)
    return _mergeTimelines(data)

  def getSimpleExamples(self):
    examples = []
    activities = self._merged_timeline.timelines[0].activities;
    for index in range(len(activities)):
      example = self.getSimpleExample(activities, index)
      if example:
        examples.append(example)
    return examples

  def getSimpleExampleAtDate(self, timestamp:int):
    activities = self._merged_timeline.timelines[0].activities;
    for index in range(len(activities)):
      activity = activities[index]
      activity_timestamp = _getActivityTimestamp(activity)
      if activity_timestamp > timestamp:
        continue
      return self.getSimpleExample(activities, index)
    return None

  def getInferenceExampleAtDate(self, symbol:str, timestamp:int):
    if not self._merged_timeline:
      start_timestamp = timestamp - self._length * 24 * 3600 * 2
      end_timestamp = timestamp
      self._merged_timeline = self.getMergedTimeline(
          self._root_dir, symbol, start_timestamp, end_timestamp)
    activities = self._merged_timeline.timelines[0].activities
    for index in range(len(activities)):
      activity = activities[index]
      activity_timestamp = _getActivityTimestamp(activity)
      if activity_timestamp > timestamp:
        continue
      return self.getInferenceExample(activities, index)
    return None, None

  def getClosePriceAtDate(self, symbol:str, timestamp:int):
    timeline = self.getMergedTimeline(self._root_dir, symbol, timestamp, timestamp)
    for activity in timeline.timelines[0].activities:
      if _getActivityTimestamp(activity) == timestamp:
        if activity.HasField('daily_stock_activity'):                                                   
          return activity.daily_stock_activity.close
    return None

  def getSimpleExample(self, activities, index):
    norm_prices, norm_highs, norm_lows, norm_volumes, fed_rates, _ = self.getNormalizedValues(
        activities, index, self._length + self._label_length)
    if norm_prices == None:
      return None

    # Get the label price as volume averaged
    total_volume = 0
    total_price = 0
    for count in range(self._label_length):
      idx = self._length + count
      this_volume = norm_volumes[idx] * (1 / 2 ** count)
      total_volume = total_volume + this_volume
      total_price = total_price + norm_prices[idx] * this_volume
    label_price = total_price / total_volume

    example = tf.train.Example()
    
    _normalizedPricesToExample(
        norm_prices[:-self._label_length], 'historical_prices', self._generator, example)
    _normalizedPricesToExample(
        norm_highs[:-self._label_length], 'historical_highs', self._generator, example)
    _normalizedPricesToExample(
        norm_lows[:-self._label_length], 'historical_lows', self._generator, example)
    _normalizedPricesToExample(
        norm_volumes[:-self._label_length], 'historical_volumes', self._generator, example)
    _normalizedPricesToExample(
        fed_rates[:-self._label_length], 'fed_rates', self._generator, example)
    _labelPriceToExample(label_price, self._generator, example)
    return example

  def getInferenceExample(self, activities, index):
    norm_prices, norm_highs, norm_lows, norm_volumes, fed_rates, scale = self.getNormalizedValues(
        activities, index, self._length)
    if norm_prices == None:
      return None, None
    example = tf.train.Example()
    _normalizedPricesToExample(norm_prices, 'historical_prices', self._generator, example)
    _normalizedPricesToExample(norm_highs, 'historical_highs', self._generator, example)
    _normalizedPricesToExample(norm_lows, 'historical_lows', self._generator, example)
    _normalizedPricesToExample(norm_volumes, 'historical_volumes', self._generator, example)
    _normalizedPricesToExample(fed_rates, 'fed_rates', self._generator, example)
    return example, scale

  def getNormalizedValues(self, activities, index, length):
    activity = activities[index]
    if not activity.HasField('daily_stock_activity'):
      return None, None, None, None, None, None

    base_price = activity.daily_stock_activity.close * activity.daily_stock_activity.split
    base_volume = activity.daily_stock_activity.volume / activity.daily_stock_activity.split 
    init_base_price = base_price
    if not base_price or not base_volume:
      return None, None, None, None, None, None

    norm_prices = []
    norm_highs = []
    norm_lows = []
    norm_volumes = []
    fed_rates = []
    while len(norm_prices) < length:
      if index > len(activities) - 1:
        return None, None, None, None, None, None
      activity = activities[index]
      if not (activity.HasField('daily_stock_activity') and
              activity.daily_stock_activity.close and
              activity.daily_stock_activity.high and
              activity.daily_stock_activity.low and
              activity.daily_stock_activity.volume and
              activity.daily_stock_activity.split):
        index = index + 1
        continue
      norm_prices.append(activity.daily_stock_activity.close / base_price)
      norm_highs.append(activity.daily_stock_activity.high / base_price)
      norm_lows.append(activity.daily_stock_activity.low / base_price)
      norm_volumes.append(activity.daily_stock_activity.volume / base_volume)
      fed_rates.append(_getFedInterestRate(_getActivityTimestamp(activity), self._fed_rate_map))
          
      base_price = base_price * activity.daily_stock_activity.split
      base_volume = base_volume / activity.daily_stock_activity.split

      index = index + 1

    norm_prices.reverse()
    norm_highs.reverse()
    norm_lows.reverse()
    norm_volumes.reverse()
    fed_rates.reverse()

    scale = norm_prices[0]
    norm_prices = [price/scale for price in norm_prices]
    norm_highs = [price/scale for price in norm_highs]
    norm_lows = [price/scale for price in norm_lows]

    volume_scale = norm_volumes[0]
    norm_volumes = [volume/volume_scale for volume in norm_volumes]

    return norm_prices, norm_highs, norm_lows, norm_volumes, fed_rates, init_base_price/scale

  @property
  def mergedTimeline(self):
    return self._merged_timeline
