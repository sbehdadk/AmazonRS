import pandas as pd
import gzip
import array
import numpy as np
import json
import gzip
import ast, gzip, json
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from database import create_database
from database import insert_dataframe


logging.basicConfig(level=logging.DEBUG)


def parse(path):
    g = gzip.open(path, 'rb')
    for l in g:
        yield eval(l)
        #yield json.dumps(eval(l))

def getDF(path):
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1 
    return pd.DataFrame.from_dict(df, orient='index')


def computing(source):
    cat = []
    for re in parse(source):
        if "categories" in re:
            cat.append(re['categories'])
        else:
            continue
    print(cat)


def categorising():
    metadata_list = ["meta_Amazon_Instant_Video.json.gz", "meta_Apps_for_Android.json.gz", "meta_Automotive.json.gz", "meta_Baby.json.gz", "meta_Beauty.json.gz", 
                    "meta_Books.json.gz", "meta_CDs_and_Vinyl.json.gz", "meta_Cell_Phones_and_Accessories.json.gz", "meta_Clothing_Shoes_and_Jewelry.json.gz",
                    "meta_Digital_Music.json.gz", "meta_Electronics.json.gz", "meta_Grocery_and_Gourmet_Food.json.gz", "meta_Health_and_Personal_Care.json.gz",
                    "meta_Home_and_Kitchen.json.gz", "meta_Kindle_Store.json.gz", "meta_Movies_and_TV.json.gz", "meta_Musical_Instruments.json.gz", 
                    "meta_Office_Products.json.gz", "meta_Patio_Lawn_and_Garden.json.gz", "meta_Pet_Supplies.json.gz", "meta_Sports_and_Outdoors.json.gz", 
                    "meta_Tools_and_Home_Improvement.json.gz", "meta_Toys_and_Games.json.gz", "meta_Video_Games.json.gz"]
    x = 0
    cluster_dic = {}
    dici = []
    amount = []


    for x in range(len(metadata_list)):
    #for x in range(1):
        dframe = getDF("/media/sina/Daten/AmazonRS/dataset/" + metadata_list[x]) 
        #dframe = getDF("/media/sina/Daten/AmazonRS/dataset/meta_Automotive.json.gz")
        #meta_df = pd.read_json(dframe)
        logging.debug("print the head of dataset : ")
        frame_columns = dframe.columns.tolist()

        categ = []
        asin = []
        asin_categ = []
        category_name = str(metadata_list[x])[:-8]
        logging.debug(category_name)
        logging.debug(dframe.shape)


        #[categ.append([d[i][j]]) for d in dframe["categories"] for i in range(len(d)) for j in range(len(d[i]))]
        #[categ.append(d[i]) for d in dframe["categories"] for i in range(len(d)) for j in range(len(d[i]))]
        #[related.append(m[i]) for m in dframe["related"] for i in range(2) if type(m) is not float]
        logging.debug(dframe.head())
        
        if 'imUrl' in dframe:
            dframe = dframe.drop("imUrl", axis=1)
        else:
            dframe = dframe

        logging.debug("end of URL...")
        
        logging.debug(dframe.shape)
        '''product_Dataframe = pd.DataFrame(list(zip(frame_data)),
                            columns=frame_columns)'''
 
        #logging.debug(product_Dataframe.head())
        """
        #dicte = [categ.count(summerize[m]) for m in range(len(summerize))]  #amount of sub categories
        item_category = {key: value for key, value in zip(asin, categ)}
        #logging.debug(item_category)
        logging.debug(len(item_category.keys()))
        logging.debug(len(item_category.values()))
        #asin_categ = pd.DataFrame.from_dict(item_category, orient='index')
        asin_categ = pd.DataFrame(list(item_category.items()), columns=['product_ID', 'sub_categories'])
        asin_categ = asin_categ.transpose()
        asin_categ = asin_categ.T
        #logging.debug(asin_categ)
        logging.debug(asin_categ.shape)
        #logging.debug(item_category)
        logging.debug("before create database...")"""

        #database = create_database(database="amazon", table=category_name + "_table", col=asin, val=categ, datafra=asin_categ)
        #database.set_table()
    
        logging.debug("the category name is :" + category_name)
        #insert_dataframe(dataframe=asin_categ, table_name=category_name)
        #asin_categ.to_csv(r'/media/sina/Daten/AmazonRS/dataset/CSV/' + category_name +'.csv', index=False)
        dframe.to_csv(r'/media/sina/Daten/AmazonRS/dataset/CSV/' + category_name +'.csv', index=False)
        logging.debug("")
        logging.debug("dataFrame is saved ...")


    #logging.debug(asin_categ.items())
    #logging.debug(asin_categ)
    return asin_categ, asin, categ, category_name


