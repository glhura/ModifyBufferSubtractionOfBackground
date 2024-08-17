#!/usr/bin/env python
"""This program optimizes the subtraction of two folders to create a subtracted folder"""
"""The subtracted folder will set dats to a q region to an input value"""

import sys
import argparse
import os
import numpy as np

"""These are custom code"""
import AdjustBufferSubtraction
import IdenDatFiles
import SubtTwoFoldScalAndBack


def offset_folder_subtraction(sample_folder_name, buffer_folder_name, Value, qmin, qmax, method_pick):
    SampNames = IdenDatFiles.IdenDatFiles(sample_folder_name)
    BuffNames = IdenDatFiles.IdenDatFiles(buffer_folder_name)
    num_files_samp = len(SampNames)
    num_files_buff = len(BuffNames)
    
    """Some proofing of directories, same number of files etc. """
    if num_files_samp != num_files_buff:
        print("Folders Have Different Num Files")
        sys.exit()
    if num_files_samp < 1:
        print("Folders Dont have dat files")
        sys.exit() 
        
    """Hope for at least 11 files to work with""" 
    hope_for = 10
    if num_files_samp < hope_for:
        print("Folder has very few files")
        hope_for = num_files_samp

    scales = np.zeros(hope_for)
    backgrounds = np.zeros(hope_for)

    """Calcluate results for first 10 files"""
    for i in range(1, hope_for+1):
        sub_output = AdjustBufferSubtraction.offset_subtraction(SampNames[i],BuffNames[i], Value, qmin, qmax,0, method_pick)
        scales[i-1] = sub_output[0]
        backgrounds[i-1] = sub_output[1]
    print(scales)
    
    """Average Results"""
    final_scale = 1/np.mean(scales)
    final_background = np.mean(backgrounds)
    
    """Apply the corrections"""
    new_dir = SubtTwoFoldScalAndBack.Over_Sub_And_Back(sample_folder_name, 1.0, buffer_folder_name, final_scale, final_background)
             
    return(new_dir)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="This code needs two folders, a value and a qmin and qmax")
    parser.add_argument("sample_folder_name", help = 'Need Two Folders, A Value to match, Qmin and Qmax')
    parser.add_argument("buffer_folder_name", help = 'Need Two Folders, A Value to match, Qmin and Qmax')
    parser.add_argument("Value", help = 'Need Two Files, A Value to match, Qmin and Qmax')
    parser.add_argument("qmin", help = 'Need Two Files, A Value to match, Qmin and Qmax')
    parser.add_argument("qmax", help = 'Need Two Files, A Value to match, Qmin and Qmax')
    parser.add_argument("--scale", action = "store_true", help = "Scaling Buffer for Result")
    parser.add_argument("--offset", action = "store_true", help = "Using an Offset for Result")
    parser.add_argument("--both", action = "store_true", help = "Using both a Scale Factor And An Offset")
    args = parser.parse_args()
    method_pick = 1
    if args.scale:
        method_pic = 1
    if args.offset:
        method_pick = 2
    if args.both:
        method_pick = 3   
    mainaction = offset_folder_subtraction(args.sample_folder_name, args.buffer_folder_name, args.Value, args.qmin, args.qmax, method_pick)