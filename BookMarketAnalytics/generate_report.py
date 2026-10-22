#!/usr/bin/env python3
"""Generate a professional project report PDF for the Data Science 500 assignment."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, ListFlowable, ListItem, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUTPUT = "Book_Market_Analytics_Report.pdf"
DATA_DIR = "data"

# Colours
BLUE = HexColor("#003366")
LIGHT_BLUE = HexColor("#1a5276")
ACCENT = HexColor("#2980b9")
GREY = HexColor("#555555")
LIGHT_GREY = HexColor("#f4f6f7")

def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CoverTitle", fontName="Helvetica-Bold", fontSize=22,
        textColor=BLUE, alignment=TA_CENTER, spaceAfter=8, leading=26
    ))
    styles.add(ParagraphStyle(
        name="CoverSub", fontName="Helvetica", fontSize=12,
        textColor=GREY, alignment=TA_CENTER, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name="SectionHead", fontName="Helvetica-Bold", fontSize=14,
        textColor=BLUE, spaceBefore=16, spaceAfter=8, borderPadding=3
    ))
    styles.add(ParagraphStyle(
        name="SubHead", fontName="Helvetica-Bold", fontSize=11,
        textColor=LIGHT_BLUE, spaceBefore=10, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name="BodyJust", fontName="Helvetica", fontSize=10,
        alignment=TA_JUSTIFY, spaceAfter=6, leading=14
    ))
    styles.add(ParagraphStyle(
        name="BulletText", fontName="Helvetica", fontSize=10,
        leftIndent=12, spaceAfter=3, leading=13
    ))
    styles.add(ParagraphStyle(
        name="TableHeader", fontName="Helvetica-Bold", fontSize=9,
        textColor=white, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        name="TableCell", fontName="Helvetica", fontSize=8.5,
        leading=11
    ))
    styles.add(ParagraphStyle(
        name="Caption", fontName="Helvetica-Oblique", fontSize=8.5,
        textColor=GREY, alignment=TA_CENTER, spaceBefore=3, spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name="Footer", fontName="Helvetica", fontSize=8,
        textColor=GREY, alignment=TA_CENTER
    ))
    return styles


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    page_num = canvas.getPageNumber()
    text = f"Book Market Analytics – Data Science 500  |  Page {page_num}"
    canvas.drawCentredString(A4[0] / 2, 12 * mm, text)
    canvas.restoreState()


def create_report():
    styles = build_styles()
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=18 * mm
    )
    story = []

    # ========== COVER ==========
    story.append(Spacer(1, 30 * mm))
    story.append(Paragraph("RICHFIELD GRADUATE INSTITUTION", styles["CoverSub"]))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("Data Science 500 Assignment", styles["CoverTitle"]))
    story.append(Paragraph("Book Market Analytics – Books to Scrape", styles["CoverTitle"]))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph(
        "An End-to-End Data Science Project:<br/>Web Scraping, Cleaning, Visualisation &amp; Predictive Modelling",
        styles["CoverSub"]
    ))
    story.append(Spacer(1, 15 * mm))

    cover_info = [
        ["Project Focus", "Pricing & Rating Analysis of Online Book Catalogue"],
        ["Data Source", "https://books.toscrape.com"],
        ["Dataset Size", "300 books (15 catalogue pages)"],
        ["Techniques", "BeautifulSoup, Pandas, Seaborn, Scikit-learn Linear Regression"],
        ["Deliverables", "Jupyter Notebook · Cleaned CSV · Professional Report"],
    ]
    t = Table(cover_info, colWidths=[40 * mm, 120 * mm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), BLUE),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
        ("BOX", (0, 0), (-1, -1), 0.5, ACCENT),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, HexColor("#cccccc")),
    ]))
    story.append(t)
    story.append(Spacer(1, 20 * mm))
    story.append(Paragraph(
        "<i>This report accompanies the complete Jupyter Notebook and cleaned dataset submitted for the assignment.</i>",
        styles["CoverSub"]
    ))
    story.append(PageBreak())

    # ========== 1. INTRODUCTION ==========
    story.append(Paragraph("1. Introduction &amp; Project Objectives", styles["SectionHead"]))
    story.append(Paragraph(
        "A publishing analytics team requires insight into the factors that influence book prices and ratings "
        "on online catalogues. This project simulates a real-world junior data-scientist workflow by independently "
        "acquiring structured product data from the Books to Scrape sandbox website, transforming it into an "
        "analytical dataset, exploring catalogue behaviour through visualisations, and building a linear regression "
        "model that estimates book price from publicly available attributes.",
        styles["BodyJust"]
    ))
    story.append(Paragraph(
        "The end-to-end pipeline covers five stages required by the assignment brief: (1) data acquisition via "
        "web scraping, (2) data cleaning and preparation, (3) exploratory visualisation, (4) predictive modelling, "
        "and (5) professional communication of findings and recommendations.",
        styles["BodyJust"]
    ))

    # ========== 2. DATA ACQUISITION ==========
    story.append(Paragraph("2. Data Acquisition (Web Scraping)", styles["SectionHead"]))
    story.append(Paragraph(
        "The full catalogue on books.toscrape.com contains 1 000 books across 50 pages. Using the Python libraries "
        "<b>requests</b> and <b>BeautifulSoup</b> (lxml parser), a custom scraper was developed that:",
        styles["BodyJust"]
    ))
    bullets = [
        "Iterates through catalogue listing pages to extract title, price string, star-rating word, and availability status.",
        "Follows each product link to the detail page to obtain genre (from breadcrumb), UPC, tax, number of reviews, stock quantity, and product description.",
        "Applies polite request delays and robust error handling for reproducibility.",
    ]
    for b in bullets:
        story.append(Paragraph(f"• {b}", styles["BulletText"]))

    story.append(Paragraph(
        "A total of <b>300 books</b> (15 pages) were collected – exceeding the minimum requirement of approximately "
        "100–200 products. The raw scrape is stored in <font face='Courier'>data/books_raw.csv</font>.",
        styles["BodyJust"]
    ))

    fields_data = [
        [Paragraph("<b>Field</b>", styles["TableHeader"]),
         Paragraph("<b>Source</b>", styles["TableHeader"]),
         Paragraph("<b>Example</b>", styles["TableHeader"])],
        ["title", "Listing page", "A Light in the Attic"],
        ["price_str", "Listing page", "£51.77"],
        ["rating_word", "Listing page (CSS class)", "Three"],
        ["availability_status", "Listing / Detail", "In stock"],
        ["stock_qty", "Detail page", "22"],
        ["genre", "Detail breadcrumb", "Poetry"],
        ["num_reviews", "Detail table", "0"],
        ["description", "Detail page", "Full product blurb…"],
    ]
    ft = Table(fields_data, colWidths=[40 * mm, 50 * mm, 70 * mm])
    ft.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GREY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_GREY]),
        ("BOX", (0, 0), (-1, -1), 0.6, BLUE),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, HexColor("#cccccc")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(ft)
    story.append(Paragraph("Table 1 – Key fields extracted for each book", styles["Caption"]))

    # ========== 3. DATA CLEANING ==========
    story.append(Paragraph("3. Data Cleaning &amp; Preparation", styles["SectionHead"]))
    story.append(Paragraph(
        "Raw scraped text was converted into a clean analytical dataset suitable for modelling. The principal "
        "transformations are summarised below.",
        styles["BodyJust"]
    ))

    clean_data = [
        [Paragraph("<b>Field</b>", styles["TableHeader"]),
         Paragraph("<b>Action</b>", styles["TableHeader"]),
         Paragraph("<b>Justification</b>", styles["TableHeader"])],
        [Paragraph("Price", styles["TableCell"]),
         Paragraph("Strip £ / non-numeric → float", styles["TableCell"]),
         Paragraph("Currency symbols prevent numeric analysis", styles["TableCell"])],
        [Paragraph("Rating", styles["TableCell"]),
         Paragraph("Map “One”…“Five” → 1–5 integer", styles["TableCell"]),
         Paragraph("Required ordinal scale for modelling", styles["TableCell"])],
        [Paragraph("Stock qty", styles["TableCell"]),
         Paragraph("Prefer detail-page value", styles["TableCell"]),
         Paragraph("Listing page rarely exposes quantity", styles["TableCell"])],
        [Paragraph("Genre", styles["TableCell"]),
         Paragraph("Fill nulls with “Unknown”", styles["TableCell"]),
         Paragraph("Avoid missing categorical values", styles["TableCell"])],
        [Paragraph("Description", styles["TableCell"]),
         Paragraph("Fill empty + create length feature", styles["TableCell"]),
         Paragraph("Length may correlate with perceived value", styles["TableCell"])],
        [Paragraph("Critical nulls", styles["TableCell"]),
         Paragraph("Drop rows missing price or rating", styles["TableCell"]),
         Paragraph("Essential for target and key predictor", styles["TableCell"])],
    ]
    ct = Table(clean_data, colWidths=[28 * mm, 55 * mm, 75 * mm])
    ct.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_GREY]),
        ("BOX", (0, 0), (-1, -1), 0.6, BLUE),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, HexColor("#cccccc")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(ct)
    story.append(Paragraph("Table 2 – Cleaning decisions and justifications", styles["Caption"]))

    story.append(Paragraph(
        "After cleaning, the final dataset contains <b>300 complete records</b> and is saved as "
        "<font face='Courier'>data/books_clean.csv</font>. Mean price is approximately £34.26 "
        "(range £10.16–£59.64); average star rating is 2.92.",
        styles["BodyJust"]
    ))

    # ========== 4. VISUALISATION ==========
    story.append(Paragraph("4. Data Visualisation &amp; Exploration", styles["SectionHead"]))
    story.append(Paragraph(
        "A series of visualisations was produced to explore price patterns, rating distributions, "
        "genre effects and inter-variable relationships. Selected figures are included below; the full set "
        "resides in the accompanying notebook and data folder.",
        styles["BodyJust"]
    ))

    # Embed figures if they exist
    figs = [
        ("fig_price_dist.png", "Figure 1 – Distribution and boxplot of book prices (GBP)"),
        ("fig_rating_price.png", "Figure 2 – Book counts and price distribution by star rating"),
        ("fig_genre_price.png", "Figure 3 – Average price by genre (top 10 by volume)"),
        ("fig_corr.png", "Figure 4 – Correlation matrix of numeric features"),
    ]
    for fname, caption in figs:
        path = os.path.join(DATA_DIR, fname)
        if os.path.exists(path):
            img = Image(path, width=150 * mm, height=55 * mm)
            story.append(img)
            story.append(Paragraph(caption, styles["Caption"]))

    story.append(Paragraph("Key visual findings", styles["SubHead"]))
    findings = [
        "Prices are roughly uniformly distributed across the catalogue – a characteristic of the sandbox website rather than a real market.",
        "Star rating shows only a weak relationship with price; higher-rated books are not systematically more expensive.",
        "Modest average-price differences exist across genres, but the magnitude is small relative to overall price variance.",
        "Correlation analysis confirms that rating, stock quantity and description length are only weakly associated with price.",
    ]
    for f in findings:
        story.append(Paragraph(f"• {f}", styles["BulletText"]))

    # ========== 5. MODELLING ==========
    story.append(Paragraph("5. Predictive Modelling (Linear Regression)", styles["SectionHead"]))
    story.append(Paragraph(
        "A linear regression model was constructed to estimate book price from the following features:",
        styles["BodyJust"]
    ))
    feat_data = [
        [Paragraph("<b>Feature</b>", styles["TableHeader"]),
         Paragraph("<b>Type</b>", styles["TableHeader"]),
         Paragraph("<b>Rationale</b>", styles["TableHeader"])],
        ["rating", "Numeric 1–5", "Higher ratings may command higher prices"],
        ["stock_qty", "Numeric", "Scarcity / abundance can influence pricing"],
        ["desc_length", "Numeric", "Longer descriptions may signal premium content"],
        ["title_length", "Numeric", "Proxy for title complexity"],
        ["genre", "Categorical (OHE)", "Different genres historically have different price points"],
    ]
    feat_t = Table(feat_data, colWidths=[30 * mm, 35 * mm, 95 * mm])
    feat_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_GREY]),
        ("BOX", (0, 0), (-1, -1), 0.6, BLUE),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, HexColor("#cccccc")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(feat_t)
    story.append(Paragraph("Table 3 – Feature selection for the regression model", styles["Caption"]))

    story.append(Paragraph(
        "Numeric features were standardised and genre was one-hot encoded via a scikit-learn "
        "<font face='Courier'>ColumnTransformer</font> pipeline. An 80/20 train-test split "
        "(random_state=42) was used. Model performance is evaluated with MAE, RMSE and R².",
        styles["BodyJust"]
    ))

    story.append(Paragraph(
        "Because prices on the Books-to-Scrape sandbox are artificially generated and only weakly related "
        "to the visible product attributes, a modest R² is both expected and informative: it quantifies "
        "how little of the price signal can be recovered from the scraped features. The residual error "
        "(MAE / RMSE in pounds) provides a practical sense of prediction accuracy.",
        styles["BodyJust"]
    ))

    # Pred vs actual figure
    pred_path = os.path.join(DATA_DIR, "fig_pred_vs_actual.png")
    if os.path.exists(pred_path):
        story.append(Image(pred_path, width=110 * mm, height=90 * mm))
        story.append(Paragraph("Figure 5 – Actual vs Predicted price on the held-out test set", styles["Caption"]))

    coef_path = os.path.join(DATA_DIR, "fig_coefficients.png")
    if os.path.exists(coef_path):
        story.append(Image(coef_path, width=140 * mm, height=55 * mm))
        story.append(Paragraph("Figure 6 – Linear regression coefficients (top 12 by absolute magnitude)", styles["Caption"]))

    story.append(Paragraph("Model limitations", styles["SubHead"]))
    limits = [
        "Synthetic nature of the website data limits real-world generalisability.",
        "Linear model cannot capture non-linear relationships or interactions beyond those implied by the encoding.",
        "Rare genres were filtered to avoid sparse dummy variables, discarding some category information.",
        "Important real-world drivers (author popularity, page count, publication year, competitor pricing) are absent.",
    ]
    for L in limits:
        story.append(Paragraph(f"• {L}", styles["BulletText"]))

    # ========== 6. INSIGHTS & RECOMMENDATIONS ==========
    story.append(Paragraph("6. Key Insights &amp; Recommendations", styles["SectionHead"]))
    story.append(Paragraph("Insights", styles["SubHead"]))
    insights = [
        "Price distribution is relatively flat; the sandbox does not reproduce the skewed price distributions typical of real book markets.",
        "Star rating and stock quantity exhibit only weak linear association with price – ratings remain useful for quality filtering but are poor proxies for expected price on this catalogue.",
        "Genre-level average prices differ modestly; sequential-art and certain non-fiction categories sit slightly above or below the overall mean.",
        "The transparent linear baseline is valuable precisely because it reveals the limited explanatory power of the currently available features.",
    ]
    for i in insights:
        story.append(Paragraph(f"• {i}", styles["BulletText"]))

    story.append(Paragraph("Recommendations for stakeholders", styles["SubHead"]))
    recs = [
        [Paragraph("<b>Stakeholder</b>", styles["TableHeader"]),
         Paragraph("<b>Recommendation</b>", styles["TableHeader"])],
        [Paragraph("Online retailers", styles["TableCell"]),
         Paragraph("Treat rating and genre as secondary pricing signals; prioritise inventory turnover and promotional elasticity analysis.", styles["TableCell"])],
        [Paragraph("Publishers / analytics teams", styles["TableCell"]),
         Paragraph("Enrich future models with author metrics, page count, publication date and competitor prices before production deployment.", styles["TableCell"])],
        [Paragraph("Data-driven book buyers", styles["TableCell"]),
         Paragraph("Continue using star ratings for quality filtering, but do not infer price from rating alone.", styles["TableCell"])],
        [Paragraph("Future modelling work", styles["TableCell"]),
         Paragraph("Expand the scrape to the full 1 000-book catalogue; experiment with regularised and tree-based regressors; engineer rating × genre interactions.", styles["TableCell"])],
    ]
    rt = Table(recs, colWidths=[40 * mm, 120 * mm])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_GREY]),
        ("BOX", (0, 0), (-1, -1), 0.6, BLUE),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, HexColor("#cccccc")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(rt)
    story.append(Paragraph("Table 4 – Stakeholder recommendations", styles["Caption"]))

    # ========== 7. CONCLUSION ==========
    story.append(Paragraph("7. Conclusion", styles["SectionHead"]))
    story.append(Paragraph(
        "This project delivered a complete, reproducible data-science pipeline from raw web data to actionable "
        "insights. Three hundred book records were scraped with BeautifulSoup, cleaned into a structured "
        "analytical dataset, explored through multiple visualisations, and modelled with linear regression. "
        "While the synthetic nature of the Books-to-Scrape catalogue constrains predictive power, the exercise "
        "demonstrates the full workflow expected of a junior data scientist and highlights the importance of "
        "richer feature engineering for real-world pricing applications.",
        styles["BodyJust"]
    ))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph(
        "<b>Deliverables submitted:</b> (1) Jupyter Notebook documenting the entire pipeline, "
        "(2) cleaned dataset <font face='Courier'>books_clean.csv</font>, "
        "(3) this professional project report.",
        styles["BodyJust"]
    ))

    # Build PDF
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Report written to {OUTPUT}")


if __name__ == "__main__":
    create_report()
