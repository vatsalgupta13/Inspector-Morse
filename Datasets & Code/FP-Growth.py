# Applying Frequent Pattern Growth (FP Growth) Algorithm on Chicago dataset
# Importing the libraries
import time 
import timing 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import pyfpgrowth as fp



# Data Preprocessing
dataset = pd.read_csv('forapriori.csv')
dataset['Date'] = pd.to_datetime(dataset.Date) # converting date in our dataset to pandas date format
dataset['date'] = [d.date() for d in dataset['Date']] # separating date and time in our column
dataset['time'] = [d.time() for d in dataset['Date']]

dataset['time'] = dataset['time'].astype(str) # convert time to string

#extracting month from date
dataset['date'] = pd.to_datetime(dataset['date'])
dataset['Month-number'] = dataset['date'].dt.month  # month number
dataset['Month'] = dataset['date'].dt.strftime('%B') #month name

# now dropping original date column which consisted of both data and time
dataset.drop(['Date'], axis=1, inplace=True)


dataset = dataset[pd.notnull(dataset['Location Description'])] # keeping only those rows where location description is not null (i.e removing rows with missing data)
dataset = dataset[pd.notnull(dataset['District'])] # keeping only those rows where district is not missing
# resetting index since index has gaps
dataset = dataset.reset_index()
del dataset['index']

# defining timeslots
t1 = '24:00:00'
t1_a = '00:00:00'
#t1_obj= datetime.strptime(t1,'%H:%M:%S')

t2 = '04:00:00'
#t2_obj= datetime.strptime(t2,'%H:%M:%S')
t3 = '08:00:00'
t4 = '12:00:00'
t5 = '14:00:00'
t6 = '17:00:00'
t7 = '19:00:00'
t8 = '21:00:00'

count_row = dataset.shape[0]

# empty list for timeslots
timeslot = []*count_row





# dividing time into time slots and adding them to our list
for i in range(0,count_row):
        if dataset.values[i,5]< t1 and dataset.values[i,5]>=t8:
            timeslot.append('Night')
        elif dataset.values[i,5]< t2 and dataset.values[i,5]>=t1_a:
            timeslot.append('Midnight')
        elif dataset.values[i,5]< t3 and dataset.values[i,5]>=t2:
            timeslot.append('Early Morning')
        elif dataset.values[i,5]< t4 and dataset.values[i,5]>=t3:
            timeslot.append('Late Morning')
        elif dataset.values[i,5]< t5 and dataset.values[i,5]>=t4:
            timeslot.append('Early Afternoon')
        elif dataset.values[i,5]< t6 and dataset.values[i,5]>=t5:
            timeslot.append('Late Afternoon')
        elif dataset.values[i,5]< t7 and dataset.values[i,5]>=t6:
            timeslot.append('Early Evening')
        else :
            timeslot.append('Late Evening')

# appending the list to our dataset
dataset['Timeslot'] = timeslot

# now dropping date,time and month no. column
dataset.drop(['date', 'time', 'Month-number'], axis=1, inplace=True)
#dataset.drop([ 'Month'], axis=1, inplace=True)


# reindexing the dataset in order to put the crime type column at the end
columnsTitles = ['District','Block', 'Location Description', 'Month', 'Timeslot', 'Primary Type']

dataset = dataset.reindex(columns=columnsTitles)

new_dataset = [] # creating an empty list
for k in range(0,count_row):
         t= dataset.values[k,5]
         new_dataset.append(t)   # appending the 5th column of all rows of our dataset


# creating a unique list of primary types
list_set = set(new_dataset)
unique_list = (list(list_set)) # list containing unique crime (primary) types
count_unique=len(unique_list) # count of unique elements 


# Applying FP Growth
starttime = time.time()
transactions = []   # initialising an empty list
for i in range(0, count_row):
    transactions.append([str(dataset.values[i,j]) for j in range(0, 6)])
    
patterns = fp.find_frequent_patterns(transactions, 3)
rules = fp.generate_association_rules(patterns,0.5) # finding rules
timeelapsed = starttime - time.time()
print("Time elapsed for generating rules using FP Growth : ", timeelapsed)

# separating antecedents (lhs) and consequents (rhs) 
key_list = []
value_list = []
for key in rules.keys():
     key_list.append(key)
for value in rules.values():
        value_list.append(value)


# cleaning the consequents
import itertools
unwind_values = list(itertools.chain(*value_list))
rule_rhs = [x for x in unwind_values if not isinstance(x, float)]
confidence = [x for x in unwind_values if isinstance(x,float)]

# function to calculate support count 
def support_count(rhs):
    count=0
    rhs = set(rhs)
    for j in df["items"]:
        j = set(j)
        if(rhs.issubset(j)):
            count  = count+1
    return count


# a dataframe consisting of all the transactions before they were converted into rules    
df = pd.DataFrame()
df['items'] = transactions 

# creating a new dataframe consisting of support, confidence, lift, conviction
rules_df = pd.DataFrame()
rules_df['Antecedent'] = key_list
rules_df['Consequent'] = rule_rhs
rules_df['Confidence'] = confidence

# calculating lift and conviction using support count 
rhs_support = []
for i in rules_df["Consequent"]:
    a = support_count(i)
    rhs_support.append(a/len(df))
rules_df['RHS support'] = rhs_support
rules_df['Lift'] = rules_df['Confidence']/rules_df['RHS support']
rules_df['Conviction'] = (1-rules_df['RHS support'])/(1-rules_df['Confidence'])

# unwinding the antecedents' and consequents' array
rule_frame = pd.DataFrame(rules_df.Antecedent.tolist(), columns=['key1', 'key2', 'key3'])
df2 = pd.DataFrame(rules_df.Consequent.tolist(),columns = ['rule_rhs1', 'rule_rhs2'])
rule_frame['rule_rhs1'] = df2['rule_rhs1']
rule_frame['rule_rhs2'] = df2['rule_rhs2']
rule_frame['Support'] = rules_df['RHS support']
rule_frame['Confidence'] = rules_df['Confidence']
rule_frame['Lift'] = rules_df['Lift']
rule_frame['Conviction'] = rules_df['Conviction']


# seeing the results in a better format with crime type as the consequent
count_rules = rule_frame.shape[0]
count_col = rule_frame.shape[1]
for i in range(0,count_rules):
    for j in range(0,count_col-4):
        if(rule_frame.values[i,j]):
            str = ''.join(rule_frame.values[i,j])
            for k in range(0,count_unique):
                if str==unique_list[k]:
                    q=j
                    for t in range(0,count_col-4):
                        if(t!=q and rule_frame.values[i,t]):
                            print(rule_frame.values[i,t],',')
                    print ('->', rule_frame.values[i,q])
                    print ('Support is :' , rule_frame.values[i,5])
                    print ('Confidence is :' , rule_frame.values[i,6])
                    print ('Lift is :' , rule_frame.values[i,7])
                    print ('Conviction is :' , rule_frame.values[i,8])
                    print ("#####################################################")
                    break
        continue
                   
                
                



    
    
    


