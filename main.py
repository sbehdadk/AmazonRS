from __future__ import absolute_import, division, print_function, unicode_literals
from data_preprocessing import categorising 
from database import create_database
import logging
import pandas as pd
import gzip
import array
import argparse
import matplotlib.pyplot as plt
import logging
import os
import tensorflow as tf
from tensorflow import keras
import random
import string
from keras import backend as K
import pandas as pd

logging.basicConfig(level=logging.DEBUG)


def get_args():
    parser = argparse.ArgumentParser(description="This script trains the CNN model for age and gender estimation.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--dataset_path", type=str, required=False,
                        default='dataset/image_features.b', help="path to binary file")
    parser.add_argument("--database", type=str, default="amazon",
                        help="database_name")
    parser.add_argument("--tablename", type=str, default='variables',
                        help="name of the table")
    '''parser.add_argument("--validation_split", type=float, default=0.2,
                        help="validation split ratio")
    parser.add_argument("--patience", type=int, default=6,
                        help="patience_epochs")'''
    args = parser.parse_args()
    return args


def main():   
    args = get_args()
    logging.debug("first step...")

    asin_categ, asin, categ, categ_name = categorising()
    
    '''if args.tablename:
        database = create_database(database=args.database, table=args.tablename, col=asin, val=categ)
        database.set_table()
        database.insert_dataframe(dataframe=asin_categ, new_name=categ_name)'''

    logging.debug("This is the query data from the Database...")

    logging.debug("This is the final DataFrame...")

    logging.debug("This is the end of the process ...")
    #logging.getLogger('matplotlib.font_manager').disabled = True


if __name__ == "__main__":
    main()