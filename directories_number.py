from os import listdir
import shutil
import os
import cv2
from PIL import Image
from glob import glob                                                           


def main():
    path = '/home/sina/Desktop/images_evaluation'
    #path = '/home/sina/Desktop/images_background'

    list_name = listdir(path)
    #print(len(list_name))

    for j in range(len(list_name)):
        parent_folder_name = list_name[j]
        #print(parent_folder_name)
        delete_folders = []

        for i in range(len(listdir(path + '/' + parent_folder_name))):
            #print(len(listdir(path + '/' + parent_folder_name)))
            list_subdir = listdir(path + '/' + parent_folder_name)
            #print("list_subdir:" + list_subdir[i])
            folder_name = list_subdir[i]
            number = listdir(path + '/' + parent_folder_name + '/' + folder_name)
            #print("number of images :" + str(len(number)))

            if len(number) < 20:
                delete_folders.append(folder_name)
            elif len(number) > 20:
                rest = len(number) - 20
                for file in number[:rest]:
                    os.remove(path + '/' + parent_folder_name + '/' + folder_name + '/' + file)
            else:
                continue
        for m in delete_folders:
            shutil.rmtree(path + '/' +parent_folder_name + '/' + m)

        #if len(os.listdir(path + '/' + parent_folder_name)) == 0: # Check is empty..
            #shutil.rmtree(path + '/' + parent_folder_name)


    '''path = "/home/sina/Desktop/Dataset/images_evaluation" 
    list_name = listdir(path)
    print(len(list_name))

    for j in range(len(list_name)):
        parent_folder_name = list_name[j]
        print(parent_folder_name)

        for i in range(len(listdir(path + '/' + parent_folder_name))):
            #print(len(listdir(path + '/' + parent_folder_name)))
            list_subdir = listdir(path + '/' + parent_folder_name)
            #print("list_subdir:" + list_subdir[i])
            folder_name = list_subdir[i]
            dir = path + '/' + parent_folder_name + '/' + folder_name
            dirs = listdir(dir)
            #print("number of images :" + str(len(dirs)))
            #print("dir: " + dir)

            for item in dirs: #Iterates through each picture
                if os.path.isfile(dir + "/" + item): 
                    im = cv2.imread(dir + "/" + item, cv2.IMREAD_UNCHANGED)
                    #im = cv2.cvtColor(colorimage, cv2.COLOR_BGR2GRAY)
                    print("original size of image:" + str(im.shape))

                    im = Image.open(dir + "/" + item)
                    print("type of image:" + str(type(im)))
                    #print("size of image:" + str(im.size))
                    #f, e = os.path.splitext(dir + "/" + item)
                    #imResize = im.resize((105,105), Image.ANTIALIAS)
                    #imResize.save(f + ' resized.jpg', 'JPEG', quality=90)
                    #formats = Image.open(dir + "/" + item)
                    width = 105
                    height = 105
                    dim = (width, height)
                    if im.size != dim:
                        resized = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)
                    else:
                        continue
                    print("resized size of image:" + str(resized.shape))
                else:
                    print("error")'''



if __name__ == '__main__':
    main()