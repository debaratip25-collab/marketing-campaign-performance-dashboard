# 📊 Marketing Campaign Performance Dashboard

## Dashboard

<img width="3848" height="2946" alt="full_dashboard" src="https://github.com/user-attachments/assets/40953d5d-49c0-4a7a-b5c9-87760c74d7a6" />

---

## 📌 Project Objective

Design a **multi-channel Marketing Campaign Performance Dashboard** that tracks and evaluates campaign effectiveness across **Google Ads, Facebook, Instagram, LinkedIn, Email, and YouTube** — measuring ROI, conversion rates, and cost efficiency to enable smarter budget allocation.

> **Industry Context:** Every business that spends money on marketing — from startups to Fortune 500s — needs to know which campaigns work best. This project mirrors how analysts at Google, Zomato, Swiggy, and HubSpot evaluate campaign performance and optimize ad budgets.

---

## 🗂️ Project Structure

```
marketing-campaign-performance-dashboard/
│
├── 📁 python/
    ├── 📄 generate_dataset.py          # Dataset generation + full cleaning pipeline
    ├── 📄 generate_charts.py           # 11 professional matplotlib/seaborn charts
│
├── 📁 data/
│   ├── marketing_campaign_raw.csv     # Original dirty dataset (204 rows, 20 cols)
│   └── marketing_campaign_clean.csv   # Cleaned dataset (197 rows, 23 cols)
│
├── 📁 charts/                      # All 11 individual chart PNGs
│   ├── 01_kpi_cards.png
│   ├── 02_spend_vs_revenue_platform.png
│   ├── 03_roi_by_platform.png
│   ├── 04_ctr_conversion_platform.png
│   ├── 05_conversion_funnel.png
│   ├── 06_cac_cpc_comparison.png
│   ├── 07_audience_segment_analysis.png
│   ├── 08_regional_roi_heatmap.png
│   ├── 09_monthly_trend.png
│   └── 11_campaign_type_roi_boxplot.png
│
├── 📁 dashboard/                 
│   ├── full_dashboard.png
│
├── 📁 excel dashboard/ 
    ├── 📊 Marketing_Campaign_Dashboard.xlsx  # Complete Excel workbook
|
└── 📄 README.md
```

---

## 📦 Dataset Description

**197 campaigns** across 6 platforms, 5 regions, and 5 audience segments — spanning **January to October 2024**.

| Column | Type | Description |
|---|---|---|
| Campaign_ID | Text | Unique identifier (C001–C200) |
| Campaign_Name | Text | Descriptive campaign name |
| Campaign_Type | Text | Brand Awareness / Lead Gen / Retargeting / Product Launch / Seasonal Sale |
| Platform | Text | Google Ads / Facebook / Instagram / LinkedIn / Email / YouTube |
| Campaign_Start/End_Date | Date | Campaign duration dates |
| Region | Text | North / South / East / West / Central |
| Audience_Segment | Text | 18-24 / 25-34 / 35-44 / 45-54 / 55+ |
| Impressions | Integer | Total ad impressions |
| Clicks | Integer | Total ad clicks |
| CTR_Pct | Float | (Clicks / Impressions) × 100 |
| Leads_Generated | Integer | Leads captured |
| Conversions | Integer | Total conversions |
| Conversion_Rate_Pct | Float | (Conversions / Clicks) × 100 |
| Marketing_Spend | Float | Total campaign spend (₹) |
| Revenue_Generated | Float | Revenue attributed (₹) |
| ROI_Pct | Float | ((Revenue − Spend) / Spend) × 100 |
| CPC | Float | Cost Per Click (₹) |
| CPM | Float | Cost Per 1000 Impressions (₹) |
| CAC | Float | Customer Acquisition Cost (₹) |
| Profit | Float | Revenue − Spend (₹) |
| Campaign_Duration_Days | Integer | End − Start date |
| Month | Text | Start month (YYYY-MM) |

