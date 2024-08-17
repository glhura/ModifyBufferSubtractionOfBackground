#!/usr/bin/env python
import os
import argparse
import sys

import IdenDatFiles
import SubTwoScaledDatsAndBack

"""Goes through a folder and applies given scale factors for sample and buffer"""
"""Also allows for the application of a background"""

def Over_Sub_And_Back(SampDirName, SampScale, BuffDirName, BufScale, BackFactor):
    float_samp = float(SampScale)
    float_buff = float(BufScale)
    float_back = float(BackFactor)
    
    SampNames = IdenDatFiles.IdenDatFiles(SampDirName)
    BuffNames = IdenDatFiles.IdenDatFiles(BuffDirName)
    #print(SampNames)
    
    """Mostly Works hard on making a name for new folder and files"""
    samp_full = SampDirName.split("/")
    samp_root = samp_full[-1]
    #print(samp_root)
    buff_full = BuffDirName.split("/")
    buff_root = buff_full[-1]
    #print(buff_root)
    trunc_scal = round(float_buff,4)
    trunc_back = round(float_back,4)  
    stg_scal = str(trunc_scal)
    if trunc_back < 0:
        trunc_back = abs(trunc_back)
        stg_back = str(trunc_back)
        stg_back = "n" + stg_back
    else: stg_back = str(trunc_back)
    new_dir = samp_root + "_" + buff_root + stg_scal + "_" + stg_back
    #print(new_dir)
    os.mkdir(new_dir)
    num_files_samp = len(SampNames)
    num_files_buff = len(BuffNames)
    if num_files_samp != num_files_buff:
        print("Folders Have Different Num Files")
        sys.exit()
    for i in range(0, num_files_samp):
        SubTwoScaledDatsAndBack.ScaleDatsSubAndBack(SampNames[i],float_samp,BuffNames[i],float_buff,float_back,new_dir)

    return(new_dir)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='This code creates a list of .dat files in a given folder')
    parser.add_argument("SampDirName", help = 'Need a Samp Directory Name')
    parser.add_argument("SampScale", help = 'Need a Factor To Over Subtract by')
    parser.add_argument("BuffDirName", help = 'Need a Buff Directory Name')
    parser.add_argument("BuffScale", help = 'Need a Factor To Over Subtract by')
    parser.add_argument("BackFactor", help = 'Need a Factor To Over Subtract by')
    args = parser.parse_args()
    MAINACTION = Over_Sub_And_Back(args.SampDirName, args.SampScale,args.BuffDirName,args.BuffScale,args.BackFactor)

