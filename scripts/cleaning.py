import pandas as pd
import re
import numpy as np
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import requests
from bs4 import BeautifulSoup
from funda_scraper.config.core import config

COLUMNS_TO_DROP = ['photo', 'descrip', 'log_id', 'insulation', 'ownership', 'building_type', 'last_ask_price_m2', 'date_list', 'listed_since', 'kind_of_house', 'last_ask_price', 'living_area']
UNMISSABLE_COLUMNS = ['url', 'price', 'address','listed_since', 'zip_code', 'size', 'year', 'layout','city']

chunk_size = 300
chunk_index = 1
pre_df = pd.read_csv('/home/nathalia/Projects/funda/data/funda_raw_data.csv') 

def general_cleaning(df):
    # dropping rows with missing values in essential columns
    for label in UNMISSABLE_COLUMNS:
        df = df.dropna(subset=[label])
    # removing duplicates
    df = df.drop_duplicates()
    # dropping unused columns
    df = df.drop(columns=COLUMNS_TO_DROP)
    return df

def clean_size(df):
    df['size'] = df['size'].str.extract(r'(\d+)')
    df = df.dropna(subset='size')
    df['size'] =  df['size'].astype(int)
    df = df.rename(columns={'size': 'size_m2'})
    return df    

def clean_price(df):
    df['price'] = df['price'].str.replace('.', '').str.extract(r'(\d+)')
    df = df.dropna(subset='price')
    df['price'] = df['price'].astype(int)
    return df

def clean_price_m2(df):
    df['price_m2'] =  round(df['price'] / df['size_m2']).astype(int)
    return df

def clean_year(df):
    df['year'] = df['year'].astype(str).str.slice(-4).astype(int)
    df = df.rename(columns={'year': 'year_built'})
    return df

def clean_house_age(df):
    def age(year_built):
        return datetime.now().year - year_built
    df['house_age'] = df['year_built'].apply(age)
    return df

def clean_energy_label(df):
    df['energy_label'] = df['energy_label'].str.split(' ').str[0]
    df.loc[df['energy_label'].str.contains('A+'), 'energy_label'] = 'A+'
    return df

def get_heating(x):
    patterns = {
        r'Cv-ketel[s]?': 'boiler',
        r'Stadsverwarming[s]?': 'district_heating',
        r'Blokverwarming[s]?': 'block_heating',
        r'Gaskachels[s]?': 'gas_heating',
        r'warmtepomp[s]?': 'heat_pump',
        r'Elektrische[s]?': 'electric_heating',
    }      
    for pattern, label in patterns.items():
        if re.search(pattern, x, re.IGNORECASE):
            return label   
    return 'other'  

def clean_heating(df):
    df['heating'] = df['heating'].apply(lambda x: get_heating(x))
    return df

def clean_parking(df):
    # public or paid are given as 'no'
    df['parking_spot'] = 'no'
    df['parking_spot'] = np.where(df['parking'].str.contains(r'openbaar|Betaald|niet|per maand|Parkeervergunningen', case=False), 'no',
                    np.where(df['parking'].str.contains(r'Vrijstaande|Inpandig|Carport|Parkeerkelder|Aangebouwde|eigen|Parkeerplaats|garage', case=False), 'yes', 
                    df['parking_spot']))
    df = df.drop(columns='parking')
    df = df.rename(columns={'parking_spot': 'has_parking'})
    return df

def get_surrounding(x):
    patterns = {
        r'centrum[s]?': 'centrum',
        r'rustige[s]?': 'quiet_street',
        r'woonwijk[s]?': 'residential_area',
        r'drukke[s]?': 'busy_area',
        r'park[s]?': 'park',
        r'bosrand[s]?|bosrijk[s]?|tuinplaats[s]?': 'woody_area',
        r'water[s]?': 'water',
    }           
    for i in range(1, len(x.split(' '))):
        try:
            y = x.split(' ')[i]
        except:
            #return x
            return x
        for pattern, label in patterns.items():
            if re.search(pattern, y, re.IGNORECASE):
                return label
    return 'other'

def get_garden(y):
    pattern = re.compile(r'[Aa]chtertuin|[Vv]oortuin')
    if 'Tuin' in y:
        x = y.split(r'Tuin')
        if pattern.search(x[1]):
            return 'yes'
        return 'no'
    if pattern.search(y):
        return 'yes'
    return 'no'

