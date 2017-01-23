from Preprocessing import list_files
from scikits.talkbox.features import mfcc
import scipy
import librosa
import essentia, essentia.standard as ess
import pandas as pd
import numpy as np

#### MFCC Using Librosa Library  *********not used******************	#####
def Extract_MFCC_Librosa(path,number_of_Mfcc=20,name="MFCC_Librosa_.csv"):
	files=list_files(path,".wav")
	for file in files:
		x, fs = librosa.load(path+"/"+file)
		mfccs = librosa.feature.mfcc(x, sr=fs) #mfccs



#### MFCC Using Scikit Talkbox Library #####
def Extract_MFCC_TalkBox(path,number_of_Mfcc=13,name="MFCC_Talk_Box.csv"):
	files=list_files(path,".wav")
	ci=0    #for keeping count of files and track of program

	X,y,label=[],[],[]
	for file in files:
		prefix=file[:3]                                       #will be used for labeling
		sample_rate, X1 = scipy.io.wavfile.read(path+"/"+file) #Read wav file  
		ceps, mspec, spec = mfcc(X1) # ceps contains the mfcc
		#write_ceps(path,file,ceps)
		num_ceps=len(ceps) #eg. 100,13
		X.append(np.mean(ceps[int(num_ceps*0.1):int(num_ceps*0.9)], axis=0))#mean is taken column wise mean([[0,0,0][1,2,4][3,2,1]])=[[4/3,4/3,5/3]]
		y.append(file)
		print ci, file
		ci+=1
		

	c=np.column_stack([X,y])         #adding file name to the extracted features respectively
	np.savetxt(path+'/'+name, c, delimiter=',', fmt='%s') # saves Mfcc in the dataset folder 
	return c
	#return c if want 		

#MFCC using Essentia*********not used******************		
def Extract_Mfcc_Essetia(path):
	hamming_window = ess.Windowing(type='hamming')
	spectrum = ess.Spectrum() 
	mfcc = essentia.standard.MFCC(numberCoefficients=13)
	frame_sz = 1024
	hop_sz = 500
	files=list_files(path,".wav")
	for file in files:
		x, fs = librosa.load(path+"/"+file)
		
		mfccs = numpy.array([mfcc(spectrum(hamming_window(frame)) ) [1] for frame in essentia.standard.FrameGenerator(x, frameSize=frame_sz, hopSize=hop_sz)])
		print mfccs.shape , " "+file


