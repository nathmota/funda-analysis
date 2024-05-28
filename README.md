# Funda Properties Listings Data Analysis 

This project involves collecting, processing and analyzing data of the Dutch real estate market, based on properties listings available on [Funda](www.funda.nl) website.

For more details, see the [full documentation](docs/index.md).



## Repository Structure
- `data/`: Raw and processed data
- `src/`: Web scraping and data processing scripts.
- `docs/`: Complete project documentation and results.
- `README.md`: This file.
- `requirements.txt`: Project dependencies list.

## Run the Project

1. Clone the repository:
    ```bash
    git clone https://github.com/nathmota/funda-analysis.git
    ```
2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the web scraping script to collect data:
    ```bash
    python src/webscraping_script.py
    ```
4. Run the data processing script:
    ```bash
    python src/data_processing_script.py
    ```
5. Open the Power BI Desktop file and load the preprocessed_data for analysis and visualization:
    ```bash
    docs/reports/funda_report.pbix
    data/preprocessed/preprocessed_data.csv
    ```

## Results
For the results and visualizations see the [full documentation](docs/index.md).


