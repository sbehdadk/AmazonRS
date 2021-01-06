from os import listdir
import shutil
import os



def main():
    path = '/media/sina/Daten/AmazonRS/dataset/Electronics/images_evaluation'
    list_name = listdir(path)
    print(len(list_name))

    for j in range(len(list_name)):
        parent_folder_name = list_name[j]
        print(parent_folder_name)
        delete_folders = []

        for i in range(len(listdir(path + '/' + parent_folder_name))):
            print(len(listdir(path + '/' + parent_folder_name)))
            list_subdir = listdir(path + '/' + parent_folder_name)
            print("list_subdir:" + list_subdir[i])
            folder_name = list_subdir[i]
            number = listdir(path + '/' + parent_folder_name + '/' + folder_name)
            print("number of images :" + str(len(number)))

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



if __name__ == '__main__':
    main()