# split data so that its under github limit 100mb
import pandas as pd

df = pd.read_csv('Traffic_Collisions_Open_Data_Complete.csv')

half = len(df) // 2

df.iloc[:half].to_csv('Traffic_Collisions_Open_Data_1.csv', index=False)
df.iloc[half:].to_csv('Traffic_Collisions_Open_Data_2.csv', index=False)
