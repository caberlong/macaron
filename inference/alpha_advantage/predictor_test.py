import sys
import datetime as datetime

from inference.alpha_advantage.predictor import Predictor


def main(argv):                                                                                     
  predictor = Predictor()
  symbol = 'AAPL'
  dt = datetime.datetime(2020, 10, 1)
  delta = datetime.timedelta(days=1)
  count = 0
  actual = []
  predict = []
  while count < 100:
    price = predictor.getClosePrice(symbol, dt)
    print('date %s, count %d' % (dt.isoformat(), count))
    dt = dt - delta
    if not price:
      print('\tcannot get price')
      continue
    predict_price = predictor.predict(symbol, dt)
    if not predict_price:
      print('\tcannot predict price')
      continue
    actual.append(price)
    predict.append(predict_price)
    count = count + 1

  for idx in range(count):
    print('%s:%s' % (predict[idx], actual[idx]))
                                                                                                    
if __name__ == '__main__':                                                                          
  main(sys.argv)

# Results:

# Baseline 3.7473e-04
# Valina LSTM: 20 epochs 0.0051
# + open/close/volume: 20 epochs 5.5889e-04
# + open/close/volume + fed interest rate: 20 epochs 6.33-04
