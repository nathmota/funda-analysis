
# Funda Properties Listings Data Analysis 

Nathalia V. M. de Oliveira - April, 2024.

### Analysis of the Dutch Real Estate Market, based on Properties Listings Available on *funda.nl* website.

## Project Objective:
1. Provide an overview of the real estate market in the Netherlands through online property listings.
2. Generate insights into the most valuable or cost-effective locations among provinces and cities.
3. Examine the profile of houses and the distribution of their most common characteristics.
4. Identify factors that may contribute to the variation in property prices.

## Data Overview

[Funda](https://www.funda.nl/) is a Dutch platform established over 20 years ago. According to their website, Funda is the largest platform connecting supply and demand in the real estate market of the Netherlands, with over 4 million unique visitors per month and hosting around 97% of the Dutch housing market.

According Funda's Terms and Conditions, scraping its website is only allowed for personal use, which means that any commercial use is prohibited.

- Data description:

The data has been collected on the 10th and 11th of April, 2024, which means that the dataset for this study case is regarding all the listings of available properties on sale **that period**.
The data was scraped from Funda using [FundaScraper](https://pypi.org/project/funda-scraper/) for Python, utilising the following arguments:
```
area=provincies  	  (list with all Dutch provincies)

want_to=buy       	  (regarding properties for sale)

find_past=False  	  (regarding properties still in the market)

page_start=1   	

n_pages=666   	 (whatever the number of properties returned in the search, there will be max 666 pages available for access, which means 9999 entries, since each page contains 15 listings). 

raw_data=True 	(to fetch the data without any preprocessing)
```

I decided to fetch the raw data and do all the preprocessing myself. But there is an option to set the argument to False to get beautifully processed and structured data.

[See the provinces](https://www.funda.nl/koop/bladeren/). 

![Location searching results](figures/fig1.png)


## Table of Contents

- [Results](results.md)
- [Figures](figures.md)
- [Reports](reports.md)

## Results

To see detailed results and insights, visit [Results](results.md).

## Figures

To view the generated figures and graphs, visit [Figures](figures.md).

## Reports

To read the complete reports, visit [Reports](reports.md).
