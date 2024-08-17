#!/usr/bin/env python
#This code checks to make sure two scat files have the same q-axis

import sys
import argparse
import os
import numpy as np

import OpenScatFile

def SameQaxisCheck(FileName1, FileName2):	
	FilesHaveSameQRange = True
	
	File1 = OpenScatFile.OpenScatFile(FileName1)
	File2 = OpenScatFile.OpenScatFile(FileName2)
	NumPointsFile1 = len(File1.q_values)
	NumPointsFile2 = len(File2.q_values)
	if NumPointsFile1 != NumPointsFile2:
		FilesHaveSameQRange = False
		print("These two files have different q axis " + FileName1 + FileName2)
	if FilesHaveSameQRange is True:	
		ArrayDiff = File1.q_values - File2.q_values
		ScalarDiff = np.sum(ArrayDiff)
		if ScalarDiff != 0.0 :
			FilesHaveSameQRange = False
			print("These two files have different q axis " + FileName1 + FileName2)
		
	#print(FilesHaveSameQRange)
	return(FilesHaveSameQRange)

if __name__=="__main__":
	parser = argparse.ArgumentParser(description='This takes two files as an input and checks to make sure they can be manipulated together')
	parser.add_argument("FileName1", help = 'File1')
	parser.add_argument("FileName2", help = 'File2')
	args = parser.parse_args()
	MAINACTION = SameQaxisCheck(args.FileName1, args.FileName2)
