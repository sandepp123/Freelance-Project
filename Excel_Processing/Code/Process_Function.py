import pandas as pd 
import hashlib

def get_group(g,key):
    if key in g.groups:return g.get_group(key)                 
    return pd.DataFrame()
def process1(Student_Enrolled,Reviews,Price,i):
    
    new_data = pd.read_excel(i)
    new_data=new_data.drop_duplicates(subset=['Product Url'],keep='first').reset_index(drop=True) #remove duplicate
    ''' Outer merge will gives us which courses are common,deleted and added in the new file'''

    merged1 = pd.DataFrame(Student_Enrolled['Product Url']).merge(pd.DataFrame(new_data['Product Url']), how='outer', indicator=True)
    deleted_course=merged1[merged1['_merge']=='left_only']
    added_courses= merged1[merged1['_merge']=='right_only']
    common_courses=merged1[merged1['_merge']=='both']
    
    Columns=list(Student_Enrolled.columns) #give the names of the columns in the processed file
    Columns.append(i[-22:-11])             #date from new_data path extracted by i[-22:-11] to be used as new column
    
    

    #generate Hash Code
    hash2=new_data['Product Url'].map(lambda x: hash(x))
    new_data['hash']=hash2
    list_of_col=new_data.columns.tolist()
    new_data = new_data.sort_values(new_data.columns[list_of_col.index('hash')])

    #new_data=new_data.sort(['hash'])
    iter_rows=Student_Enrolled.iterrows() #for faster iterating on rows
    x=[]                                   # for Students_Enrollede
    y=[]                                   # for Reviews
    z=[]                                   # for Price
    for i,rows in iter_rows:
        temp1=new_data['hash'].values.searchsorted(rows['hash']) #search fo hash code in sorted new_data,Binary search
        #print type(i),'******************'
        temp2=new_data.iloc[temp1] #data at searched position
        if temp2['hash']==rows['hash']: # checks if data is found in new_data as searchsorted tells us index where searched data can be added
            
            m=rows.values.tolist()
            m.append(int(temp2['Students Enrolled'])) #append new data
            x.append(m)
            m2=Reviews.iloc[int(i)].values.tolist()
            m2.append(temp2['Reviews'])
            y.append(m2)
            m3=Price.iloc[int(i)].values.tolist()
            m3.append(temp2['Price'])
            z.append(m3)
            
            
  
    
    Student_Enrolled_GroupBy=Student_Enrolled.groupby(['Product Url'])
    new_data_groupby        = new_data.groupby(['Product Url'])

  
       #for newly added courses
    for k in added_courses['Product Url']:
        x4 = new_data_groupby.get_group(k)
        #print x4
        xt = [-1 for i in range(len(Columns))]
        #print xt
        xt[0]=x4['Instructor Name'].values[0]
        xt[1]=x4['Product Name'].values[0]
        xt[2]=x4['Product Url'].values[0]
        xt[3]=x4['hash'].values[0]
        xt[-1]=x4['Students Enrolled'].values[0]
        x.append(xt)
        #print xt
        xt2=[-1 for i in range(len(Columns))]
        xt2[0]=x4['Instructor Name'].values[0]
        xt2[1]=x4['Product Name'].values[0]
        xt2[2]=x4['Product Url'].values[0]
        xt2[3]=x4['hash'].values[0]
        xt2[-1]=x4['Reviews'].values[0]
        y.append(xt2)
        xt3=[-1 for i in range(len(Columns))]
        xt3[0]=x4['Instructor Name'].values[0]
        xt3[1]=x4['Product Name'].values[0]
        xt3[2]=x4['Product Url'].values[0]
        xt3[3]=x4['hash'].values[0]
        xt3[-1]=x4['Students Enrolled'].values[0]
        xt3[-1]=x4['Price'].values[0]
        z.append(xt3)
        xt=[]
    #print x[-1]

# for deleted courses
    for j in deleted_course['Product Url']:
        t = int (Student_Enrolled_GroupBy.get_group(j).index[0])
        x5=Student_Enrolled.iloc[t].values.tolist()
        x6=Reviews.iloc[t].values.tolist()
        x7=Price.iloc[t].values.tolist()  
        
        
        while len(x5)!=len(Columns):
            x5.append(-1)
            x6.append(-1)
            x7.append(-1)

        x.append(x5)
        #print x5
        y.append(x6)
        z.append(x7)


    '''convrt x,y,z into dataframes'''  
    intermediate=pd.DataFrame(x,columns=Columns)
    intermediate_Reviews=pd.DataFrame(y,columns=Columns)
    intermediate_Price=pd.DataFrame(z,columns=Columns)  
            
       
    return intermediate,intermediate_Reviews,intermediate_Price
