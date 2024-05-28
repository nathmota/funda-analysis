# Funda Properties Listings Data Analysis 

This project involves collecting, processing and analyzing data of the Dutch real estate market, based on properties listings available on [Funda](www.funda.nl) website.

For more details, see the [full documentation](docs/index.md).

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
    # Clone this repository
    $ git clone https://github.com/nathmota/funda-analysis.git
    # Go into the repository
    $ cd funda-analysis
    ```
2. Install the dependencies using pip or you own virtual environment:
    ```bash
    pip install -r requirements.txt
    ```
3. Open the web scraping script, set the arguments as your needs, and your file path.
   For this project, the follow arguments has been used:
   ```bash
        folder_path = '/your_path/funda/data/'  
        provincies = ["provincie-drenthe", "provincie-groningen", "provincie-flevoland", "provincie-friesland", "provincie-zeeland", "provincie-limburg", "provincie-utrecht", "provincie-overijssel","provincie-gelderland","provincie-noord-brabant","provincie-noord-holland","provincie-zuid-holland"]
        want_to = "buy"
        find_past = False
        n_pages = 50       
        final_page = 2000
        entries_per_page = 15
        raw_data = True
    ```
   If need, check [Funda Scraper](https://github.com/whchien/funda-scraper) documentation.
   
4. Run the web scraping script to collect data:
    ```bash
    python src/webscraping_script.py
    ```
5. Open the data processing script, set the arguments as your needs, and your file path;
 
6. Run the data processing script:
    ```bash
    python src/data_processing_script.py
    ```
7. Open the chunks concatenator script, set the arguments as your needs, and your file path;
   
8. Run the chunks concatenator script:
    ```bash
    python src/chunks_concat.py
    ```
9. Open the .pbix file and load the processed data for analysis and visualization:
    ```bash
    docs/reports/funda_report.pbix
    data/preprocessed/processed_data.csv
    ```

## Results
For the results and visualizations see the [full documentation](docs/index.md).

![Report_cover_page](figures/cover_page.png)
