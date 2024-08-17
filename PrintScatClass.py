#!/usr/bin/env python

"""This code prepares the scattering data class for writing"""

import argparse
import numpy as np

import OpenScatFile

def PrintQ_I_Eclass(qvalues, Ivalues, Evalues, file_name):
    """Takes in data from Q_I_Eclass and prints it to file named file_name"""
    Q_column = np.asarray(qvalues).astype(float)
    I_column = np.asarray(Ivalues).astype(float)
    E_column = np.asarray(Evalues).astype(float)

    num_points = len(qvalues)
    dat_to_print = np.zeros((num_points,3),dtype=float)

    for newindex1 in range(0,num_points):
        dat_to_print[newindex1,0] = Q_column[newindex1]
        dat_to_print[newindex1,1] = I_column[newindex1]
        dat_to_print[newindex1,2] = E_column[newindex1]

    np.savetxt(file_name, dat_to_print, fmt='%1.5f')

    #print(file_name)
    return(dat_to_print)

if __name__== "__main__":
    parser = argparse.ArgumentParser(description='I need a scattering data class')
    parser.add_argument("ScatteringDataFile", help = 'Scattering Data in class form')
    parser.add_argument("OutputDataFile", help = 'Scattering Data in class form')
    args = parser.parse_args()
    Q_I_Eclass = OpenScatFile.OpenScatFile(args.ScatteringDataFile)

    MAINACTION = PrintQ_I_Eclass(Q_I_Eclass.q_values, Q_I_Eclass.I_values, Q_I_Eclass.E_values, args.OutputDataFile)
