import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

raw_folder_path = 'my_path/funda-analysis/data/raw/'
processed_folder_path = 'my_path/funda-analysis/data/processed/'
chunk_folder_path = f'{raw_folder_path}chunks/'
provincie_folders = [f.path for f in os.scandir(chunk_folder_path) if f.is_dir()]

for provincie_folder in provincie_folders:
    csv_files = [file.path for file in os.scandir(provincie_folder) if file.name.endswith('.csv')]  # gathering the chunk files for each province
    dfs = []
    for csv_file in csv_files:
        df_chunk = pd.read_csv(csv_file)
        dfs.append(df_chunk)
    concatenated_df = pd.concat(dfs, ignore_index=True)

    output_csv_path = os.path.join(provincie_folder, 'provincie_data_final.csv')  # generating one single csv for the province
    concatenated_df.to_csv(output_csv_path, index=False)

provincie_csv_files = [os.path.join(provincie_folder, 'provincie_data_final.csv') for provincie_folder in provincie_folders]  # joining the province's single csv
processed_data = pd.concat([pd.read_csv(csv_file) for csv_file in provincie_csv_files], ignore_index=True)

big_final_csv_path = f'{processed_folder_path}{processed_data}.csv'
processed_data.to_csv(big_final_csv_path, index=False)