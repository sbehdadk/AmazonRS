'''import sys
import numpy as np
from matplotlib.pyplot import imread
import cv2
import pickle
import os
import matplotlib.pyplot as plt

"""Script to preprocess the omniglot dataset and pickle it into an array that's easy
    to index my character type"""
    
data_path = os.path.join('/home/sina/Desktop/omniglot/')
train_folder = os.path.join(data_path,'images_background')
valpath = os.path.join(data_path,'images_evaluation')

data_path = os.path.join('/home/sina/Desktop/d/jk')
train_folder = os.path.join(data_path,'b')
valpath = os.path.join(data_path,'m')

save_path = '/home/sina/Desktop/data/'

lang_dict = {}



def preprocess_input(x, v2=True):
    x = x.astype('float32')
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x

def loadimgs(path,n = 0):
    
    path => Path of train directory or test directory
    
    X=[]
    y = []
    cat_dict = {}
    lang_dict = {}
    curr_y = n
    # we load every alphabet seperately so we can isolate them later
    for alphabet in os.listdir(path):
        print("loading Product's Category: " + alphabet)
        lang_dict[alphabet] = [curr_y,None]
        alphabet_path = os.path.join(path,alphabet)
        # every letter/category has it's own column in the array, so  load seperately
        for letter in os.listdir(alphabet_path):
            cat_dict[curr_y] = (alphabet, letter)
            category_images=[]
            letter_path = os.path.join(alphabet_path, letter)
            # read all the images in the current category
            for filename in os.listdir(letter_path):
                image_path = os.path.join(letter_path, filename)
                image = cv2.imread(image_path, cv2.IMREAD_COLOR)
                image = cv2.resize(image, (150,150))
                
                #im=image.astype('float32')
                #image = cv2.normalize(im,None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
                #print("type of image:{}".format(image.size))

                #image = cv2.imread(image_path)
                #image = cv2.resize(image, (224,224))
                category_images.append(image)
                y.append(curr_y)
            try:
                X.append(np.stack(category_images))
            # edge case  - last one
            except ValueError as e:
                print(e)
                print("error - category_images:", category_images)
            curr_y += 1
            lang_dict[alphabet][1] = curr_y - 1
    y = np.vstack(y)
    X = np.stack(X)
    #X = preprocess_input(X)
    return X,y,lang_dict

X,y,c=loadimgs(train_folder)
print("shape of X1: {}".format(X.dtype))

with open(os.path.join(save_path,"train.pickle"), "wb") as f:
	pickle.dump((X,c),f)
#print("shape of X2: {}".format(X.shape))

Xval,yval,cval=loadimgs(valpath)

#X,y,c=loadimgs(valpath)
with open(os.path.join(save_path,"val.pickle"), "wb") as f:
	pickle.dump((Xval,cval),f)

print("shape of Xval: {}".format(Xval.dtype))'''



import sys
import numpy as np
from matplotlib.pyplot import imread
import pickle
import os
import matplotlib.pyplot as plt

"""Script to preprocess the omniglot dataset and pickle it into an array that's easy
    to index my character type"""

data_path = os.path.join('/home/sina/Desktop/omniglot/')
train_folder = os.path.join(data_path,'images_background')
valpath = os.path.join(data_path,'images_evaluation')

save_path = '/home/sina/Desktop/data/'

lang_dict = {}



def loadimgs(path,n=0):
    #if data not already unzipped, unzip it.
    if not os.path.exists(path):
        print("unzipping")
        os.chdir(data_path)
        os.system("unzip {}".format(path+".zip" ))
    X=[]
    y = []
    cat_dict = {}
    lang_dict = {}
    curr_y = n
    #we load every alphabet seperately so we can isolate them later
    for alphabet in os.listdir(path):
        print("loading alphabet: " + alphabet)
        lang_dict[alphabet] = [curr_y,None]
        alphabet_path = os.path.join(path,alphabet)
        #every letter/category has it's own column in the array, so  load seperately
        for letter in os.listdir(alphabet_path):
            cat_dict[curr_y] = (alphabet, letter)
            category_images=[]
            letter_path = os.path.join(alphabet_path, letter)
            for filename in os.listdir(letter_path):
                image_path = os.path.join(letter_path, filename)
                image = imread(image_path)
                category_images.append(image)
                y.append(curr_y)
            try:
                X.append(np.stack(category_images))
            #edge case  - last one
            except ValueError as e:
                print(e)
                print("error - category_images:", category_images)
            curr_y += 1
            lang_dict[alphabet][1] = curr_y - 1
    y = np.vstack(y)
    X = np.stack(X)
    return X,y,lang_dict

X,y,c=loadimgs(train_folder)


with open(os.path.join(save_path,"train.pickle"), "wb") as f:
	pickle.dump((X,c),f)


X,y,c=loadimgs(valpath)
with open(os.path.join(save_path,"val.pickle"), "wb") as f:
	pickle.dump((X,c),f)