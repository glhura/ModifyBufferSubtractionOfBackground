#!/usr/bin/env python

"""Code subtracts two files using two scale factors and then a background factor"""

import sys
import argparse
import os
import numpy as np

import OpenScatFile
import ChangeFileName

def ScaleDatsSubAndBack(SampName,SampNorm,BuffName,BufNorm,Background,OutPutDir):
	SampData = OpenScatFile.OpenScatFile(SampName)
	BufData = OpenScatFile.OpenScatFile(BuffName)
	if len(SampData.I_values) != len(SampData.I_values): 
		sys.exit("Dat files are of different lengths")

	SubtractedInt = (SampData.I_values/(float(SampNorm))) - (BufData.I_values/(float(BufNorm))) - float(Background)
	ReNormError = (SampData.E_values/(float(SampNorm))) + BufData.E_values/(float(BufNorm)) 
	
	SubFileSize = int(len(SampData.I_values))
	SubDatToPrint = np.zeros((SubFileSize,3))
	for newindex1 in range(0,SubFileSize):
		SubDatToPrint[newindex1,0] = SampData.q_values[newindex1]
		SubDatToPrint[newindex1,1] = SubtractedInt[newindex1]
		SubDatToPrint[newindex1,2] = ReNormError[newindex1]
	FileToPrint = ChangeFileName.ChangeName(SampName,"sub",1)
	if OutPutDir != os.getcwd():
		StringSlashed = FileToPrint.split("/")
		FileToPrint = StringSlashed[-1]
		FileToPrint = os.path.join(OutPutDir,FileToPrint)
	
	np.savetxt(FileToPrint, SubDatToPrint,fmt='%1.5f')
	#print("wrote %s" % FileToPrint)
	return(FileToPrint)



if __name__=="__main__":
	parser = argparse.ArgumentParser(description='This takes a cbf file as input')
	parser.add_argument('SampName', help = 'Need Sample File')
	parser.add_argument('SampScale', help = 'Need Sample Scale Factor')
	parser.add_argument('BufName', help = 'Need Buffer File')
	parser.add_argument('BufScale', help = 'Need Buffer Scale Factor')
	parser.add_argument('Background', help = 'Need an offset')
	parser.add_argument("--DefineOut", type= str, required=False)

	args = parser.parse_args()
	OutPutDir = os.getcwd()
	#print(args.DefineOut)
	if args.DefineOut:
		OutPutDir = os.path.join(OutPutDir,args.DefineOut)
	
	#print(OutPutDir)
	MAINACTION = ScaleDatsSubAndBack(args.SampName,args.SampScale,args.BufName,args.BufScale,args.Background,OutPutDir)
