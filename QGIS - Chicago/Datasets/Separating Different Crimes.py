import pandas as pd
import numpy as np

df = pd.read_csv("2017-2019 Data.csv")
df.dropna(inplace = True)
# Keeping the rows with a particular condition (only violent crimes and narcotic dealings)
# 04B is battery, 04A is assault, 18 is narcotics, 01A is homicide
df_homicide = df[df['FBI Code'] == '01A']
df_assault = df[df['FBI Code'] == '04A']
df_battery = df[df['FBI Code'] == '04B']
df_narcotics = df[df['FBI Code'] == '18'] 

# Exporting this dataframe to csv file 
export_csv = df_homicide.to_csv (r'C:\Users\vatsa\Desktop\Homicide.csv', index = None, header=True)
export_csv = df_assault.to_csv (r'C:\Users\vatsa\Desktop\Assault.csv', index = None, header=True)
export_csv = df_battery.to_csv (r'C:\Users\vatsa\Desktop\Battery.csv', index = None, header=True)
export_csv = df_narcotics.to_csv (r'C:\Users\vatsa\Desktop\Narcotics.csv', index = None, header=True)
