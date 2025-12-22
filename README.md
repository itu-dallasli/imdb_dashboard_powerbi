# TMDB 5000 Movie Data Visualization Project

## Project Overview
This project analyzes the TMDB 5000 movie dataset to uncover trends in film success, financial return, and actor networks. The final output is an interactive Power BI dashboard.

## Repository Structure
- `data/`: Contains raw input data and processed CSV files ready for Power BI.
- `scripts/`: Python scripts used for cleaning and EDA.
- `dashboard/`: The final Power BI (.pbix) file.

## Key Visualizations
Per the project guidelines, this dashboard includes:
1. **Scatter Plot**: Budget vs. Revenue analysis.
2. **Geospatial Map**: Global distribution of production countries.
3. **Network Graph**: Analysis of co-starring actors.
4. **Heatmap**: Correlation matrix of financial and popularity metrics.
5. **Time Series**: Analysis of movie releases over time.

## How to Reproduce
1. **Data Prep**:
   - Install requirements: `pip install pandas numpy`
   - Run the script: `python scripts/data_prep.py`
   - This will generate the necessary CSV files in the folder.
2. **Dashboard**:
   - Open `dashboard/Movie_Analysis.pbix` in Power BI Desktop.
   - If prompted, refresh the data source to point to the `data/processed/` folder on your machine.