########################################################
# resultHandler.py 
# Author: Jamie Zhu <jimzhu@GitHub>
# Created: 2014/2/6
# Last updated: 2014/11/7
########################################################

import numpy as np
import linecache
import os, sys, time
 

def main():
	para = {'metrics': ['MAE', 'NMAE', 'RMSE', 'MRE', 'NPRE']} # delete where appropriate
	resultFolder = '../result/'
	lineIdToExtract = 2
	timeSlice = 7
	density = list(np.arange(0.02, 0.11, 0.02))

	# add result/average folder
	if not os.path.exists('../result/average'):
		os.mkdir('../result/average')

	for den in density:
		result = []
		for timeslice in range(timeSlice):
			inputfile = resultFolder + '%02d_relResult_%.2f.txt'%(timeslice + 1, den)
			data = linecache.getline(inputfile, lineIdToExtract).strip().split('\t')
			metrics = [float(x) for x in data[1:]]
			result.append(metrics)
		outfile = resultFolder + 'average/avg_relResult_%.2f.txt'%(den)
		saveResult(outfile, np.array(result), para)
		avgResult = np.average(result, axis = 0)
		print avgResult


########################################################
# Save the evaluation results into file
#
def saveResult(outfile, result, para):
    fileID = open(outfile, 'w')
    fileID.write('Metric: ')
    for metric in para['metrics']:
        fileID.write('| %s\t'%metric)
    avgResult = np.average(result, axis = 0)         
    fileID.write('\nAvg:\t')
    np.savetxt(fileID, np.matrix(avgResult), fmt='%.4f', delimiter='\t')
    stdResult = np.std(result, axis = 0)
    fileID.write('Std:\t')
    np.savetxt(fileID, np.matrix(stdResult), fmt='%.4f', delimiter='\t')
    fileID.write('\n==========================================\n')
    fileID.write('Detailed results for %d slices:\n'%result.shape[0])
    np.savetxt(fileID, result, fmt='%.4f', delimiter='\t')     
    fileID.close()
########################################################


if __name__ == "__main__": main()