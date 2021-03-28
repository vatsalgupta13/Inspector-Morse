import pandas as pd
import numpy as np

# Importing the dataset
df = pd.read_csv("2017-2019 Data.csv")

# Dropping rows with null values
df.dropna(inplace = True)
# Keeping the rows with a particular condition (only violent crimes)
df_filtered = df[df['FBI Code'] < '05']
# Exporting this dataframe to csv file 
export_csv = df_filtered.to_csv (r'C:\Users\vatsa\Desktop\2017 - 2019 Crime.csv', index = None, header=True)
