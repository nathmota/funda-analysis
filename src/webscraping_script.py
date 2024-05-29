from funda_scraper import FundaScraper
import pandas as pd
import os


raw_folder_path = '/home/nathalia/Projects/funda-analysis/src/data/raw/'  
provincies = ["provincie-drenthe", "provincie-groningen", "provincie-flevoland", "provincie-friesland", "provincie-zeeland", "provincie-limburg", "provincie-utrecht", "provincie-overijssel","provincie-gelderland","provincie-noord-brabant","provincie-noord-holland","provincie-zuid-holland"]
want_to = "buy"
find_past = False
n_pages = 50        # records every 50 pages (750 entries) to avoid loss in case of execution failure
final_page = 2000
entries_per_page = 15
raw_data = True

for provincie in provincies:
    output_file_path = os.path.join(raw_folder_path, f'{provincie}.csv')
    if os.path.exists(output_file_path):
        proviencies_data = pd.read_csv(output_file_path)
        #print(len(proviencies_data),provincie, '\n')
    else:
        proviencies_data = pd.DataFrame()
    for page_start in range(0, final_page, n_pages):
        page_start = len(proviencies_data) // entries_per_page + 1 
        scraper = FundaScraper(area=provincie, want_to=want_to, find_past=find_past, page_start=page_start, n_pages=n_pages)
        df = scraper.run(raw_data=raw_data)
        if df.empty:
            break
        else:
            proviencies_data = pd.concat([proviencies_data, df], ignore_index=True)
            proviencies_data.to_csv(output_file_path, index=False)
            print(provincie)

print("Data recorded successfully.")