from funda_scraper import FundaScraper
import pandas as pd

provincies = ["provincie-noord-holland", "provincie-zuid-holland", "provincie-zeeland", "provincie-noord-brabant", "provincie-utrecht", "provincie-flevoland", "provincie-friesland", "provincie-groningen", "provincie-drenthe", "provincie-overijssel", "provincie-gelderland", "provincie-limburg"]
want_to = "buy"
find_past = False
page_start = 1
n_pages = 20
# min_price = 200000
# max_price = 500000
raw_data = True
proviencies_dfs = []

for provincie in provincies:
    scraper = FundaScraper(area=provincie, want_to=want_to, find_past=find_past, page_start=page_start, n_pages=n_pages)
    df = scraper.run(raw_data=raw_data)
    proviencies_dfs.append(df)
proviencies_data = pd.concat(proviencies_dfs)
proviencies_data.to_csv('~/funda/data/', index=False)

