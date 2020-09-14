import sys
import tensorflow as tf


def plotHistoricalPrices(path:str):
  raw_dataset = tf.data.TFRecordDataset("path")
  for raw_record in raw_dataset.take(1):
      example = tf.train.Example()
      example.ParseFromString(raw_record.numpy())
      print(example)

def main(argv):                                                                                     
  plotHistoricalPrices(argv[1])

                                                                                                    
if __name__ == '__main__':                                                                          
  main(sys.argv)
