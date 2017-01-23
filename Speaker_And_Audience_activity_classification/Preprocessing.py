import os
import subprocess
import numpy as np
import pandas as pd

def list_files(path,extension=""):
	''' Lists all the files with exension specified in argument extension
		returns list of the file names	'''
	final=[]
	for files in os.listdir(path):
		#print files
		if files.endswith(extension):
			final.append(files)

	return final


def write_ceps(path,file,ceps):
	ceps_name=path+'/'+os.path.splitext(file)[0]+".ceps"
	numpy.save(ceps_name,ceps)
	print "Written to %s" %ceps_name

''' labels the MFCC featur matrix based on the subscript of the file name eg. 001_0-2.wav ll be applause'''
def labeling(feature_matrix,path_to_save):
	#matrix=pd.read_csv(path_to_Feature_Mfcc,dtype=object,header=None)
	matrix=pd.DataFrame(feature_matrix)
	print matrix
	audio_labels=pd.read_csv('labels.csv',dtype=object) #read the file name and respective labels
	file_names=matrix[matrix.shape[1]-1]                #extract file names from feature matrix
	
	file_names=list(file_names)
	#print list(file_names)
	labels=[]
	#print audio_labels['name'].values
	for names in file_names:

		if names[:3] in audio_labels['name'].values:
			print names[:3],audio_labels['label'][audio_labels[audio_labels['name']==names[:3]].index[0]]
	#		print names[:3]
			labels.append(audio_labels['label'][audio_labels[audio_labels['name']==names[:3]].index[0]]) #add labels to the list

	labels=pd.DataFrame(labels)
	labels.columns=[matrix.shape[1]]
	result = pd.concat([matrix, labels], axis=1) #concat feature matrix with labels

	result.to_csv(path_to_save+'/'+'final_Mfcc.csv',sep=',',index=False,index_label=False) #save
	return result







