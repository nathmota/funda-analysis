# Funda Properties Listings Data Analysis 🏡

![Report preview](docs/figures/report_preview.png)

This project involves collecting, processing and analyzing data of the Dutch real estate market, based on properties listings available on [Funda](https://www.funda.nl/) website.

The ETL process is carried out as follows:
- Extraction: via Web Scraping using [Funda Scraper](https://github.com/whchien/funda-scraper)
- Cleaning/pre-processing: executed in chunks, using:
    - Numpy/Pandas for cleaning
    - Beautiful Soup for scraping some additional data directly from Funda
    - Geopy for obtaining geolocations
- Transformation:
  Power BI for Exploratory Data Analysis and generating visualizations


For more details, see the [full documentation](https://nathmota.github.io/funda-analysis/).

## Repository Structure
- `data/`: Raw, processed and external data
- `src/`: Web scraping and data processing scripts.
- `docs/`: Complete project documentation and results, reports and figures.
- `README.md`: This file.
- `requirements.txt`: Project dependencies list.

## Run the Project
For running this project, you have to be installed: Python3, the dependencies on requirements.txt, and Power BI Desktop.
Steps:

1. Clone the repository:
    ```bash
    # Go to your project diretory
    cd project_local_path/projects
    # Clone this repository
    $ git clone https://github.com/nathmota/funda-analysis.git
    # Go into the repository
    $ cd funda-analysis
    ```
2. Install the dependencies using pip or you preferred virtual environment:
    ```bash
    pip install -r requirements.txt
    ```
3. Open the [Funda Scraper](https://github.com/whchien/funda-scraper), set the arguments as your needs, and your file path.
   For this project, the follow arguments has been used:
   ```bash
    raw_folder_path = "project_path/funda-analysis/data/raw/"
    provincies = ["provincie-drenthe", "provincie-groningen", "provincie-flevoland", "provincie-friesland", "provincie-zeeland", "provincie-limburg", "provincie-utrecht", "provincie-overijssel","provincie-gelderland","provincie-noord-brabant","provincie-noord-holland","provincie-zuid-holland"]
    want_to = "buy"
    find_past = False
    n_pages = 50        # records every 50 pages (750 entries) to avoid loss in case of execution failure
    final_page = 2000
    entries_per_page = 15
    raw_data = True
    ```
   If need, check [Funda Scraper](https://github.com/whchien/funda-scraper) documentation and/or [Funda](https://www.funda.nl/) website.
   
4. Run the web scraping script to collect data:
    ```bash
    python src/webscraping_script.py
    ```
5. Open the [data processing script](src/data_processing_script.py), set the arguments as your needs, and your file path;
 
6. Run the data processing script:
    ```bash
    python src/data_processing_script.py
    ```
7. Open the [chunks concatenator script](src/chunks_concat.py), set the arguments as your needs, and your file path;
   `src/chunks_concat.py`

8. Run the chunks concatenator script:
    ```bash
    python src/chunks_concat.py
    ```
9. Open the .pbix file on Power BI Desktop and load the processed data for analysis and visualization:
    ```bash
    docs/reports/funda_report.pbix
    data/preprocessed/processed_data.csv
    ```

## Results
For the results and visualizations see the [full documentation](https://nathmota.github.io/funda-analysis/).
