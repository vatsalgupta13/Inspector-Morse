# importing the necessary libraries
from __future__ import division   # future functionality for integer division,
import warnings
warnings.filterwarnings('ignore')
import timing # not an inbuilt package...compiled by myself...location : anaconda - lib - sitepackages - timing.py
import numpy as np  # tools for working with arrays
import pandas as pd  # used for data analysis
import matplotlib.pyplot as plt
from IPython import get_ipython
ipy = get_ipython()     # alternative python interpreter
if ipy is not None:                             # sets the backend of matplotlib to the 'inline'
    ipy.run_line_magic('matplotlib', 'inline')  # backend: With this the output of plotting commands
                                                # is displayed inline within frontends
from sklearn.cluster import KMeans
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D # for 3D graphs
from plotly.graph_objs import Scatter, Figure, Layout # for plotting graphs



data = pd.read_csv("forclustering.csv")
data.head() # gets the first five rows of data

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

# Clustering based on Time, District and Primary Type(as per IUCR codes).
# Here we will scale the time in seconds to be between 1 and 0, with 0.5 representing the
# time 12:00 noon(else clusters will only be based on time segments), that way the
# clusters will be divided into sections of morning, afternoon and night.


# Normalizing the time to be between 0 and 1, this way lower values would indicate midnight to early morning
# medium values would indicate the afternoon sessions, and high values would indicate evening and night time
# also kmeans then won't cluster just based on the time as the range of euclidean distances in time column will be very high without scaling
data['Normalized_time'] = (data['seconds'] - data['seconds'].min())/(data['seconds'].max()-data['seconds'].min())


sub_data1 = data[['IUCR', 'Normalized_time', 'District']]
sub_data1['IUCR'] = sub_data1.IUCR.str.extract('(\d+)', expand=True).astype(int)
sub_data1['IUCR'] = (sub_data1['IUCR'] - sub_data1['IUCR'].min())/(sub_data1['IUCR'].max()-sub_data1['IUCR'].min())
sub_data1['District'] = (sub_data1['District'] - sub_data1['District'].min())/(sub_data1['District'].max()-sub_data1['District'].min())
sub_data1.head()

# finding optimum clusters using Elbow Method
wcss = []
for i in range (1,20):
    kmeans = KMeans(n_clusters = i , init = 'k-means++' , max_iter = 300 , n_init = 10, random_state=0)
    kmeans.fit(sub_data1)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,20), wcss)
plt.title('The Elbow Method') 
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()


# plotting with 4 clusters
km = KMeans(n_clusters=4)
km.fit(sub_data1)
y = km.predict(sub_data1)
labels = km.labels_
sub_data1['Clusters'] = y
sub_data1.head()
data.drop(['ID', 'Arrest','Domestic', 'Census Tracts', 'Wards', 'Boundaries - ZIP Codes', 'Police Districts', 'Police Beats'], axis=1, inplace=True)
data.drop(['Date', 'Location Description','Ward', 'Community Area', 'Historical Wards 2003-2015'], axis = 1, inplace = True)
data.drop(['Zip Codes', 'Community Areas', 'seconds'], axis=1, inplace=True)
data.drop(['Case Number', 'FBI Code', 'Year'], axis = 1, inplace = True)
data.drop(['Description'], axis = 1, inplace = True)
data['Clusters']= sub_data1['Clusters']


fig = plt.figure(figsize=(12,10))
ax = fig.add_subplot(111, projection='3d')
x = np.array(sub_data1['Normalized_time'])
y = np.array(sub_data1['IUCR'])
z = np.array(sub_data1['District'])

ax.set_xlabel('Time')
ax.set_ylabel('IUCR')
ax.set_zlabel('District')

ax.scatter(x,y,z, marker="o", c = sub_data1["Clusters"], s=60, cmap="jet")
ax.view_init(azim=-20)
#print(ax.azim)
plt.show()

# Silhouette Analysis with 4 clusters
from yellowbrick.cluster import SilhouetteVisualizer
model = SilhouetteVisualizer(KMeans(4))
model.fit(sub_data1)
model.show()

# plotting with 5 clusters
km = KMeans(n_clusters=5)
km.fit(sub_data1)
y = km.predict(sub_data1)
labels = km.labels_
sub_data1['Clusters'] = y
sub_data1.head()



fig = plt.figure(figsize=(12,10))
ax = fig.add_subplot(111, projection='3d')
x = np.array(sub_data1['Normalized_time'])
y = np.array(sub_data1['IUCR'])
z = np.array(sub_data1['District'])

ax.set_xlabel('Time')
ax.set_ylabel('IUCR')
ax.set_zlabel('District')

ax.scatter(x,y,z, marker="o", c = sub_data1["Clusters"], s=60, cmap="jet")
ax.view_init(azim=-20)
#print(ax.azim)
plt.show()
# Silhouette Analysis with 5 clusters
from yellowbrick.cluster import SilhouetteVisualizer
model = SilhouetteVisualizer(KMeans(5))
model.fit(sub_data1)
model.show()

# Performance Evaluation using Silhouette Analysis
# The silhouette_score gives the average value for all the samples.
# This gives a perspective into the density and separation of the formed
# clusters
from sklearn.metrics import silhouette_samples, silhouette_score
n_clusters = 5
silhouette_avg = silhouette_score(sub_data1, labels)
print("For n_clusters =", n_clusters,
"The average silhouette_score is :", silhouette_avg)
# Compute the silhouette scores for each sample
sample_silhouette_values = silhouette_samples(sub_data1, labels)
silhouette_val = pd.DataFrame()
silhouette_val['sample'] = sample_silhouette_values
silhouette_val['labels'] = sub_data1['Clusters']
avg_list = []
list1 = []
for i in range(0,n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        cluster_silhouette_values = silhouette_val[labels == i]
        ith_cluster_silhouette_values = cluster_silhouette_values['sample'].values.tolist()
        avg_value = sum(ith_cluster_silhouette_values)/len(ith_cluster_silhouette_values)
        avg_list.append(avg_value)
        list1.append(i)
    
toplot = pd.DataFrame()
toplot['cluster'] = list1
toplot['avg'] = avg_list
"""# Silhouette Analysis with 3 clusters
from yellowbrick.cluster import SilhouetteVisualizer
model = SilhouetteVisualizer(KMeans(3))
model.fit(sub_data1)
model.show() """

"""# Silhouette Analysis with 6 clusters
from yellowbrick.cluster import SilhouetteVisualizer
model = SilhouetteVisualizer(KMeans(6))
model.fit(sub_data1)
model.show()"""







