from Splitter_batch import Split_Video_files
from Mfcc_Extraction import Extract_MFCC_TalkBox 
from Preprocessing import labeling
from Classification import *
import pandas as pd 
print "Preparing Test Data"
print "###################"
print " "
print "Enter Train Video Path"
path_to_train_videos = raw_input()                      # absolute path to the folders of videos to be used for training 
print " Enter Target Folder to save split videos"       #target where the splitted video will b saved for further processing
target_train_videos = raw_input()
print "Enter the time of split"                         # size of smaller videos
split=int(raw_input())          ### 
Split_Video_files(path_to_train_videos,target_train_videos,split) # after this splitted videos along with .wav file is created

print "MFCC Extraction From Train data"                 #Mfcc xtraction of wav files generated above

print "Enter the number of MFCC Coefficient more or equal to 13 "
Mfcc_coefficient = int(raw_input())
feature_matrix=Extract_MFCC_TalkBox(target_train_videos,Mfcc_coefficient,'Train_MFCC.csv')
train_data=labeling(feature_matrix,target_train_videos) # labeling in preprocessing -  used for taging the mfcc with classification label 
print train_data                                        # final training data subjected to slicing before going for training

print "type a for calculating accuracy of model type b for testing"

x=raw_input()
if x=='a':
	scores =  Classification_spliting_dataset(train_data)
	print scores
	print ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


elif x=='b':
	print 'enter the path of testing videos'
	path_to_test_video=raw_input() # entering the absolute path for testing videos
	print "enter the target to save splited videos"
	path_target_test_videos=raw_input() # path to save splited testing videos must be different from target_train_videos
	print "spliting videos"
	Split_Video_files(path_to_test_video,path_target_test_videos,split)
	print "MFCC Extraction From Test data" # No. of coefficient will be equal to MFcc_coefficient 

	feature_matrix_test=Extract_MFCC_TalkBox(path_target_test_videos,Mfcc_coefficient,'Test_MFCC.csv')
	#train_data=DataFrame(train_data)
	print "******************************************** feature matrix********************"
	feature_matrix_test=pd.DataFrame(feature_matrix_test)
	
	print feature_matrix_test              # feature matrix of Test Videos
	print "**************test data*********"
	print train_data                      
	print "**************training data**********"
	training_data=train_data[train_data.columns[:train_data.shape[1]-2]] # Seprating numerical values with labels
	print training_data
	target=train_data[train_data.columns[train_data.shape[1]-1]]         # labels as vectors to fit in algorithm
	print "***************target***************"
	print target                                                         # target (labels)
	test_matrix=feature_matrix_test[feature_matrix_test.columns[:feature_matrix_test.shape[1]-1]] #Seprating numerical values from Test Data
	test_video_name= feature_matrix_test[feature_matrix_test.columns[feature_matrix_test.shape[1]-1]] #names of the videos
	print "**************test matrix**************"
	print test_matrix

	result = Classification(training_data,target,test_matrix) # Classification.py 
	result=pd.DataFrame(result)                               
	print pd.concat([result, test_video_name], axis=1)        # concating the predicted labels along with name of the videos




