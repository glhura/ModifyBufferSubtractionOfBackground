#!/usr/bin/env python
"""This code averages the range of frames you specify given a folder's name"""
import sys
import argparse
import os
import numpy as np

import OpenScatFile
import ChangeFileName
import IdenDatFiles
import PrintScatClass

def ave_files_in_fold(folder, first_frame, last_frame, WRITE_TO_FILE):
    first_frame = int(first_frame)
    last_frame = int(last_frame)
    if first_frame > last_frame:
        print("Hey! First Frame must be smaller than Last Frame")
        raise SystemExit()
    num_frames = (last_frame - first_frame) + 1
    if num_frames < 1:
        print("Hey! Need more Frames")
        raise SystemExit()
    top_dir = os.getcwd()
    working_dir = os.path.join(top_dir,folder)
    all_files = IdenDatFiles.IdenDatFiles(working_dir)
    #print(all_files)
    ave_vec = OpenScatFile.OpenScatFile(all_files[first_frame])
    for i in range(first_frame+1, last_frame+1):
        curr_vec = OpenScatFile.OpenScatFile(all_files[i])
        ave_vec.I_values = ave_vec.I_values + curr_vec.I_values
        ave_vec.E_values = ave_vec.E_values + curr_vec.E_values
    
    ave_vec.I_values = ave_vec.I_values/num_frames
    ave_vec.E_values = ave_vec.E_values/num_frames
    
    std_vec = ave_vec.E_values*0
    #print (std_vec)
    if num_frames > 5:
        for i in range(first_frame+1, last_frame+1):
            curr_vec = OpenScatFile.OpenScatFile(all_files[i])
            std_vec = std_vec + (ave_vec.I_values - curr_vec.I_values)*(ave_vec.I_values - curr_vec.I_values)
        std_vec = std_vec/(num_frames - 1)
        numpoints = len(std_vec)
        for i in range(0,numpoints):
            std_vec[i] = np.sqrt(std_vec[i])
        ave_vec.E_values = std_vec
        #print(std_vec)

    string_to_change = str(first_frame) + "to" + str(last_frame)
    print(string_to_change)
    
    new_name = ChangeFileName.ChangeName(all_files[first_frame], string_to_change, 1)
    split_new_name = os.path.split(new_name)
    new_name = split_new_name[1]
    
    PrintScatClass.PrintQ_I_Eclass(ave_vec.q_values, ave_vec.I_values, ave_vec.E_values, new_name)
    
    if(WRITE_TO_FILE == 1):
        return new_name
    else:
        return(new_name,ave_vec)
     
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='This takes the name of a file as input')
    parser.add_argument("folder", help = 'folder where data is')
    parser.add_argument("first_frame", help = 'frame number to start with')
    parser.add_argument("last_frame", help = 'last frame you want in the average')
    parser.add_argument("--file", action = "store_true", help = "Will Print Results of Analysis to Screen")
    args = parser.parse_args()
    WRITE_TO_FILE = 0
    if args.file:
        print("you want this printed to a file")
        WRITE_TO_FILE = 1

    MAINACTION = ave_files_in_fold(args.folder, args.first_frame, args.last_frame, WRITE_TO_FILE)
