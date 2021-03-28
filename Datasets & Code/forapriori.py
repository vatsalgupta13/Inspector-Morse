# Applying Apriori in Chicago Dataset
# Importing the libraries
import time
import timing 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

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

# Applying Apriori
transactions = []   # initialising an empty list
for i in range(0, count_row):
    transactions.append([str(dataset.values[i,j]) for j in range(0, 6)])

# Training Apriori on the dataset
starttime = time.time()
from efficient_apriori import apriori
itemsets, rules = apriori(transactions, min_support = 0.0020935101186, min_confidence = 0.5)
timeelapsed = starttime - time.time()
print("Time elapsed for generating rules using Apriori : ", timeelapsed)


#results = list(rules)
# Print out every rule with 3 items on the left hand side,
# 1 item on the right hand side, sorted by lift
rules_rhs = filter(lambda rule: len(rule.lhs) >= 3 and len(rule.rhs) == 1 , rules)
rules_rh = list(rules_rhs)
for rule in sorted(rules_rhs, key=lambda rule: rule.lift):
               str =  ''.join(rule.rhs)
               for j in range(0,count_unique):
                    if str==unique_list[j]:
                          print( rule.lhs , '->' , rule.rhs)
                          print('Support is :', rule.support)
                          print ('Confidence is :' , rule.confidence)
                          print ('Lift is :' , rule.lift)
                          print ('Conviction is :' , rule.conviction)
                          print("#####################################################")







