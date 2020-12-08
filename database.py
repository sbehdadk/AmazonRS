from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from mysql.connector import MySQLConnection, Error
import MySQLdb
import mysql.connector
import matplotlib.pyplot as plt
import matplotlib as mlp
import logging
from sqlalchemy.types import Integer, Text, String, DateTime
import pymysql
import json

class create_database:
    def __init__(self, database, table, col, val, datafra):
        self.database = database
        self.table = table
        self.col = col
        self.val = val
        self.datafra = datafra
        
    def set_table(self):
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Sina 6839",
            database=self.database,
            auth_plugin="mysql_native_password"
            )

        table_variables = "CREATE TABLE IF NOT EXISTS dictionaries( product_ID CHAR(100), sub_categories CHAR(100)"

        logging.debug("before inserting into asin_category table...")

        insert_values = """INSERT INTO dictionaries(product_ID, sub_categories) VALUES (%s, %s)"""

        mycursor = mydb.cursor()
        #mycursor.execute("DROP database IF EXISTS amazon")
        #mycursor.execute("CREATE database amazon")
        mycursor.execute("USE amazon")
        #mycursor.execute("DROP table IF EXISTS dictionaries")
        #mycursor.execute(table_variables)

        asin_dict = dict(zip(self.col, self.val))
        
        for mydict in asin_dict:
            placeholders = ', '.join(['%s'] * len(asin_dict))
            colum = ', '.join("`" + str(x).replace('/', '_') + "`" for x in mydict.keys())
            valu = ', '.join("'" + str(x).replace('/', '_') + "'" for x in mydict.values())
            columns = json.dumps(colum)
            values = json.dumps(valu)
            sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('categories', columns, values)
            # print(sql)

        logging.debug("middle of set_table...")
        #logging.debug(asin_category_dict)
        '''for index, row in self.datafra.iterrows():
            mycursor.execute(insert_values, (row['product_ID'], row['sub_categories']))'''


        #mycursor.execute(insert_values, asin_category_dict.keys(), asin_category_dict.values())
        #mycursor.execute(insert_values)

        mydb.commit()

        logging.debug("End of Set_Table...")        
        mydb.close()


def insert_dataframe(dataframe, table_name):

    engine = create_engine('mysql://root:Sina 6839@127.0.0.1:3306/amazon') #change to connect your mysql
    logging.debug("after creating the database...")
    #if you want to append the data to an existing table
    #dataframe.to_sql(name=new_name, con=engine, if_exists='append',index=False) 

    #if you want to create a new table 
    dataframe.to_sql(name=table_name, con=engine, if_exists='replace', index=False, chunksize=5000)

    logging.debug("End of inserting DataFrame...")


    def query_data(self):
        rows = []
        colus = []
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Sina 6839",
            database=self.database,
            auth_plugin="mysql_native_password"
            )

        db_cursor = db.cursor()
        db_cursor.execute("USE amazon")

        query = ("SELECT * FROM dictionaries")        
        
        db_cursor.execute(query)
        records = db_cursor.fetchall()
        for row, colu in records:
            rows.append(row)
            colus.append(colu)

        db_cursor.close()

        return rows, colus

    def visualise_dframe(self, row, col):
        df = pd.DataFrame({
            "asin":row,
            "categories":col
        })

        df.plot(x="asin", y="categories", kind="barh", figsize=(35,35))
        plt.title("dictionary of asin and related categories")
        plt.ylabel("asin")
        plt.xlabel("related categories")

        plt.savefig("dic_asin_categorie.jpg")
        plt.show()
