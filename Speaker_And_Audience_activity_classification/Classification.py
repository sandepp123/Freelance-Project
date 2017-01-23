from sklearn import svm

from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
import pandas as pd
import numpy as np


''' Classification with seperate test data '''
def Classification(train_data,label,test_data):
	clf=svm.SVC()
	clf.fit(train_data,label)
	result=clf.predict(test_data)
	return result

'''Classification splitting test data'''
def Classification_spliting_dataset(data):
	data1=data[data.columns[:data.shape[1]-2]]
	target2=data[data.columns[data.shape[1]-1]]
	clf2=svm.SVC()
	scores = cross_val_score(clf2, data1, target2, cv=5)
	
	return scores


