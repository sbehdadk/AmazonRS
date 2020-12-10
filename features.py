import array
import json
import gzip
import pandas as pd
import gzip


def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)


def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')


def readImageFeatures(path):
  f = open(path, 'rb')
  while True:
    #print(f)
    asin = f.read(10)
    if asin == '': break
    #print(asin)
    a = array.array('f')
    #print(f.read(4096))
    a.fromfile(f, 4096)
    yield asin, a.tolist()


def main():
    ab = []
    cd = []
    path1 = "/media/sina/Daten/AmazonRS/dataset/image_features_Musical_Instruments.b"
    for asin, a in readImageFeatures(path1):
      #print(asin)
      #print(a)
      ab.append(asin)
      cd.append(a)
    print(type(ab))
    print(type(cd))
    #df = getDF('reviews_Video_Games.json.gz')

if __name__=='__main__':
    main()