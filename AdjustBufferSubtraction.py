#!/usr/bin/env python

"""This program optimizes the subtraction of two files to create a subtracted file"""
"""The subtracted file will set a q region to an input value"""

import sys
import argparse
import os
import numpy as np

"""These are custom code"""
import DoTheseFilesHaveSameQ
import OpenScatFile
import PrintScatClass
import ChangeFileName

def offset_subtraction(sample_file_name, buffer_file_name, Value, qmin, qmax, print_file, method_pick):
    """Main function, calls one sub-function defined below"""
    good_or_bad = DoTheseFilesHaveSameQ.SameQaxisCheck(sample_file_name,buffer_file_name)
    #print(good_or_bad)
    if good_or_bad is False:
        print("Input files do not have the same q range as one another")
        exit()
        
    """Once the two files are validated code cand proceed"""
    scale_factor = 1.0
    background = 0.0
    if good_or_bad is True:
        samp_file = OpenScatFile.OpenScatFile(sample_file_name)
        buff_file = OpenScatFile.OpenScatFile(buffer_file_name)
        
        """This is the sub-fuction defined below to pull q-range data"""
        qplaces = extract_q_range(samp_file,qmin,qmax)
        samp_reg_int = samp_file.I_values[qplaces[0]:qplaces[1]]
        buff_reg_int = buff_file.I_values[qplaces[0]:qplaces[1]]
        q_reg_int = samp_file.q_values[qplaces[0]:qplaces[1]]
        
        """Here we fit the sample data in range as quadratic"""
        samp_coef = np.polyfit(q_reg_int, samp_reg_int, 2) 
        samp_p2 = np.poly1d(samp_coef)
        fit_samp_data = samp_p2(q_reg_int)
        
        """Here we fit unsubtracted buffer data as quadratic"""
        buff_coef = np.polyfit(q_reg_int, buff_reg_int, 2) 
        buff_p2 = np.poly1d(buff_coef)
        fit_buff_data = buff_p2(q_reg_int)
        
        #print(diff_usual)
        #print(fit_diff_data)
        """Here we identified the fit data minima"""
        min_value_fit = np.amin(fit_samp_data)
        min_value_pos = np.argmin(fit_samp_data)
        buff_val_at_samp_fit_min = fit_buff_data[min_value_pos]
        
        """Here we define the adjustment needed to the buffer so that"""
        """when subtracted the minimum of the data hits the desired value using scaling"""
        adjuster = ((min_value_fit - float (Value))/buff_val_at_samp_fit_min)
        print(adjuster)
        
        """Here we define the adjustment needed to the buffer so that"""
        """when subtracted the minimum of the data hits the desired value using background"""
        adjuster_back = (min_value_fit - buff_val_at_samp_fit_min - float (Value))
        print(adjuster_back)
        
        """Trying to find a minimal scale factor and background that does the job"""
        """This is done by knowing that the missing parameters are on a line"""
        """the minimal disance between that line and a scale of 1 and background of 0 (1,0)"""
        """can be found by a perpendicular slope going through (1,0)"""
        min_scale_2 = (buff_val_at_samp_fit_min + min_value_fit - float (Value))/(2*buff_val_at_samp_fit_min)
        min_back_2 = (-(buff_val_at_samp_fit_min + min_value_fit - float (Value))/2) + buff_val_at_samp_fit_min
        print(min_scale_2, min_back_2)
        
        return_values= np.zeros(2)
        """We apply the adjustment for a new file"""

        print(method_pick)
        if method_pick == 1:
            full_adjusted = samp_file.I_values - adjuster*buff_file.I_values
            return_values = [adjuster,0.0]
        if method_pick == 2:
            full_adjusted = samp_file.I_values - buff_file.I_values - adjuster_back
            return_values = [1.0,adjuster_back]
        if method_pick == 3:
            full_adjusted = samp_file.I_values - min_scale_2*buff_file.I_values - min_back_2
            return_values = [min_scale_2,-1*min_back_2] 

        #print(full_diff_adjusted)
        if print_file == 1:
            up_or_down = "up"
            if return_values[1] < 1.0:
                up_or_down = "dn"
            mod = up_or_down + ".dat"
            """We print the new data into a new file with a name"""
            new_file_name = ChangeFileName.ChangeName(sample_file_name,mod,0)
            PrintScatClass.PrintQ_I_Eclass(samp_file.q_values, full_adjusted, samp_file.E_values, new_file_name)
            #print(new_file_name)
        
    print(return_values)    
    return (return_values)    	

def extract_q_range(samp_file, qmin, qmax):
    """This part finds the data associated with the q range of interest"""
    q_size = len(samp_file.q_values)
    qmin_place = 0
    qmax_place = 0
    for i in range(0,q_size):
        if samp_file.q_values[i] > float (qmin):
            qmin_place = i
            break
    for i in range(0,q_size):        
        if samp_file.q_values[i] > float (qmax):
            qmax_place = i
            break
    if qmin_place == 0 or qmax_place == 0:
        print("Input files did not have the q range specified")
        exit()
    return(qmin_place,qmax_place)    
    
        
                


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="This code needs two scattering profiles a value and a qmin and qmax, three options are available")
    parser.add_argument("sample_file_name", help = 'Need Two Files, A Value to match, Qmin and Qmax')
    parser.add_argument("buffer_file_name", help = 'Need Two Files, A Value to match, Qmin and Qmax')
    parser.add_argument("Value", help = 'Need Two Files, A Value to match, Qmin and Qmax')
    parser.add_argument("qmin", help = 'Need Two Files, A Value to match, Qmin and Qmax')
    parser.add_argument("qmax", help = 'Need Two Files, A Value to match, Qmin and Qmax')
    parser.add_argument("--printfile", action = "store_true", help = "Print File")
    parser.add_argument("--scale", action = "store_true", help = "Scaling Buffer for Result")
    parser.add_argument("--offset", action = "store_true", help = "Using an Offset for Result")
    parser.add_argument("--both", action = "store_true", help = "Using both a Scale Factor And An Offset")
    args = parser.parse_args()
    PRINT_FILE = 0
    if args.printfile:
        PRINT_FILE = 1
    method_pick = 1
    if args.scale:
        method_pic = 1
        print("I Understand")
    if args.offset:
        method_pick = 2
    if args.both:
        method_pick = 3    
    mainaction = offset_subtraction(args.sample_file_name, args.buffer_file_name, args.Value, args.qmin, args.qmax, PRINT_FILE, method_pick)