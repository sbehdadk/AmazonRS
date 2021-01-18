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
from os import listdir
import itertools
import cv2
import os
import shutil


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

def first_step_categorising(folder):
    print('start of categorising folders...!!!')
    #categories = []
    sub_category = []
    asin = []
    j = 0
    labelList = []  # List of class tags
    datasetList = listdir(folder)
    #print(datasetList)
    datasetLength = len(datasetList)  # Number of files in the folder
    print(datasetLength)
    for i in range(datasetLength):
        filename = datasetList[i]  # Get the file name string

        if "]," in filename:
            categ = filename.split(']')[-1]  # Extract the file name by ]
            category = categ.split(",")[-2]
            labelList.append(category)

        elif len(filename.split(',')) >= 2:
            category = filename.split(',')[-2]
            labelList.append(category)
        elif len(filename.split(',')) < 2:
            category = filename.split('_')[0]
            labelList.append(category)
        else:
            continue
            
            #print("not enough categories...!!!"))
    #print("number of false categories: " + str(j))
        #print("end of categ name")

    labelList.sort()
    final_list = list(labelList for labelList,_ in itertools.groupby(labelList)) #remove duplicate items in a list of list
    print("number of categories: " + str(len(final_list)))
    print("categorising is done!")
    #print(final_list)
    #print(len(final_list))

    #print(asin)
    return final_list

def transfer_to_folders(final_list, root_path):
    print("start of transfering into the folders...!!!")
    #list_filename = listdir(root_path)
    k = 0
    list_filename = [] 
    for file_name in os.scandir(root_path):
        if file_name.is_dir():
            k += 1
        else:
            list_filename.append(file_name.name)

    print(len(list_filename))
    print(len(final_list))
    #print(final_list)

    for folder in final_list:   #create folders related to categories
        if not folder:
            print("folder name is empty")
        else:

            if not os.path.isdir(os.path.join(root_path, str(folder))):
                os.mkdir(os.path.join(root_path,str(folder)))
            else:
                continue
            for image in list_filename:     #copy files into related folder categories
                file_path = root_path + image
                dest_dir = root_path + str(folder)
                
                #if folder in image:
                if str(folder) in image:
                    shutil.copy2(file_path, os.path.join(dest_dir, image))
                    #shutil.move(file_path, os.path.join(dest_dir, image))
                    #list_filename.remove(image)
                else:
                    continue
            print("copy files into folders is done!")
    print("copying into created folders is done!")   


def remove_remain_images(root_path):
    print("start of removing images...!!!")
    for path in os.listdir(root_path):  #remove files but not sub_folders
        full_path = os.path.join(root_path, path)
        if os.path.isfile(full_path):
            os.remove(full_path)
    print("removing all the images in root folder is done!")


def categorise_sub_categories(root_path):
    print("start of sub_foldering...!!!")
    #list_of_folders = ['AccessoryKits', 'Batteries', 'Covers']
    
    '''list_of_folders = ['Electronics, Accessories & Supplies, Audio & Video Accessories, Cables & Interconnects',
                       'Electronics, Computers & Accessories, Touch Screen Tablet Accessories',
                       'Electronics, Accessories & Supplies, Audio & Video Accessories, Cables & Interconnects, Video Cables']'''
    list_of_folders = [] 
    for folder_name in os.scandir(root_path):
        if folder_name.is_dir():
            list_of_folders.append(folder_name.name)
    print(len(list_of_folders))
    #list_of_folders = listdir(root_path)
    #print(len(list_of_folders)) #list of folder's name
    #print(list_of_folders)
    for i in range(len(list_of_folders)):
        final_list = []
        asins = []
        label_list = []
        name_list = []          #define lists in for loop for avoiding duplicated in the appended lists
        j = 0

        temp_path = root_path + list_of_folders[i] + "/"
        #print(temp_path)
        list_of_files = listdir(temp_path) #list of files into the folder
        print(len(list_of_files))
        for data in list_of_files: 
            #print(data)
            if "]" in data:
                if "_" in data:
                    data_split = data.split('[')[-1]
                    categ_and_asin = data_split.split(',')[-1]
                    category = categ_and_asin.split('_')[0]
                    asin = categ_and_asin.split('_')[1]
                    #categ_name = data_split.split(',')[4:-1]
                    #print(categ_name)
                    
                    only_name = category + '_' + str(asin)
                    
                    label_list.append(category)
                    name_list.append(only_name)
                    asins.append(asin)
                    os.rename(temp_path + data , temp_path + only_name)
                    j += 1
                else:
                    continue
            else:
                data_with_asi = data.split(',')[-1]
                category = data_with_asi.split('_')[0]
                asin = data_with_asi.split('_')[1]
                only_name = category + "_" + str(asin)
                asins.append(asin)
                name_list.append(only_name)
                label_list.append(category)
                os.rename(temp_path + data , temp_path + only_name)
                j += 1

        label_list.sort()
        final_list = list(label_list for label_list,_ in itertools.groupby(label_list)) #remove duplicate items in a list of list
        list_of_renamed_files = listdir(temp_path)
        print("All Images renamed and Sub_categories are listed...!!!")


        for folder in final_list:   #create folders related to categories
            if not folder:
                print("folder name is empty")
            else:
                if not os.path.isdir(os.path.join(temp_path, str(folder))):
                    os.mkdir(os.path.join(temp_path,str(folder)))
                #print(list_of_files)
                for image in list_of_renamed_files:     #copy files into related folder categories
                    #print(temp_path)
                    file_path = temp_path +  image
                    dest_dir = temp_path + str(folder)
                    #print(file_path)
                    #print(dest_dir)
                    if str(folder) in image:
                        shutil.copy2(file_path, os.path.join(dest_dir, image))
                        #shutil.move(file_path, os.path.join(dest_dir, image))
                        #list_of_renamed_files.remove(image)
        print("sub categories are created ...!!!")

        remove_remain_images(temp_path)
        print("remove remained images from sub_category...!!!")     
        '''for path in os.listdir(temp_path):  #remove files but not sub_folders
            full_path = os.path.join(temp_path, path)
            if os.path.isfile(full_path):
                os.remove(full_path)
        print("all duplicated files are removed...")'''


