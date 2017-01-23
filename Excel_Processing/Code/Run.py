import pandas as pd 
import os.path
from Process_Function import process1
import glob
import hashlib
from Path import final_data_path,location_of_the_data_files
import sys


def listdir_nohidden(path):
    '''Funtions returns all the non hidden files in the path'''
    return glob.glob(os.path.join(path, '*'))


'''If part will run when there is data in final_data ie the program is executed once before'''
if (os.path.isfile(final_data_path+'/'+'Student_Enrolled.xls')      #
	and os.path.isfile(final_data_path+'/'+'Reviews.xls') 
	and os.path.isfile(final_data_path+'/'+'Price.xls')):


	Student_enrolled=pd.read_excel(final_data_path+'/'+'Student_Enrolled.xls')
	Reviews = pd.read_excel(final_data_path+'/'+'Reviews.xls')
	Price   = pd.read_excel(final_data_path+'/'+'Price.xls')
	
	hash1=Student_enrolled['Product Url'].map(lambda x: hash(x))#genrating hash for unique identification
	Student_enrolled['hash']=hash1
	hash2=Reviews['Product Url'].map(lambda x:hash(x)) #genrating hash for unique identification
	Reviews['hash']=hash2
	hash3=Price['Product Url'].map(lambda x: hash(x))  #genrating hash for unique identification
  	Price['hash']=hash3
	
	#latest_entry=list(Student_enrolled.columns)[-1].strip()                   # Most  recently added column name (ie. data) 
	files_to_consider = list(listdir_nohidden(location_of_the_data_files))    # list all the files in folder
	#files_to_consider.sort()
	if len(files_to_consider)==0:
		print "File is already up-to-date"
		sys.exit("File is already up-to-date")	
	files_accesed=Student_enrolled.columns.tolist()[4:] # will contain column name that are dates
	for i in files_accesed:

		for j in files_to_consider:
			if i in j:
				files_to_consider.pop(files_to_consider.index(j))
	files_to_consider.sort()
	
	
	if len(files_to_consider)==0:
		
		sys.exit("File is already up-to-date")
	'''Finally using the Process'''
	for i in files_to_consider:
		print "processing %d out of %d files"%(len(files_to_consider[:files_to_consider.index(i)+1]),len(files_to_consider))
		New_Student_Enrolled, New_Reviews, New_Price = process1(Student_enrolled,Reviews,Price,i)
		Student_enrolled=New_Student_Enrolled
		Reviews         =New_Reviews
		Price           =New_Price

	df1=Student_enrolled[Student_enrolled.columns[:4]] #sort the columns based on date
	df2=Student_enrolled[Student_enrolled.columns[4:]]
	df2=df2.sort_index(axis=1)
	Student_enrolled=pd.concat([df1,df2],axis=1)

	df3=Reviews[Reviews.columns[:4]]                  #sort the columns based on date
	df4=Reviews[Reviews.columns[4:]]
	df4=df4.sort_index(axis=1)
	Reviews=pd.concat([df3,df4],axis=1)

	df5=Price[Price.columns[:4]]                     #sort the columns based on date
	df6=Price[Price.columns[4:]]
	df6=df6.sort_index(axis=1)
	Price=pd.concat([df5,df6],axis=1)

	'''Student_enrolled=Student_enrolled.drop(['hash'], axis=1) #drop hash column
	Reviews         =Reviews.drop(['hash'],axis=1)
	Price           =Price.drop(['hash'],axis=1) 
	'''
	'''Saving the data'''
	Student_enrolled.to_excel(final_data_path+'/'+'Student_Enrolled.xls',index=False)
	Reviews.to_excel(final_data_path+'/'+'Reviews.xls',index=False)
	Price.to_excel(final_data_path+'/'+'Price.xls',index=False)


	#list of the 
# Else parts only xecute when the program is xecuted for first time
else:

	all_the_files=listdir_nohidden(location_of_the_data_files) # all the files in directory
	all_the_files.sort()
	
	print "Populating The Data for first time"
	
	oldest_dated_file = all_the_files.pop(0) # get the file with oldest date in the name
	

	first=pd.read_excel(oldest_dated_file)
	first = first.drop_duplicates(subset=['Product Url'],keep='first').reset_index(drop=True) #Start from oldest file
	date= oldest_dated_file[-22:-11]  #extracting date to put as column name
	hash1=first['Product Url'].map(lambda x: hash(x)) #genrating hash
	first['hash']=hash1

	Student_Enrolled=pd.concat([first['Instructor Name'],first['Product Name'],first['Product Url'],first['hash'],first['Students Enrolled']],axis=1)
	Student_Enrolled=Student_Enrolled.rename(index=str , columns={'Students Enrolled':date})
	#print Student_Enrolled.columns
	Reviews			= pd.concat([first['Instructor Name'],first['Product Name'],first['Product Url'],first['hash'],first['Reviews']],axis=1)
	Reviews			= Reviews.rename(index=str , columns={'Reviews':date})
	Price			= pd.concat([first['Instructor Name'],first['Product Name'],first['Product Url'],first['hash'],first['Price']],axis=1)
	Price			= Price.rename(index=str , columns={'Price':date})

	print all_the_files
	for files in all_the_files:
		
		print "Processing %d out of %d"%(len(all_the_files[:all_the_files.index(files)+1]),len(all_the_files))
		New_Student_Enrolled, New_Reviews, New_Price	 = process1(Student_Enrolled,Reviews,Price, files)
		Student_Enrolled = New_Student_Enrolled
		Reviews 		 = New_Reviews
		Price 			 = New_Price

	df1=Student_Enrolled[Student_Enrolled.columns[:4]]
	df2=Student_Enrolled[Student_Enrolled.columns[4:]]
	df2=df2.sort_index(axis=1)
	Student_Enrolled=pd.concat([df1,df2],axis=1)

	df3=Reviews[Reviews.columns[:4]]
	df4=Reviews[Reviews.columns[4:]]
	df4=df4.sort_index(axis=1)
	Reviews=pd.concat([df3,df4],axis=1)

	df5=Price[Price.columns[:4]]
	df6=Price[Price.columns[4:]]
	df6=df6.sort_index(axis=1)
	Price=pd.concat([df5,df6],axis=1)

	'''Student_Enrolled=Student_Enrolled.drop(['hash'], axis=1)
	Reviews         =Reviews.drop(['hash'],axis=1)
	Price           =Price.drop(['hash'],axis=1) 
	'''
	Student_Enrolled.to_excel(final_data_path+'/'+'Student_Enrolled.xls',index=False)
	Reviews.to_excel(final_data_path+'/'+'Reviews.xls',index=False)
	Price.to_excel(final_data_path+'/'+'Price.xls',index=False)


	






	