---

## ⚙️ Methodology

### Step 1 — Data Generation (`generate_dataset.py`)
- 200 rows generated with **platform-realistic parameters** (e.g., Email CTR ~18%, YouTube CPM-heavy, LinkedIn higher CPC)
- Noise injection: 5% missing values, 4 duplicate rows, platform name typos, 3 zero-spend outliers

### Step 2 — Data Cleaning (`generate_dataset.py`)
| Activity | Action |
|---|---|
| Duplicates | Removed on `Campaign_ID` |
| Platform standardisation | Stripped whitespace, title-cased, mapped aliases |
| Date parsing | `pd.to_datetime()` on Start/End columns |
| Missing values | Filled with column medians |
| Zero-spend rows | Removed (invalid records) |
| Metric recalculation | CTR, Conv Rate, ROI, CPC, CPM, CAC recalculated for consistency |
| Feature engineering | Added `Profit`, `Campaign_Duration_Days`, `Month` |
| Outlier detection | IQR method reported 18 CAC outliers, 28 CPC outliers |

### Step 3 — EDA & Visualisation (`generate_charts.py`)
11 dark-theme professional charts built with matplotlib/seaborn.

### Step 4 — Excel Analysis 
7-sheet excel workbook

---

## 📊 Analysis Performed

- **Platform ROI Comparison** — Which platform delivers the best return per rupee spent?
- **Spend vs Revenue Analysis** — Multi-channel investment efficiency
- **Conversion Funnel Analysis** — Impressions → Clicks → Leads → Conversions drop-off
- **CAC vs CPC Benchmarking** — Cost efficiency across platforms
- **Audience Segment Analysis** — Which age group converts best?
- **Regional Heatmap** — ROI by Region × Platform interaction
- **Monthly Trends** — Revenue, Spend, and ROI trajectory Jan–Oct 2024
- **Campaign Type Distribution** — ROI boxplot by campaign type

---

## 📈 Dashboard Features

| Feature | Details |
|---|---|
| 8 KPI Cards | Spend, Revenue, ROI, CTR, Conversions, Impressions, Leads, CAC |
| Platform Analysis Sheet | Revenue, ROI, CTR, CPC, CAC per platform + embedded bar charts |
| Region Analysis Sheet | Revenue, Profit, ROI per region + pie chart |
| Audience Sheet | ROI, Conversion Rate, CAC per segment + data bars |
| Monthly Trends Sheet | Line chart: Revenue vs Spend over time with formula totals |
| Data Dictionary | Full column documentation |
| Conditional Formatting | Color scale on ROI, data bars on conversion |

---

## 🔑 Key Insights

1. **Email has the highest avg ROI** despite the lowest spend — ideal for scaling with automation
2. **LinkedIn has the highest CPC and CAC** but strong conversion rate — suitable for high-value B2B leads
3. **Google Ads** delivers the best balance of CTR and conversion — strong mid-funnel performer
4. **25–34 age segment** shows the highest revenue share and conversion rate across all platforms
5. **North and Central regions** consistently outperform in ROI across most platforms
6. **YouTube** drives maximum impressions but has the lowest CTR — best for brand awareness, not conversions
7. **Conversion funnel** reveals 92%+ drop-off from Impressions to Clicks — significant optimisation opportunity

---


## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Data generation, cleaning, EDA |
| pandas | Data manipulation & aggregation |
| numpy | Numerical operations |
| matplotlib | Chart creation (11 visualizations) |
| seaborn | Heatmap & boxplot styling |
| Excel | Multi-sheet dashboard & native charts |

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/marketing-campaign-performance-dashboard.git
cd marketing-campaign-performance-dashboard

# 2. Install dependencies
pip install pandas numpy matplotlib seaborn openpyxl

# 3. Generate dataset + clean data
python generate_dataset.py

# 4. Generate all charts
python generate_charts.py

# 5. Build Excel workbook
```

---
