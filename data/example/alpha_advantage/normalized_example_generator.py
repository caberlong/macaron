import sys
import glob
import datetime
import tensorflow as tf
import csv

from proto import data_pb2
from proto import timeline_pb2
from proto.activity import activity_pb2
from data.utils.data_proto_generator import DataProtoGenerator

_simpleExampleActivityLength = 20
_interest_rate_file = '/Users/longchb/Documents/GitHub/macaron/data/store/misc/fed-funds-rate.csv'

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

def _getFedInterestRate(timestamp:int, rate_map:map):
  dt = datetime.datetime.fromtimestamp(timestamp)
  isofmt = dt.strftime('%Y-%m-%d')
  if isofmt in rate_map:
    return rate_map[isofmt]
  return _getFedInterestRate((dt - datetime.timedelta(days=1)).timestamp(), rate_map)

def _mergeTimelines(data:data_pb2.Data):
    new_timeline = timeline_pb2.Timeline()
    for timeline in data.timelines:
      for activity in timeline.activities:
        new_timeline.activities.append(activity)
    new_timeline.activities.sort(reverse=True, key=_getActivityTimestamp)
    while (len(data.timelines) > 0):
      data.timelines.pop()
    data.timelines.append(new_timeline)
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
               symbol:str,
               start_timestamp:int,
               end_timestamp:int,
               length:int = _simpleExampleActivityLength):
    self._generator = DataProtoGenerator()
    self._length = length
    self._merged_timeline = self.getMergedTimeline(
        root_dir, symbol, start_timestamp, end_timestamp)
    self._fed_rate_map = _getFedInterestRates(_interest_rate_file)

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

  def getSimpleExample(self, activities, index):
    activity = activities[index]
    if not activity.HasField('daily_stock_activity'):
      return None

    base_price = activity.daily_stock_activity.close * activity.daily_stock_activity.split
    base_volume = activity.daily_stock_activity.volume / activity.daily_stock_activity.split 
    if not base_price or not base_volume:
      return None

    norm_prices = []
    norm_highs = []
    norm_lows = []
    norm_volumes = []
    fed_rates = []
    index = index + 1
    while len(norm_prices) <= self._length:
      if index >= len(activities) - 1:
        return None
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

    label_price = 1.0 / scale

    example = tf.train.Example()
    _normalizedPricesToExample(norm_prices[:-1], 'historical_prices', self._generator, example)
    _normalizedPricesToExample(norm_highs[:-1], 'historical_highs', self._generator, example)
    _normalizedPricesToExample(norm_lows[:-1], 'historical_lows', self._generator, example)
    _normalizedPricesToExample(norm_volumes[:-1], 'historical_volumes', self._generator, example)
    _normalizedPricesToExample(fed_rates[:-1], 'fed_rates', self._generator, example)
    _labelPriceToExample(label_price, self._generator, example)
    return example

  @property
  def mergedTimeline(self):
    return self._merged_timeline
