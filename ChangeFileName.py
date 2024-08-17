#!/usr/bin/env python
"""Purpose of this program is to manipulate
an incoming file name and change it so that
it has a new extension or will keep original one.
Written with the intended purpose of changing
 .cbf files into .sub.cbf files"""

import argparse


def ChangeName(file_name,mod,keep_orig_flag):
    """This is the buisness end of this function"""
    #print(file_name,mod,keep_orig_flag)
    orig_flag = int(keep_orig_flag)
    name_length = len(file_name)
    str1 = "."
    last_dot= file_name.rfind(str1)
    #print(last_dot)
    where_to_cut=name_length - last_dot
    trouble = file_name[(name_length - where_to_cut):(name_length)]
    #print(trouble)
    first_file_root = file_name[:-4]
    #CurrentFileExtension
    if orig_flag == 0:
        new_file_name = (first_file_root+"."+mod)
    if orig_flag == 1:
        new_file_name = (first_file_root+"."+mod+trouble)
    #print(new_file_name)
    return new_file_name

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='This takes the name of a file as input')
    parser.add_argument("file_name", help = 'Need File to Work On')
    parser.add_argument("mod", help = 'Need Extension You Want to Add')
    parser.add_argument("--KeepOrig", action = "store_true", help = "KeepsLast4")
    args = parser.parse_args()
    KEEP_ORIG_FLAG = 0
    if args.KeepOrig:
        KEEP_ORIG_FLAG = 1
    MAINACTION = ChangeName(args.file_name, args.mod, KEEP_ORIG_FLAG)
