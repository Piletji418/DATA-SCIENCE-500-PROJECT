#!/usr/bin/env python3
"""
Scrape the entire Books to Scrape catalogue (books.toscrape.com)
Extracts: title, price, rating, availability, genre, upc, product_type, tax, num_reviews, description
Saves to data/books_raw.csv
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}


def get_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "lxml")


def parse_availability(text: str):
    """Return (status, quantity) from availability string."""
    text = text.strip()
    if "In stock" in text:
        qty_match = re.search(r"\((\d+)\s+available\)", text)
        qty = int(qty_match.group(1)) if qty_match else None
        return "In stock", qty
    return "Out of stock", 0


def scrape_book_detail(book_url: str) -> dict:
    """Scrape individual book page for extra fields."""
    try:
        soup = get_soup(book_url)
        # UPC, Product Type, Price (excl tax), Price (incl tax), Tax, Availability, Number of reviews
        table = soup.select_one("table.table.table-striped")
        info = {}
        if table:
            for row in table.select("tr"):
                th = row.select_one("th")
                td = row.select_one("td")
                if th and td:
                    info[th.get_text(strip=True)] = td.get_text(strip=True)

        # Genre (breadcrumb: Home > Books > Genre > Title)
        crumbs = soup.select("ul.breadcrumb li")
        if len(crumbs) >= 3:
            genre = crumbs[2].get_text(strip=True)
        else:
            genre = "Unknown"

        # Description
        desc_div = soup.select_one("#product_description")
        description = ""
        if desc_div:
            next_p = desc_div.find_next_sibling("p")
            if next_p:
                description = next_p.get_text(strip=True)

        # Parse availability quantity from detail table
        avail_raw = info.get("Availability", "")
        status_d, qty_d = parse_availability(avail_raw)

        return {
            "upc": info.get("UPC", ""),
            "product_type": info.get("Product Type", ""),
            "price_excl_tax": info.get("Price (excl. tax)", ""),
            "price_incl_tax": info.get("Price (incl. tax)", ""),
            "tax": info.get("Tax", ""),
            "num_reviews": info.get("Number of reviews", "0"),
            "genre": genre,
            "description": description,
            "detail_status": status_d,
            "detail_qty": qty_d,
        }
    except Exception as e:
        print(f"  Detail error for {book_url}: {e}")
        return {
            "upc": "", "product_type": "", "price_excl_tax": "",
            "price_incl_tax": "", "tax": "", "num_reviews": "0",
            "genre": "Unknown", "description": "",
            "detail_status": "", "detail_qty": None
        }


def scrape_catalogue(max_pages: int = 50, delay: float = 0.3) -> pd.DataFrame:
    """Scrape all catalogue listing pages and optionally detail pages."""
    records = []
    page = 1

    while page <= max_pages:
        url = CATALOGUE_URL.format(page)
        print(f"Scraping page {page} ...")
        try:
            soup = get_soup(url)
        except Exception as e:
            print(f"Failed to fetch page {page}: {e}")
            break

        articles = soup.select("article.product_pod")
        if not articles:
            print("No more books found.")
            break

        for art in articles:
            # Title
            title_tag = art.select_one("h3 a")
            title = title_tag.get("title", title_tag.get_text(strip=True)) if title_tag else ""
            rel_link = title_tag.get("href", "") if title_tag else ""
            book_url = urljoin(BASE_URL + "catalogue/", rel_link)

            # Price
            price_tag = art.select_one("p.price_color")
            price_str = price_tag.get_text(strip=True) if price_tag else ""

            # Rating
            rating_tag = art.select_one("p.star-rating")
            rating_word = ""
            if rating_tag:
                classes = rating_tag.get("class", [])
                for c in classes:
                    if c != "star-rating":
                        rating_word = c
                        break

            # Availability (from listing)
            avail_tag = art.select_one("p.instock.availability")
            avail_text = avail_tag.get_text(strip=True) if avail_tag else ""
            status, qty = parse_availability(avail_text)

            # Get detail info
            detail = scrape_book_detail(book_url)
            time.sleep(delay * 0.5)  # polite pause on detail

            records.append({
                "title": title,
                "price_str": price_str,
                "rating_word": rating_word,
                "availability_status": status,
                "availability_qty": qty,
                "book_url": book_url,
                **detail
            })

        page += 1
        time.sleep(delay)

    df = pd.DataFrame(records)
    print(f"\nScraped {len(df)} books.")
    return df


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = scrape_catalogue(max_pages=50, delay=0.25)
    out_path = "data/books_raw.csv"
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Saved raw data to {out_path}")
    print(df.head())
    print(df.columns.tolist())