def clean_exteriors(df):
    df['has_balcony'] = 'no'
    df.loc[df['exteriors'].str.contains(r'balkon|terras', case=False), 'has_balcony'] = 'yes'
    # has_garden
    df['has_garden'] = 'no'
    df['has_garden'] = df['exteriors'].apply(lambda x: get_garden(x))
    df['surrounding'] = df['exteriors'].apply(lambda x: get_surrounding(x))
    df = df.drop(columns='exteriors')
    return df

def get_house_type(x):
    patterns = {
        r'appartement[s]?': 'apartment',
        r'huis[s]?': 'house',
    }
    x = x.split('/')[-2].split('-')[0]
    for pattern, label in patterns.items():
            if re.search(pattern, x, re.IGNORECASE):
                return label
    return 'other'

def get_house_id(x):
    return x.split('/')[-2].split('-')[1]

def get_script_element(url): 
    response = requests.get(url,headers=config.header, verify=True)     
    if response.status_code == 200:    
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            script_text = soup.find(lambda tag: tag.name=='script' and tag.has_attr('data-test-gtm-script')).get_text()  
            return script_text                         
        except AttributeError:            
            print("Script element not found.")
            return np.nan
    return np.nan

def time_difference(text):
    time_difference_string = text
    current_date = datetime.now()
    if "jaren" in time_difference_string:
        time_unit = "year"   
    elif "maanden" in time_difference_string:
        time_unit = "month"         
    elif "weken" in time_difference_string:
        time_unit = "week"
    elif "dagen" in time_difference_string:
        time_unit = "day"
    elif "uur" in time_difference_string:
        time_unit = "hour"
    elif "minuten" in time_difference_string:
        time_unit = "minute"
    elif "seconden" in time_difference_string:
        time_unit = "second"    
    elif "vandaag" in time_difference_string:
        time_unit = "today"    
    elif "gisteren" in time_difference_string:
        time_unit = "yesterday"   
    else:
         raise ValueError("Unsupported time format")

    try:   
        units_ago = re.findall(r'(\d+)', time_difference_string)
    except ValueError:
        pass
    # Create a timedelta based on the time unit and number of units
    if time_unit == "year":
        time_difference = timedelta(days=365 * int(units_ago[0]))   
    elif time_unit == "month":
        time_difference = timedelta(days=30 * int(units_ago[0]))  # Approximate number of days in a month         
    elif time_unit == "week":
        time_difference = timedelta(weeks=int(units_ago[0]))
    elif time_unit == "day":
        time_difference = timedelta(days=int(units_ago[0]))
    elif time_unit == "hour":
        time_difference = timedelta(hours=int(units_ago[0]))
    elif time_unit == "minute":
        time_difference = timedelta(minutes=int(units_ago[0]))   
    elif time_unit == "second":
        time_difference = timedelta(seconds=int(units_ago[0]))       
    elif time_unit == "today":
        return current_date     
    elif time_unit == "yesterday":
        return current_date - timedelta(days=1)

    else:
        raise ValueError("Unsupported time format")
    # Calculate the date by subtracting the time difference from the current date    
    return current_date - time_difference   

def get_date_list(x):
    # Mapping Dutch month to English
    def date_formatting(date_text):
        date_formatting = {
            "januari": "January",
            "februari": "February",
            "maart": "March",
            "april": "April",
            "mei": "May",
            "juni": "June",
            "juli": "July",
            "augustus": "August",
            "september": "September",
            "oktober": "October",
            "november": "November",
            "december": "December"
        }

        for dutch_month, english_month in date_formatting.items():
            if dutch_month in date_text:
                text = date_text.replace(dutch_month, english_month)
                date_object = datetime.strptime(text, '%d %B %Y')
                date_str = date_object.strftime('%Y-%m-%d')
                return date_str

    if isinstance(x, str):
        match_date = re.search(r"'aangebodensinds' : '(.+?)'", x)  
        date = match_date.group(1).lower()          
        pattern_date = r'\d+\s+\w+\s+\d+'
        pattern_period = r'weken|maanden|jaren|vandaag|gisteren'                      
        if re.findall(pattern_date, date):
            date_text = re.findall(pattern_date, date)
            date_formatted = date_formatting(date_text[0])
            return date_formatted
        elif re.findall(pattern_period, date):
            #period = period_formatting(date)
            date = time_difference(date)
            date_str = date.strftime('%Y-%m-%d')
            return date_str
    return x

def get_provincie(x):
    if isinstance(x, str):
        match_prov = re.search(r"'provincie' : '(.+?)'", x)           
        provincie = match_prov.group(1)  
        return provincie
    return x

