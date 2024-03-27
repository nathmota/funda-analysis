import os
import pandas as pd

folder_path = '/home/nathalia/Projects/funda/chunks'
all_files = os.listdir(folder_path)
dfs = []

for file in all_files:
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)
        df_chunk = pd.read_csv(file_path)
        dfs.append(df_chunk)

concatenated_df = pd.concat(dfs, ignore_index=True)
rows_with_null = concatenated_df.isnull().any(axis=1).sum()

print(concatenated_df.info())