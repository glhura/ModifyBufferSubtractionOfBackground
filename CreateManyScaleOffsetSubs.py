#!/usr/bin/env python
"""This program runs the FindFactorForSubtraction over a range of desired values and Averages the resulting folders"""

import sys
import argparse
import os
import numpy as np

import FindFactorForSubtractionAtHighQ
import AveRangeFrames
import IdenDatFiles

def create_many_subtractions(sample_folder_name, buffer_folder_name, ValueMin, ValueMax, ValueInt, qmin, qmax, method_pick):
    float_valmin = float(ValueMin)
    float_valmax = float(ValueMax)
    float_valint = float(ValueInt)
    
    num_to_create = int ((float_valmax - float_valmin)/float_valint)
    
    value = float_valmin
    for i in range (0, num_to_create):
        print (value)
        new_dir = FindFactorForSubtractionAtHighQ.offset_folder_subtraction(sample_folder_name, buffer_folder_name, value, qmin, qmax, method_pick)
        new_dats = IdenDatFiles.IdenDatFiles(sample_folder_name)
        num_dats = len(new_dats) - 1
        ave_name = AveRangeFrames.ave_files_in_fold(new_dir, 1, num_dats, 1)
        new_name = sample_folder_name + "_" + str(value) + ".dat"
        os.rename(ave_name,new_name)
        value = value + float_valint


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="This code needs two folders, a value and a qmin and qmax")
    parser.add_argument("sample_folder_name", help = 'Need Two Folders, A Value to match, Qmin and Qmax')
    parser.add_argument("buffer_folder_name", help = 'Need Two Folders, A Value to match, Qmin and Qmax')
    parser.add_argument("ValueMin", help = 'Need Two Files, A ValueMin to match, Qmin and Qmax')
    parser.add_argument("ValueMax", help = 'Need Two Files, A ValueMax to match, Qmin and Qmax')
    parser.add_argument("ValueInt", help = 'Need Two Files, A ValueInterval to match, Qmin and Qmax')
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
    mainaction = create_many_subtractions(args.sample_folder_name, args.buffer_folder_name, args.ValueMin, args.ValueMax, args.ValueInt, args.qmin, args.qmax, method_pick)