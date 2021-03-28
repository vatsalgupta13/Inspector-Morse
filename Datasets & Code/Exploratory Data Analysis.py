# Exploratory Data Analysis
# importing the necessary libraries
from __future__ import division   # future functionality for integer division,
import warnings
warnings.filterwarnings('ignore')
import numpy as np  # tools for working with arrays
import pandas as pd  # used for data analysis
import matplotlib.pyplot as plt
from IPython import get_ipython
ipy = get_ipython()     # alternative python interpreter
if ipy is not None:                             # sets the backend of matplotlib to the 'inline'
    ipy.run_line_magic('matplotlib', 'inline')  # backend: With this the output of plotting commands
                                                # is displayed inline within frontends


data = pd.read_csv("Crimes - 2019.csv")


# dropping some unnecessary or redundant columns
data.drop(['X Coordinate', 'Y Coordinate', 'Updated On', 'Location', 'Beat'], axis=1, inplace=True)

# doing some data preprocessing
data['Date'] = pd.to_datetime(data.Date) # converting date in our dataset to pandas date format
data['date'] = [d.date() for d in data['Date']] # separating date and time in our column
data['time'] = [d.time() for d in data['Date']]

data['time'] = data['time'].astype(str) # convert time to string
empty_list = []
for timestr in data['time'].tolist():
    ftr = [3600,60,1]
    var = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])  # splitting into hours minutes and seconds
    empty_list.append(var)
    
data['seconds'] = empty_list
# convert dates to pandas datetime format
data.Date = pd.to_datetime(data.Date, format='%m/%d/%Y %I:%M:%S %p')
# setting the index to be the date will help us a lot later on
data.index = pd.DatetimeIndex(data.Date)

# month wise
plt.figure(figsize=(11,6))
data.groupby([data.index.month]).size().plot(legend=False)
plt.title('Number of crimes per month (2019)')
plt.xlabel('Months')
plt.ylabel('Number of crimes')
plt.show()

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']
data.groupby([data.index.month]).size().plot(kind='barh', color = 'maroon', figsize=(10, 9))
plt.ylabel('Month of Year')
plt.yticks(np.arange(11), months)
plt.xlabel('Number of crimes')
plt.title('Number of crimes per month(2019)')
plt.show()

# day wise
plt.figure(figsize=(11,6))
data.groupby([data.index.dayofweek]).size().plot(legend=False, color = 'purple')
plt.title('Number of crimes by day of week (2019)')
plt.xlabel('Days')
plt.ylabel('Number of crimes')
plt.show()





plt.figure(figsize=(8,10))
data.groupby([data['Primary Type']]).size().sort_values(ascending=True).plot(kind='barh') # horizontal bar graph
plt.title('Number of crimes by type')
plt.ylabel('Crime Type')
plt.xlabel('Number of crimes')
plt.show()

# creating an excel style hierarchial table with location description as  and aggregating primary type using the defined function np.size
location_by_type  = data.pivot_table(values='ID', index='Location Description', columns='Primary Type', aggfunc=np.size).fillna(0)


from sklearn.cluster import AgglomerativeClustering as AC

# standarising dataframe
def scale_df(df,axis=0):
    return (df - df.mean(axis=axis)) / df.std(axis=axis)

# normalising dataframe
def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result

df = normalize(location_by_type)
ix = AC(3).fit(df.T).labels_.argsort()
plt.figure(figsize=(27, 12))
plt.imshow(df.T.iloc[ix,:], cmap='Reds')
plt.colorbar(fraction=0.03)
plt.xticks(np.arange(df.shape[0]), df.index, rotation='vertical')
plt.yticks(np.arange(df.shape[1]), df.columns)
plt.title('Normalized location frequency for each crime')
plt.grid(False)
plt.show()
