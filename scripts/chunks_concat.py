import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

folder_path = '/home/nathalia/Projects/funda/data/chunks'
all_files = os.listdir(folder_path)
dfs = []

for file in all_files:
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)
        df_chunk = pd.read_csv(file_path)
        dfs.append(df_chunk)

concatenated_df = pd.concat(dfs, ignore_index=True)

output_file_path = '/home/nathalia/Projects/funda/data/concatenated_data.csv'
concatenated_df.to_csv(output_file_path, index=False)