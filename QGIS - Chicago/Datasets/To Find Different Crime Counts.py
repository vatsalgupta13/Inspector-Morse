import pandas as pd
import numpy as np

df = pd.read_csv("2017-2019 Data.csv")
df.dropna(inplace = True)
# Keeping the rows with a particular condition (only violent crimes)
df_filtered = df[df['FBI Code'] < '05']
df_fil = df[df['FBI Code'] == '18']
df_filtered = df_filtered.append(df_fil , ignore_index = True) 
df_filtered = df_filtered.rename(columns = {"Primary Type" : "Primary","Census Tracts" : "Census"})
Diffcrimecount = pd.crosstab(df_filtered.Primary,df_filtered.Census).replace(0,np.nan).\
     stack().reset_index().rename(columns={0:'Count'})

# Exporting this dataframe to csv file 
export_csv = Diffcrimecount.to_csv (r'C:\Users\vatsa\Desktop\Different Crime Count.csv', index = None, header=True)
