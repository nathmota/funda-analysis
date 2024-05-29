
# Funda Properties Listings Data Analysis 

Nathalia V. M. de Oliveira - April, 2024.

### Analysis of the Dutch Housing Market, based on Properties Listings Available on *funda.nl* website.

## Project Objective:
1. Provide an overview of the housing market in the Netherlands through online property listings;
2. Generate insights into the most valuable or cost-effective locations among provinces and cities;
3. Examine the profile of houses and the distribution of their most common features;
4. Identify factors that may contribute to the variation in property prices.

## Data Source

[Funda](https://www.funda.nl/) is a Dutch platform established over 20 years ago. According to their website, Funda is the largest platform connecting supply and demand in the real estate market of the Netherlands, with over 4 million unique visitors per month and hosting around 97% of the Dutch housing market.

According Funda's Terms and Conditions, scraping its website is only allowed for personal use, which means that any commercial use is prohibited.


## Collecting the Data

/src/webscrapin_script.py

The data were scraped from Funda using [FundaScraper](https://github.com/whchien/funda-scraper) for Python.
There are several different set of arguments that can generate diverse searches.
For this project, the following arguments has been used:

```
area=provincie ----------- # To fetch data by province (you can also search for city, neighborhood or postcode);
want_to=buy -------------- # Regarding properties for sale (you can switch for "rent");
find_past=False ---------- # Regarding properties available at the moment, not already sold;
page_start=1 ------------- # Starting page;
n_pages = 50 ------------- # Regarding the amount of pages to be fetched;
raw_data=True ------------ # To fetch the data without any preprocessing.
```
I decided to fetch the raw data and do all the preprocessing myself. But there is an option to set the argument to False to get beautifully processed and structured data.

About number of pages: 
Although the search by province may return 15.000 results, for instance, Funda only makes accessible max 666 pages, as you can see bellow, which means 9990 entries, since each page contains 15 listings.

[See the provinces results.](https://www.funda.nl/koop/bladeren/). 

![Search results](/docs/figures/fig1.png)


Then, every 50 pages (or 750 entries), the script scrapes and records the data into a province csv.

### Data Overview

The data was collected on the 10th and 11th of April, 2024, which means that the dataset for this case study includes all the housing property listings **available** for sale during **that period**.

The raw scraped content contains following information:

1. url
2. price
3. address
4. description
5. listed_since
6. zip_code
7. size
8. year_built
9. living_area
10. kind_of_house
11. building_type
12. num_of_rooms
13. num_of_bathrooms
14. layout
15. energy_label
16. insulation
17. heating
18. ownership
19. exteriors
20. parking
21. neighborhood_name
22. date_list
23. date_sold
24. term
25. price_sold
26. last_ask_price
27. last_ask_price_m2
28. city

And they look like this:

![raw data](/docs/figures/raw1.png)

You can also check it up on /data/raw/

It’s possible to see that it is going to take a lot of work.


## Processing the Data

/src/data_processing_script.py

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
