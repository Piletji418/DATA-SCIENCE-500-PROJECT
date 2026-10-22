# Book Market Analytics – Books to Scrape

**Data Science 500 Assignment**  
Richfield Graduate Institution

## Project Overview

End-to-end data science solution that:

1. Scrapes the Books to Scrape catalogue with BeautifulSoup  
2. Cleans and structures the data  
3. Explores pricing, ratings and genre trends through visualisations  
4. Builds a linear regression model to estimate book price  
5. Communicates findings in a professional report  

## Deliverables

| File | Description |
|------|-------------|
| `Book_Market_Analytics.ipynb` | Complete Jupyter Notebook (acquisition → modelling) |
| `data/books_clean.csv` | Final cleaned analytical dataset (300 books) |
| `data/books_raw.csv` | Raw scraped data |
| `Book_Market_Analytics_Report.pdf` | Professional project report |
| `scrape_books.py` | Reproducible scraper script |
| `data/fig_*.png` | Visualisation figures used in the notebook & report |

## How to Re-run

```bash
# Optional: re-scrape (already done – 300 books saved)
python scrape_books.py

# Open and run the notebook
jupyter notebook Book_Market_Analytics.ipynb
```

Required packages (standard data-science stack):

```
pip install requests beautifulsoup4 lxml pandas scikit-learn matplotlib seaborn
```

## Dataset Summary

- **300 books** from the first 15 catalogue pages  
- Fields: title, price (GBP), star rating (1–5), genre, stock quantity, number of reviews, description length, etc.  
- Mean price ≈ £34.26 | Mean rating ≈ 2.92  

## Author

Student submission for Data Science 500.
