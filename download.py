## Importing Necessary Modules
import requests # to get image from the web
import shutil # to save it locally
import argparse
import gzip
from pymongo import MongoClient
import urllib
from urllib import request
import logging
import os


def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)


def get_args():
    parser = argparse.ArgumentParser(description="this Script will download images using the Url from metadata",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--imageURL", type=str,
                        default='./dataset/', help="path to metadata file")

    args = parser.parse_args()
    return args


def get_the_URL():
    adress = []
    i = 0
    for metadata in parse("./dataset/meta_Clothing_Shoes_and_Jewelry.json.gz"):

        if "categories" in metadata and "imUrl" in metadata :
            namestring = str(metadata["categories"])[3:-3] + "_" + str(metadata["asin"])
            print("the name of checking process is :" + namestring)

            if not os.path.isfile("/media/sina/Daten/AmazonRS/dataset/1/"+ namestring):
                print("file doesn't exist...")
                #print(metadata["imUrl"])
                #print(metadata["asin"])
                #print(metadata.keys())
                #new_str = str(metadata["categories"])[3:-3] 
                #filename = new_str + "_" + str(metadata["asin"])
                #print(filename)
                try:
                    request.urlretrieve(metadata["imUrl"],"/media/sina/Daten/AmazonRS/dataset/1/"+ namestring)
                except:
                    pass

                adress.append(metadata['imUrl'])
                print("downloaded first...!")
            else:
                print("file existed...")
                continue
        else:
            '''filename = "ClosingShoesandJewelry" + "_" + str(metadata["asin"])
            request.urlretrieve(metadata["imUrl"],"/media/sina/Daten/AmazonRS/dataset/1/"+ filename)
            print("Downloaded second...!")'''
            continue

        
    return print(adress)
    

                

def main():
    args = get_args()
    print("first place...")
    image_url = get_the_URL()
    print("second place...")

    # save into database
    '''client = MongoClient("mongodb+srv://Sina:Sbsb+6839@amazon.dinmb.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.amazon
    collection = db.image_urls
    data = collection.insert(image_url)'''

    logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info("hello")

if __name__ == '__main__':
    main()

