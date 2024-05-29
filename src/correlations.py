import pandas as pd
from sklearn.preprocessing import LabelEncoder


COLUMNS_TO_DROP = ['url', 'address', 'zip_code', 'year_built', 'num_of_rooms', 'num_of_bathrooms', 'neighborhood_name',  'house_id', 'date_list', 'zip_code_complete', 'geo_location', 'located_floor', 'num_of_floors', 'num_of_toilets', 'city', 'provincie']
columns_to_encode = ['energy_label', 'heating', 'has_parking', 'has_garden', 'has_balcony', 'surrounding', 'house_type', 'num_of_bedrooms']
processed_data_path = '/home/nathalia/Projects/funda-analysis/src/data/processed/processed_data.csv'

df = pd.read_csv(processed_data_path)
df = df.drop(columns=COLUMNS_TO_DROP)

label_encoder = LabelEncoder()
for column in columns_to_encode:
    df[column + '_encoded'] = label_encoder.fit_transform(df[column])
df.drop(columns=columns_to_encode, inplace=True)
corr = df.corr()
print(corr)