def one_level_categorising(root_folder):
    
    categories = []
    asins = []
    labelList = []  # List of class tags
    datasetList = listdir(root_folder)
    print(datasetList)
    '''datasetLength = len(datasetList)  # Number of files in the folder
    print(datasetLength)

    for i in range(datasetLength):
        filename = datasetList[i]  # Get the file name string

        split_by_coma = filename.split(',')
        category = split_by_coma[-1].split('_')[0]
        asin = split_by_coma[-1].split('_')[1]
        only_name = category + "_" + str(i) + "_" + asin
        categories.append(category)    
        asins.append(asin)
        os.rename(root_folder + filename , root_folder + only_name)

    categories.sort()
    final_list = list(categories for categories,_ in itertools.groupby(categories)) #remove duplicate items in a list of list    label_list.sort()'''

    return final_list, asins


    
def main():
    #folder = "/media/sina/Daten/AmazonRS/dataset/Electronics/"
    #folder = "/media/sina/Daten/Amazon_dataset/Electronics/"
    folder = "/home/sina/Desktop/images_evaluation/"
    #for folder in folders:
        #labelList, final_list, asin = local_categorising(folder)  #first level categorising
        #move_to_newfolder_categories(final_list, folder)   #move images into related categories
    #final_list, asin = one_level_categorising(folder)    
    #final_list = first_step_categorising(folder)
    #transfer_to_folders(final_list, folder)
    #remove_remain_images(folder)
    one_level_categorising(folder)
    #categorise_sub_categories(folder)  #classifing one step deeper into sub_categories
    print("Categorising is done...!!!")


if __name__=='__main__':
    main()


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



def local_categorising(folder):
    #categories = []
    sub_category = []
    asin = []
    labelList = []  # List of class tags
    datasetList = listdir(folder)
    #print(datasetList)
    datasetLength = len(datasetList)  # Number of files in the folder
    print(datasetLength)
    for i in range(datasetLength):
        filename = datasetList[i]  # Get the file name string
        categories = []

        for j in range(len(filename.split(']'))):
            category = filename.split(', [')[j]  # Extract the file name by.
            #print("main category is: " +category)
            if j == len(filename.split(']')) -1:
                #print("this is the last iteration")
                #print(category)
                if "_" in category:
                    asi = category.split('_')[1]
                    category = category.split('_')[0]
                    #print(category)
                    asin.append(asi)
                    categories.append(category)
                else:
                    continue
            else:
                continue
            '''for k in range(len(category.split(','))):
                print(len(category.split(',')))
                sub_category = category.split(',')[k]  # Extract category number by _ segmentation
                labelList.append(sub_category)
                print("sub category is: " +sub_category)'''
        #print(categories)
        #print(categories[-1].split('_')[0])
        #categoriess = categories.replace(categories[-1], categories[-1].split('_')[0])

        labelList.append(categories)
    #print(labelList)
    #print(len(labelList))
    labelList.sort()
    final_list = list(labelList for labelList,_ in itertools.groupby(labelList)) #remove duplicate items in a list of list
    print("categorising is done!")

    return labelList, final_list, asin

def move_to_newfolder_categories(final_list, root_path):
    list_filename = listdir(root_path)
    print(len(final_list))
    #print(final_list)

    for folder in final_list:   #create folders related to categories
        if not folder:
            print("folder name is empty")
        else:
            #print(folder)
            folder1 = str(folder)[2:-2] 
            #print(folder1)
            if not os.path.isdir(os.path.join(root_path, folder1)):
                os.mkdir(os.path.join(root_path,str(folder1)))
            
            for image in list_filename:     #copy files into related folder categories
                file_path = root_path + image
                dest_dir = root_path + folder1
                #print(file_path)
                #print(dest_dir)
                if folder1 in image:
                    shutil.copy2(file_path, os.path.join(dest_dir, image))
            print("copy files into folders is done!")
    print("copying into created folders is done!")     
    for path in os.listdir(root_path):  #remove files but not sub_folders
        full_path = os.path.join(root_path, path)
        if os.path.isfile(full_path):
            os.remove(full_path)
    print("removing all the images in root folder is done!")


