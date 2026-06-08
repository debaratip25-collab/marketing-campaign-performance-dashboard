"""
Marketing Campaign Performance Dashboard
Step 1 & 2: Dataset Generation + Data Cleaning
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings('ignore')

random.seed(42)
np.random.seed(42)

# ─── CONFIG ────────────────────────────────────────────────────────────────────
PLATFORMS       = ["Google Ads", "Facebook", "Instagram", "LinkedIn", "Email", "YouTube"]
CAMPAIGN_TYPES  = ["Brand Awareness", "Lead Generation", "Retargeting", "Product Launch", "Seasonal Sale"]
REGIONS         = ["North", "South", "East", "West", "Central"]
AUDIENCE_SEGS   = ["18-24", "25-34", "35-44", "45-54", "55+"]
CAMPAIGN_NAMES  = [
    "Summer Splash Sale", "Back to School Drive", "Festive Season Blitz",
    "New Year Kickoff", "Brand Launch 2024", "Lead Gen Q1", "Retarget Lost Carts",
    "Flash Sale Weekend", "Product Demo Push", "Loyalty Rewards Campaign",
    "Awareness Wave", "Growth Hack Sprint", "LinkedIn B2B Push", "YouTube Pre-Roll",
    "Email Nurture Series", "Holiday Countdown", "App Install Drive",
    "Cross-Sell Upsell", "Win-Back Campaign", "Referral Boost Program",
]

def generate_campaign_data(n=200):
    records = []
    for i in range(1, n + 1):
        platform     = random.choice(PLATFORMS)
        camp_type    = random.choice(CAMPAIGN_TYPES)
        region       = random.choice(REGIONS)
        audience     = random.choice(AUDIENCE_SEGS)
        camp_name    = random.choice(CAMPAIGN_NAMES)

        start = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 300))
        duration = random.randint(7, 45)
        end = start + timedelta(days=duration)

        # Platform-specific realistic ranges
        platform_cfg = {
            "Google Ads":  dict(imp=(50000, 200000), ctr_base=0.06, conv_base=0.04, spend_base=(40000, 150000)),
            "Facebook":    dict(imp=(80000, 300000), ctr_base=0.04, conv_base=0.03, spend_base=(30000, 120000)),
            "Instagram":   dict(imp=(100000, 400000), ctr_base=0.03, conv_base=0.025, spend_base=(25000, 100000)),
            "LinkedIn":    dict(imp=(20000, 80000),  ctr_base=0.025, conv_base=0.05, spend_base=(50000, 200000)),
            "Email":       dict(imp=(10000, 50000),  ctr_base=0.18, conv_base=0.10, spend_base=(5000, 30000)),
            "YouTube":     dict(imp=(200000, 800000), ctr_base=0.015, conv_base=0.02, spend_base=(60000, 250000)),
        }
        cfg = platform_cfg[platform]

        impressions = random.randint(*cfg["imp"])
        ctr         = round(cfg["ctr_base"] * random.uniform(0.7, 1.5), 4)
        clicks      = int(impressions * ctr)
        conv_rate   = round(cfg["conv_base"] * random.uniform(0.6, 1.6), 4)
        conversions = int(clicks * conv_rate)
        leads       = int(conversions * random.uniform(1.2, 2.5))
        spend       = round(random.randint(*cfg["spend_base"]) * random.uniform(0.8, 1.2), 2)
        rev_mult    = random.uniform(1.1, 3.5)
        revenue     = round(spend * rev_mult, 2)

        cpc         = round(spend / clicks, 2) if clicks > 0 else 0
        cpm         = round((spend / impressions) * 1000, 2) if impressions > 0 else 0
        cac         = round(spend / conversions, 2) if conversions > 0 else 0
        roi_pct     = round(((revenue - spend) / spend) * 100, 2) if spend > 0 else 0
        ctr_pct     = round(ctr * 100, 2)
        conv_rate_pct = round(conv_rate * 100, 2)

        records.append({
            "Campaign_ID":        f"C{str(i).zfill(3)}",
            "Campaign_Name":      camp_name,
            "Campaign_Type":      camp_type,
            "Platform":           platform,
            "Campaign_Start_Date": start.strftime("%Y-%m-%d"),
            "Campaign_End_Date":   end.strftime("%Y-%m-%d"),
            "Region":             region,
            "Audience_Segment":   audience,
            "Impressions":        impressions,
            "Clicks":             clicks,
            "CTR_Pct":            ctr_pct,
            "Leads_Generated":    leads,
            "Conversions":        conversions,
            "Conversion_Rate_Pct": conv_rate_pct,
            "Marketing_Spend":    spend,
            "Revenue_Generated":  revenue,
            "ROI_Pct":            roi_pct,
            "CPC":                cpc,
            "CPM":                cpm,
            "CAC":                cac,
        })
    return pd.DataFrame(records)


def introduce_noise(df):
    """Introduce realistic dirty data for cleaning exercise."""
    df = df.copy()
    n = len(df)

    # 5 % missing values in CTR, Leads, CAC
    for col in ["CTR_Pct", "Leads_Generated", "CAC"]:
        idx = df.sample(frac=0.05).index
        df.loc[idx, col] = np.nan

    # Duplicate 4 rows
    dupes = df.sample(4).copy()
    df = pd.concat([df, dupes], ignore_index=True)

    # Typos in Platform
    typo_map = {"Facebook": "facebook", "Instagram": "Instagram ", "Email": "EMAIL"}
    idx = df.sample(frac=0.04).index
    for i in idx:
        orig = df.at[i, "Platform"]
        df.at[i, "Platform"] = typo_map.get(orig, orig.lower())

    # A few zero-spend outliers
    df.loc[df.sample(3).index, "Marketing_Spend"] = 0

    return df


def clean_data(df):
    """Full data cleaning pipeline."""
    print(f"Raw shape          : {df.shape}")

    # 1. Remove duplicates
    df = df.drop_duplicates(subset="Campaign_ID", keep="first")
    print(f"After dedup        : {df.shape}")

    # 2. Standardise Platform
    df["Platform"] = df["Platform"].str.strip().str.title()
    df["Platform"] = df["Platform"].replace({"Email": "Email", "EMAIL": "Email".title()})
    platform_clean = {
        "Facebook": "Facebook", "Google Ads": "Google Ads", "Instagram": "Instagram",
        "Linkedin": "LinkedIn", "Email": "Email", "Youtube": "YouTube",
    }
    df["Platform"] = df["Platform"].replace(platform_clean)

    # 3. Parse dates
    for col in ["Campaign_Start_Date", "Campaign_End_Date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # 4. Fill missing numeric values with column medians
    num_cols = ["CTR_Pct", "Leads_Generated", "CAC"]
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())
        df[col] = df[col].round(2)

    # 5. Remove zero-spend rows (invalid)
    df = df[df["Marketing_Spend"] > 0].reset_index(drop=True)

    # 6. Recalculate derived metrics for consistency
    df["CTR_Pct"]             = (df["Clicks"] / df["Impressions"] * 100).round(2)
    df["Conversion_Rate_Pct"] = (df["Conversions"] / df["Clicks"].replace(0, np.nan) * 100).round(2).fillna(0)
    df["ROI_Pct"]             = ((df["Revenue_Generated"] - df["Marketing_Spend"]) / df["Marketing_Spend"] * 100).round(2)
    df["CPC"]                 = (df["Marketing_Spend"] / df["Clicks"].replace(0, np.nan)).round(2).fillna(0)
    df["CPM"]                 = (df["Marketing_Spend"] / df["Impressions"] * 1000).round(2)
    df["CAC"]                 = (df["Marketing_Spend"] / df["Conversions"].replace(0, np.nan)).round(2).fillna(0)

    # 7. Campaign_Duration column
    df["Campaign_Duration_Days"] = (df["Campaign_End_Date"] - df["Campaign_Start_Date"]).dt.days

    # 8. Profit column
    df["Profit"] = (df["Revenue_Generated"] - df["Marketing_Spend"]).round(2)

    # 9. Month column for time-series
    df["Month"] = df["Campaign_Start_Date"].dt.to_period("M").astype(str)

    print(f"After cleaning     : {df.shape}")
    print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    print(f"\nPlatform counts:\n{df['Platform'].value_counts()}")
    return df


def outlier_report(df):
    print("\n── Outlier Report (IQR method) ──")
    for col in ["ROI_Pct", "CAC", "CPC", "Marketing_Spend"]:
        Q1, Q3 = df[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
        print(f"  {col:25s}: {len(outliers)} outliers")


if __name__ == "__main__":
    print("=" * 60)
    print("  Marketing Campaign Performance — Data Pipeline")
    print("=" * 60)

    raw_df   = generate_campaign_data(200)
    dirty_df = introduce_noise(raw_df)
    dirty_df.to_csv("/home/claude/marketing_dashboard/data/marketing_campaign_raw.csv", index=False)
    print("\n✔ Raw (dirty) dataset saved.")

    clean_df = clean_data(dirty_df)
    outlier_report(clean_df)
    clean_df.to_csv("/home/claude/marketing_dashboard/data/marketing_campaign_clean.csv", index=False)
    print("\n✔ Clean dataset saved.")
    print("\nSample (5 rows):")
    print(clean_df[["Campaign_ID","Platform","ROI_Pct","CTR_Pct","Marketing_Spend","Revenue_Generated"]].head())