def clean_url(df):
    # house_type
    df['house_type'] = df['url'].apply(lambda x: get_house_type(x)).astype(str)
    # house_id
    df['house_id'] = df['url'].apply(lambda x: get_house_id(x)).astype(str)
    # date_list and provincie
    df['date_list']  = df['url'].apply(lambda x: get_script_element(x)).apply(get_date_list)
    df['provincie'] = df['url'].apply(lambda x: get_script_element(x)).apply(get_provincie)
    df = df.dropna(subset=['date_list'])    #if date_list is nan that means the url is not up
    return df

def get_digit_floor(x):
    x = x.split(r'woonla')
    if len(x) >= 3:
        if re.findall(r'\d+', x[2]):
         return re.findall(r'\d+', x[2])[0]
        elif re.findall(r'Begane', x[2]):
            return '1'
        else:
            return x[2]            
        
    elif len(x) == 1:
        if re.findall(r'\d+', x[0]):
         return re.findall(r'\d+', x[0])[0]
        elif re.findall(r'Begane', x[0]):
            return '1'
        else:
            return x[0]
    else:
        return x[0]

def clean_layout(df):   
    # num_of_floors
    df['num_of_floors'] = df['layout'].str.split(r'woonla[s]?').str[1].str.extract(r'(\d+)') 

    # located_floor
    # ground floor is given as '1'
    df['located_floor'] = df['layout'].apply(lambda x: get_digit_floor(x))
    df['located_floor'] = pd.to_numeric(df['located_floor'], errors='coerce')                           #non-numeric to NaN
    df.loc[(df['located_floor'].isnull()) & (df['house_type'] == 'house'), 'located_floor'] = 1       # fill NaN with right value
    df.loc[(df['located_floor'].isnull()), 'located_floor'] = 'unknown'
    df['located_floor'] = df['located_floor'].astype(str).str.replace(r'\..*', '', regex=True)  
    #df['located_floor'] = pd.to_numeric(df['located_floor'], errors='coerce', downcast='integer')  doesn't work
    #df['located_floor'] = pd.to_numeric(df['located_floor'], errors='coerce').astype(int)          doesn't work

    # num_of_rooms
    df.loc[:, 'num_of_rooms'] = df['layout'].str.split(r'kamer[s]?').str[1]

    # num_of_bedrooms
    df.loc[:, 'num_of_bedrooms'] = df['layout'].str.split(r'slaapkamer[s]?').str[0].str.split('(').str[1]

    # num_of_bathrooms
    df['num_of_bathrooms'] = df['layout'].str.split(r'badkamers').str[1].str.extract(r'(\d+)')

    # nym_of_toilets
    df['num_of_toilets'] = df['layout'].str.split(r'badkamer').str[2].str.extract(r'(\d+)') 

    df = df.drop(columns='layout') 
    print('layout ok')
    return df

def get_zip_code(x):
    x =  x.split(' ')
    code = x[0]+x[1]
    return code

def clean_zip_code(df):
    # zip_code_complete includes city
    df['zip_code_complete'] = df['zip_code']
    # zip code 0000 AZ
    df['zip_code'] = df['zip_code_complete'].apply(lambda x: get_zip_code(x))
    return df

def get_geolocation(x):
    try:
        geolocator = Nominatim(user_agent="my_app", timeout=2)
        t1 = datetime.now()
        try:
            location = geolocator.geocode(x)
        except ConnectionError:
            return np.nan
        return (location.latitude, location.longitude)
    except AttributeError:
        return np.nan

def clean_address(df):
    df['address'] = df['address'].str.extract(r'(.+\d+)')
    df['address'] = df['address'] +  ' ' + df['zip_code_complete']
    df['geo_location'] = df['zip_code'].apply(lambda x: get_geolocation(x))
    return df



df = general_cleaning(pre_df)
df.to_csv('df_dropped_cols.csv', index=False)
df = pd.read_csv('/home/nathalia/Projects/funda/df_dropped_cols.csv', chunksize=chunk_size)

for chunk in df:
    chunk = (
        chunk.pipe(clean_size)
            .pipe(clean_price)
            .pipe(clean_price_m2)   #transformation
            .pipe(clean_year)       
            .pipe(clean_house_age)  #transformation
            .pipe(clean_energy_label)
            .pipe(clean_heating)
            .pipe(clean_parking)
            .pipe(clean_exteriors)
            .pipe(clean_url)        
            .pipe(clean_layout)
            .pipe(clean_zip_code)
            .pipe(clean_address)
    )
    filename = f'chunk_{chunk_index}.csv'
    file_path = f'/home/nathalia/Projects/funda/data/chunks/{filename}'
    chunk.to_csv(file_path, index=False)    
    chunk_index += 1







