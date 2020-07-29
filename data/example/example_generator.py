import sys
import tensorflow as tf

from proto import data_pb2
from data.utils.data_proto_generator import DataProtoGenerator

class ExampleGenerator:
  def __init__(self):
    self._generator = DataProtoGenerator()
    self._new_repeats = {'value':1}

  def addFeature(self, config:str, data:data_pb2.Data, example:tf.train.Example):
    self._generator.generateDataProto(
        config, example, new_repeats=self._new_repeats, var_values={'DATA': data})

  def addCommonTraitSector(self, data:data_pb2.Data, example:tf.train.Example): 
    self.addFeature('''
      features {
        feature {
          key: "sector";
          value {
            bytes_list {
              value: $DATA.timelines.fin_entity.traits.common_trait.sector;
            }
          }
        }
      }''', data, example)

  def addCommonTraitIndustry(self, data:data_pb2.Data, example:tf.train.Example): 
    self.addFeature('''
      features {
        feature {
          key: "industry";
          value {
            bytes_list {
              value: $DATA.timelines.fin_entity.traits.common_trait.industry;
            }
          }
        }
      }''', data, example)

  def addTradingActivityPrice(self, data:data_pb2.Data, example:tf.train.Example): 
    self.addFeature('''
      features {
        feature {
          key: "price";
          value {
            float_list {
              value: $DATA.timelines.activities.trading_activity.price;
            }
          }
        }
      }''', data, example)

  def addTradingActivityTotalRevenue(self, data:data_pb2.Data, example:tf.train.Example): 
    self.addFeature('''
      features {
        feature {
          key: "total_revenue_b";
          value {
            float_list {
              value: $DATA.timelines.activities.trading_activity.total_revenue / 1000000000;
            }
          }
        }
      }''', data, example)

  def addTradingActivityGrossProfit(self, data:data_pb2.Data, example:tf.train.Example): 
    self.addFeature('''
      features {
        feature {
          key: "gross_profit_b";
          value {
            float_list {
              value: $DATA.timelines.activities.trading_activity.gross_profit / 1000000000;
            }
          }
        }
      }''', data, example)

  def addTradingActivityMarketCap(self, data:data_pb2.Data, example:tf.train.Example): 
    self.addFeature('''
      features {
        feature {
          key: "market_cap_b";
          value {
            float_list {
              value: $DATA.timelines.activities.trading_activity.market_cap / 1000000000;
            }
          }
        }
      }''', data, example)

  def addTradingActivityNumEmployees(self, data:data_pb2.Data, example:tf.train.Example): 
    self.addFeature('''
      features {
        feature {
          key: "num_employees";
          value {
            int64_list {
              value: $DATA.timelines.activities.trading_activity.num_full_time_employees;
            }
          }
        }
      }''', data, example)

  def addTradingActivityHistoricalPriceHigh(self, data:data_pb2.Data, example:tf.train.Example):
    self.addFeature('''
      features {
        feature {
          key: "historical_high";
          value {
            float_list {
              value: $DATA.timelines.activities.trading_activity.historical_prices.high;
            }
          }
        }
      }''', data, example)

  def addTradingActivityHistoricalPriceLow(self, data:data_pb2.Data, example:tf.train.Example):
    self.addFeature('''
      features {
        feature {
          key: "historical_low";
          value {
            float_list {
              value: $DATA.timelines.activities.trading_activity.historical_prices.low;
            }
          }
        }
      }''', data, example)

  def addTradingActivityHistoricalPriceClose(self, data:data_pb2.Data, example:tf.train.Example):
    self.addFeature('''
      features {
        feature {
          key: "historical_close";
          value {
            float_list {
              value: $DATA.timelines.activities.trading_activity.historical_prices.close;
            }
          }
        }
      }''', data, example)

  def addTradingActivityHistoricalPriceVolumn(self, data:data_pb2.Data, example:tf.train.Example):
    self.addFeature('''
      features {
        feature {
          key: "historical_volume";
          value {
            int64_list {
              value: $DATA.timelines.activities.trading_activity.historical_prices.volume;
            }
          }
        }
      }''', data, example)


  def generateExample(self, data:data_pb2.Data):
    example = tf.train.Example()

    # Common trait
    self.addCommonTraitSector(data, example)
    self.addCommonTraitIndustry(data, example)

    # Trading activity
    self.addTradingActivityPrice(data, example)
    self.addTradingActivityTotalRevenue(data, example)
    self.addTradingActivityGrossProfit(data, example)
    self.addTradingActivityMarketCap(data, example)
    self.addTradingActivityNumEmployees(data, example)
    self.addTradingActivityHistoricalPriceHigh(data, example)
    self.addTradingActivityHistoricalPriceLow(data, example)
    self.addTradingActivityHistoricalPriceClose(data, example)
    self.addTradingActivityHistoricalPriceVolumn(data, example)

    return example
