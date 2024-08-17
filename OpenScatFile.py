#!/usr/bin/env python
"""This program is pretty fundemental in defining a class to handle scattering data"""

import re
import argparse
import numpy as np

class Q_I_Error:
    """This is a fundemental class for evaluating scattering data"""
    def __init__(self, q_values, I_values, E_values):
        self.q_values = q_values
        self.I_values = I_values
        self.E_values = E_values
    def __repr__(self):
        return repr((self.q_values, self.I_values, self.E_values))

#This function reads a file and outputs a class Q_I_Error
#If Error is missing it adds Error of 3% of I

def OpenScatFile(file_name):

    """This Opens a File and places the contents in the defined class"""
    # Read the data in from a file to a list
    column1 = []
    column2 = []
    column3 = []
    #num_lines = 0
    #print("Hello")
    with open(file_name, 'r', encoding = "utf8") as in_file:
        for line in in_file:
            #print(line)
            if line.find('#') > 0:
                line = in_file.readline()
            line = line.rstrip("\n")
            line = line.rstrip("\t")
            #line.replace('\t', " ")
            line = line.rstrip(" ")
            line_contents = re.split(r"\s+", line)
            #print(line_contents)

            if (len(line_contents) == 3 and float(line_contents[0])):

                column1.append(line_contents[0])
                column2.append(line_contents[1])
                column3.append(line_contents[2])

            if (len(line_contents) == 2 and float(line_contents[0])):
                column1.append(line_contents[0])
                column2.append(line_contents[1])
                column3.append(float(line_contents[1])*0.03)

    q_column = np.asarray(column1).astype(float)
    i_column = np.asarray(column2).astype(float)
    e_column = np.asarray(column3).astype(float)

    final_output = Q_I_Error(q_column, i_column, e_column)
    in_file.close()

    return final_output

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Need scattering file; outputs contents as Q_I_Eclass")
    parser.add_argument("FileName", help = 'Need File to Work On')
    args = parser.parse_args()
    MAINACTION = OpenScatFile(args.FileName)
    #print(MAINACTION)
