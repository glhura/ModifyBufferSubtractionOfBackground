#!/usr/bin/env python
import os
import argparse

#This function looks through the directory for anything with a .dat extension and assumes this is the input
def IdenDatFiles(dir_name): 
    file_list = []
    directory_content_list = os.listdir(dir_name)
    file_list = list((os.path.join(dir_name, list_item) for list_item in directory_content_list if (str(list_item).endswith('.dat') and "Ave" not in list_item)))
    file_list.sort(key=lambda dat_file_1: int((str(os.path.basename(dat_file_1)).split('.')[0]).split('_')[-1]))

    return file_list

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='This code creates a list of .dat files in a given folder')
    parser.add_argument("DirName", help = 'Need a Directory Name Profile')
    args = parser.parse_args()
    MAINACTION = IdenDatFiles(args.DirName)
    print(MAINACTION)
