from funda_scraper import FundaScraper

#provincies = [provincie-noord-holland, provincie-zuid-holland, provincie-zeeland, provincie-noord-brabant, provincie-utrecht, provincie-flevoland, provincie-friesland, provincie-groningen, provincie-drenthe, provincie-overijssel, provincie-gelderland, provincie-limburg]
provincies = ["provincie-limburg"]
want_to = "rent"
find_past = False
page_start = 1
n_pages = 10
min_price = 500
max_price = 2000
raw_data = True

for provincie in provincies:
    scraper = FundaScraper(area=provincie, want_to=want_to, find_past=find_past, page_start=page_start, n_pages=n_pages, min_price=min_price, max_price=max_price)
    df = scraper.run(raw_data=raw_data)
    df.to_csv(f"{provincie}.csv", index=False)
    
