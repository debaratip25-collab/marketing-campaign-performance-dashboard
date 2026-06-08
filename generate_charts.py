"""
Marketing Campaign Performance Dashboard
Step 3: Chart Generation (matplotlib / seaborn)
Produces PNG screenshots for GitHub, LinkedIn, Instagram
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ─── Theme ─────────────────────────────────────────────────────────────────────
PALETTE = {
    "bg":       "#0F1117",
    "panel":    "#1A1D2E",
    "accent1":  "#6C63FF",
    "accent2":  "#FF6584",
    "accent3":  "#43E97B",
    "accent4":  "#FFD93D",
    "accent5":  "#4FC3F7",
    "text":     "#E8E8F0",
    "subtext":  "#9494B8",
    "grid":     "#2A2D42",
}
PLATFORM_COLORS = {
    "Google Ads":  "#4285F4",
    "Facebook":    "#1877F2",
    "Instagram":   "#E1306C",
    "LinkedIn":    "#0A66C2",
    "Email":       "#43E97B",
    "YouTube":     "#FF0000",
}
FONT_TITLE  = {"fontsize": 15, "fontweight": "bold", "color": PALETTE["text"]}
FONT_LABEL  = {"fontsize": 10, "color": PALETTE["subtext"]}
FONT_TICK   = {"labelsize": 9,  "colors": PALETTE["subtext"]}

def apply_dark_theme():
    plt.rcParams.update({
        "figure.facecolor":  PALETTE["bg"],
        "axes.facecolor":    PALETTE["panel"],
        "axes.edgecolor":    PALETTE["grid"],
        "axes.labelcolor":   PALETTE["subtext"],
        "xtick.color":       PALETTE["subtext"],
        "ytick.color":       PALETTE["subtext"],
        "grid.color":        PALETTE["grid"],
        "grid.alpha":        0.5,
        "text.color":        PALETTE["text"],
        "font.family":       "DejaVu Sans",
        "axes.spines.top":   False,
        "axes.spines.right": False,
    })

def currency(x, _): return f"₹{x/1e6:.1f}M" if abs(x) >= 1e6 else f"₹{x/1e3:.0f}K"
def pct(x, _): return f"{x:.1f}%"

OUT = "/home/claude/marketing_dashboard/charts"


# ─── 1. KPI Summary Card ───────────────────────────────────────────────────────
def chart_kpi_cards(df):
    apply_dark_theme()
    fig, axes = plt.subplots(1, 5, figsize=(18, 3.5))
    fig.patch.set_facecolor(PALETTE["bg"])
    fig.suptitle("Marketing Campaign Performance — KPI Overview", fontsize=14,
                 fontweight="bold", color=PALETTE["text"], y=1.02)

    kpis = [
        ("Total Spend",        f"₹{df['Marketing_Spend'].sum()/1e6:.2f}M",     PALETTE["accent1"], "💰"),
        ("Total Revenue",      f"₹{df['Revenue_Generated'].sum()/1e6:.2f}M",   PALETTE["accent3"], "📈"),
        ("Avg ROI",            f"{df['ROI_Pct'].mean():.1f}%",                  PALETTE["accent4"], "🏆"),
        ("Avg CTR",            f"{df['CTR_Pct'].mean():.2f}%",                  PALETTE["accent5"], "🎯"),
        ("Total Conversions",  f"{int(df['Conversions'].sum()):,}",              PALETTE["accent2"], "✅"),
    ]

    for ax, (label, value, color, icon) in zip(axes, kpis):
        ax.set_facecolor(PALETTE["panel"])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.axis("off")
        # Card border line
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor(color)
            spine.set_linewidth(2)
        ax.text(0.5, 0.78, icon,  ha="center", va="center", fontsize=22, transform=ax.transAxes)
        ax.text(0.5, 0.50, value, ha="center", va="center", fontsize=22,
                fontweight="bold", color=color, transform=ax.transAxes)
        ax.text(0.5, 0.20, label, ha="center", va="center", fontsize=11,
                color=PALETTE["subtext"], transform=ax.transAxes)

    plt.tight_layout(pad=2)
    plt.savefig(f"{OUT}/01_kpi_cards.png", dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close()
    print("  ✔ 01_kpi_cards.png")


# ─── 2. Revenue vs Spend by Platform ──────────────────────────────────────────
def chart_spend_vs_revenue(df):
    apply_dark_theme()
    agg = df.groupby("Platform")[["Marketing_Spend", "Revenue_Generated", "Profit"]].sum().reset_index()
    agg = agg.sort_values("Revenue_Generated", ascending=False)

    fig, ax = plt.subplots(figsize=(13, 6))
    x = np.arange(len(agg))
    w = 0.35

    bars1 = ax.bar(x - w/2, agg["Marketing_Spend"],   w, label="Marketing Spend",   color=PALETTE["accent1"], alpha=0.85)
    bars2 = ax.bar(x + w/2, agg["Revenue_Generated"], w, label="Revenue Generated", color=PALETTE["accent3"], alpha=0.85)

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1e5,
                f"₹{bar.get_height()/1e6:.1f}M", ha="center", fontsize=8, color=PALETTE["subtext"])
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1e5,
                f"₹{bar.get_height()/1e6:.1f}M", ha="center", fontsize=8, color=PALETTE["accent3"])

    ax.set_xticks(x)
    ax.set_xticklabels(agg["Platform"], fontsize=10)
    ax.yaxis.set_major_formatter(FuncFormatter(currency))
    ax.set_title("Marketing Spend vs Revenue Generated by Platform", **FONT_TITLE)
    ax.set_ylabel("Amount (₹)", **FONT_LABEL)
    ax.legend(facecolor=PALETTE["panel"], edgecolor=PALETTE["grid"], labelcolor=PALETTE["text"])
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{OUT}/02_spend_vs_revenue_platform.png", dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close()
    print("  ✔ 02_spend_vs_revenue_platform.png")


# ─── 3. ROI by Platform (Horizontal Bar) ──────────────────────────────────────
def chart_roi_by_platform(df):
    apply_dark_theme()
    roi = df.groupby("Platform")["ROI_Pct"].mean().sort_values()
    colors = [PLATFORM_COLORS.get(p, PALETTE["accent1"]) for p in roi.index]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(roi.index, roi.values, color=colors, alpha=0.88, height=0.55)

    for bar, val in zip(bars, roi.values):
        ax.text(val + 1, bar.get_y() + bar.get_height()/2,
                f"{val:.1f}%", va="center", fontsize=10, fontweight="bold",
                color=PALETTE["text"])

    ax.axvline(roi.mean(), color=PALETTE["accent4"], linestyle="--", linewidth=1.5, label=f"Mean ROI: {roi.mean():.1f}%")
    ax.set_xlabel("Average ROI (%)", **FONT_LABEL)
    ax.set_title("Average ROI by Platform", **FONT_TITLE)
    ax.legend(facecolor=PALETTE["panel"], edgecolor=PALETTE["grid"], labelcolor=PALETTE["text"])
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{OUT}/03_roi_by_platform.png", dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close()
    print("  ✔ 03_roi_by_platform.png")


# ─── 4. CTR & Conversion Rate by Platform (dual bars) ─────────────────────────
def chart_ctr_conv_platform(df):
    apply_dark_theme()
    agg = df.groupby("Platform")[["CTR_Pct","Conversion_Rate_Pct"]].mean().reset_index()
    agg = agg.sort_values("CTR_Pct", ascending=False)

    x = np.arange(len(agg)); w = 0.38
    fig, ax = plt.subplots(figsize=(12, 5.5))

    ax.bar(x - w/2, agg["CTR_Pct"],             w, label="CTR %",             color=PALETTE["accent5"], alpha=0.85)
    ax.bar(x + w/2, agg["Conversion_Rate_Pct"], w, label="Conversion Rate %", color=PALETTE["accent2"], alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(agg["Platform"], fontsize=10)
    ax.yaxis.set_major_formatter(FuncFormatter(pct))
    ax.set_title("CTR % vs Conversion Rate % by Platform", **FONT_TITLE)
    ax.set_ylabel("Rate (%)", **FONT_LABEL)
    ax.legend(facecolor=PALETTE["panel"], edgecolor=PALETTE["grid"], labelcolor=PALETTE["text"])
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{OUT}/04_ctr_conversion_platform.png", dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close()
    print("  ✔ 04_ctr_conversion_platform.png")


# ─── 5. Conversion Funnel ─────────────────────────────────────────────────────
def chart_conversion_funnel(df):
    apply_dark_theme()
    stages  = ["Impressions", "Clicks", "Leads_Generated", "Conversions"]
    totals  = [df[s].sum() for s in stages]
    labels  = ["Impressions", "Clicks", "Leads", "Conversions"]
    colors  = [PALETTE["accent1"], PALETTE["accent5"], PALETTE["accent4"], PALETTE["accent3"]]

    fig, ax = plt.subplots(figsize=(10, 6))
    y_pos = np.arange(len(stages))
    bars = ax.barh(y_pos, totals, color=colors, height=0.55, alpha=0.9)

    for bar, val, lab in zip(bars, totals, labels):
        ax.text(bar.get_width() * 0.5, bar.get_y() + bar.get_height()/2,
                f"{val:,.0f}", ha="center", va="center", fontsize=11,
                fontweight="bold", color=PALETTE["bg"])

    # Drop-off annotations
    for i in range(1, len(totals)):
        pct_val = totals[i] / totals[i-1] * 100
        ax.text(totals[i] + totals[0]*0.01, y_pos[i],
                f"↑{pct_val:.1f}% from prev", va="center", fontsize=9, color=PALETTE["subtext"])

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=12)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x,_: f"{x/1e6:.1f}M" if x>=1e6 else f"{x/1e3:.0f}K"))
    ax.set_title("Campaign Conversion Funnel — All Channels Combined", **FONT_TITLE)
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{OUT}/05_conversion_funnel.png", dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close()
    print("  ✔ 05_conversion_funnel.png")


# ─── 6. CAC & CPC Comparison ──────────────────────────────────────────────────
def chart_cac_cpc(df):
    apply_dark_theme()
    agg = df.groupby("Platform")[["CAC","CPC"]].mean().reset_index().sort_values("CAC")

    x = np.arange(len(agg)); w = 0.38
    fig, ax1 = plt.subplots(figsize=(12, 5.5))
    ax2 = ax1.twinx()

    bars1 = ax1.bar(x - w/2, agg["CAC"], w, label="CAC (₹)", color=PALETTE["accent2"], alpha=0.85)
    bars2 = ax2.bar(x + w/2, agg["CPC"], w, label="CPC (₹)", color=PALETTE["accent4"], alpha=0.85)

    ax1.set_xticks(x); ax1.set_xticklabels(agg["Platform"], fontsize=10)
    ax1.set_ylabel("Customer Acquisition Cost — CAC (₹)", color=PALETTE["accent2"], fontsize=10)
    ax2.set_ylabel("Cost Per Click — CPC (₹)",            color=PALETTE["accent4"], fontsize=10)
    ax1.set_title("CAC vs CPC by Platform", **FONT_TITLE)

    lines1 = mpatches.Patch(color=PALETTE["accent2"], label="Avg CAC")
    lines2 = mpatches.Patch(color=PALETTE["accent4"], label="Avg CPC")
    ax1.legend(handles=[lines1, lines2], facecolor=PALETTE["panel"],
               edgecolor=PALETTE["grid"], labelcolor=PALETTE["text"])
    ax1.grid(axis="y", alpha=0.2)

    plt.tight_layout()
    plt.savefig(f"{OUT}/06_cac_cpc_comparison.png", dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close()
    print("  ✔ 06_cac_cpc_comparison.png")


# ─── 7. Revenue by Audience Segment ───────────────────────────────────────────
def chart_audience_revenue(df):
    apply_dark_theme()
    agg = df.groupby("Audience_Segment")[["Revenue_Generated","Conversions","Marketing_Spend"]].sum().reset_index()
    agg["ROI_Pct"] = (agg["Revenue_Generated"] - agg["Marketing_Spend"]) / agg["Marketing_Spend"] * 100
    agg = agg.sort_values("Revenue_Generated", ascending=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    colors = [PALETTE["accent1"], PALETTE["accent3"], PALETTE["accent4"], PALETTE["accent5"], PALETTE["accent2"]]
    wedges, texts, autotexts = ax1.pie(
        agg["Revenue_Generated"], labels=agg["Audience_Segment"],
        autopct="%1.1f%%", colors=colors,
        wedgeprops=dict(edgecolor=PALETTE["bg"], linewidth=2),
        textprops=dict(color=PALETTE["text"], fontsize=10),
        startangle=90,
    )
    for at in autotexts: at.set_color(PALETTE["bg"]); at.set_fontweight("bold")
    ax1.set_title("Revenue Share by Audience Segment", **FONT_TITLE)
    ax1.set_facecolor(PALETTE["panel"])

    bars = ax2.bar(agg["Audience_Segment"], agg["ROI_Pct"], color=colors, alpha=0.88)
    for b, v in zip(bars, agg["ROI_Pct"]):
        ax2.text(b.get_x()+b.get_width()/2, b.get_height()+1, f"{v:.1f}%",
                 ha="center", fontsize=9, color=PALETTE["text"])
    ax2.set_title("ROI % by Audience Segment", **FONT_TITLE)
    ax2.set_ylabel("ROI (%)", **FONT_LABEL)
    ax2.yaxis.set_major_formatter(FuncFormatter(pct))
    ax2.grid(axis="y", alpha=0.3)

    fig.suptitle("Audience Segment Performance Analysis", fontsize=16, fontweight="bold",
                 color=PALETTE["text"], y=1.01)
    plt.tight_layout()
    plt.savefig(f"{OUT}/07_audience_segment_analysis.png", dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close()
    print("  ✔ 07_audience_segment_analysis.png")


# ─── 8. Regional Performance Heat-map ─────────────────────────────────────────
def chart_regional_heatmap(df):
    apply_dark_theme()
    pivot = df.pivot_table(values="ROI_Pct", index="Region", columns="Platform", aggfunc="mean")

    fig, ax = plt.subplots(figsize=(13, 5))
    sns.heatmap(
        pivot, ax=ax, annot=True, fmt=".0f", cmap="RdYlGn",
        linewidths=0.5, linecolor=PALETTE["bg"],
        annot_kws={"size": 10, "weight": "bold"},
        cbar_kws={"label": "Avg ROI %"},
    )
    ax.set_title("Regional ROI % Heatmap by Platform", **FONT_TITLE)
    ax.set_xlabel("Platform", **FONT_LABEL)
    ax.set_ylabel("Region",   **FONT_LABEL)
    ax.tick_params(**FONT_TICK)

    plt.tight_layout()
    plt.savefig(f"{OUT}/08_regional_roi_heatmap.png", dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close()
    print("  ✔ 08_regional_roi_heatmap.png")


# ─── 9. Monthly Trend ─────────────────────────────────────────────────────────
def chart_monthly_trend(df):
    apply_dark_theme()
    monthly = df.groupby("Month").agg(
        Revenue=("Revenue_Generated","sum"),
        Spend=("Marketing_Spend","sum"),
        ROI=("ROI_Pct","mean"),
        Conversions=("Conversions","sum"),
    ).reset_index().sort_values("Month")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9), sharex=True)

    ax1.fill_between(monthly["Month"], monthly["Revenue"], alpha=0.25, color=PALETTE["accent3"])
    ax1.fill_between(monthly["Month"], monthly["Spend"],   alpha=0.25, color=PALETTE["accent1"])
    ax1.plot(monthly["Month"], monthly["Revenue"], marker="o", markersize=5, color=PALETTE["accent3"], label="Revenue", linewidth=2)
    ax1.plot(monthly["Month"], monthly["Spend"],   marker="o", markersize=5, color=PALETTE["accent1"], label="Spend",   linewidth=2)
    ax1.yaxis.set_major_formatter(FuncFormatter(currency))
    ax1.set_title("Monthly Revenue vs Marketing Spend", **FONT_TITLE)
    ax1.legend(facecolor=PALETTE["panel"], edgecolor=PALETTE["grid"], labelcolor=PALETTE["text"])
    ax1.grid(axis="y", alpha=0.3)

    ax2.plot(monthly["Month"], monthly["ROI"], marker="s", markersize=5, color=PALETTE["accent4"], label="Avg ROI %", linewidth=2)
    ax2.fill_between(monthly["Month"], monthly["ROI"], alpha=0.2, color=PALETTE["accent4"])
    ax2.yaxis.set_major_formatter(FuncFormatter(pct))
    ax2.set_title("Monthly Average ROI Trend", **FONT_TITLE)
    ax2.set_xlabel("Month", **FONT_LABEL)
    ax2.legend(facecolor=PALETTE["panel"], edgecolor=PALETTE["grid"], labelcolor=PALETTE["text"])
    ax2.grid(axis="y", alpha=0.3)
    ax2.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig(f"{OUT}/09_monthly_trend.png", dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close()
    print("  ✔ 09_monthly_trend.png")


# ─── 10. Full Dashboard Screenshot ────────────────────────────────────────────
def chart_full_dashboard(df):
    apply_dark_theme()
    fig = plt.figure(figsize=(22, 16))
    fig.patch.set_facecolor(PALETTE["bg"])

    # Title Banner
    fig.text(0.5, 0.97, "📊 Marketing Campaign Performance Dashboard",
             ha="center", va="top", fontsize=20, fontweight="bold", color=PALETTE["text"])
    fig.text(0.5, 0.945, "Multi-Channel ROI, Conversion & Spend Intelligence  |  Dataset: 197 Campaigns  |  Periods: Jan–Oct 2024",
             ha="center", va="top", fontsize=11, color=PALETTE["subtext"])

    gs = gridspec.GridSpec(4, 4, figure=fig,
                           hspace=0.55, wspace=0.4,
                           top=0.92, bottom=0.05, left=0.06, right=0.97)

    # ── Row 0: KPI Cards ──
    kpis = [
        ("💰 Total Spend",       f"₹{df['Marketing_Spend'].sum()/1e6:.2f}M",    PALETTE["accent1"]),
        ("📈 Total Revenue",     f"₹{df['Revenue_Generated'].sum()/1e6:.2f}M",  PALETTE["accent3"]),
        ("🏆 Avg ROI",           f"{df['ROI_Pct'].mean():.1f}%",                 PALETTE["accent4"]),
        ("🎯 Avg CTR",           f"{df['CTR_Pct'].mean():.2f}%",                 PALETTE["accent5"]),
        ("✅ Conversions",       f"{int(df['Conversions'].sum()):,}",             PALETTE["accent2"]),
        ("📣 Total Impressions", f"{df['Impressions'].sum()/1e6:.1f}M",          "#FF9F43"),
        ("🧩 Leads Generated",  f"{int(df['Leads_Generated'].sum()):,}",         "#A29BFE"),
        ("💵 Avg CAC",          f"₹{df['CAC'].mean():,.0f}",                    "#FD79A8"),
    ]

    for idx, (label, value, color) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, idx % 4])
        ax.set_facecolor("#1E2235")
        ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
        for spine in ax.spines.values():
            spine.set_visible(True); spine.set_edgecolor(color); spine.set_linewidth(2.5)
        ax.text(0.5, 0.62, value, ha="center", va="center", fontsize=17, fontweight="bold", color=color, transform=ax.transAxes)
        ax.text(0.5, 0.22, label, ha="center", va="center", fontsize=9, color=PALETTE["subtext"], transform=ax.transAxes)

    # Need two rows for 8 KPIs — add row 1 cards too
    for idx in range(4, 8):
        ax = fig.add_subplot(gs[1, idx % 4])
        label, value, color = kpis[idx]
        ax.set_facecolor("#1E2235")
        ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
        for spine in ax.spines.values():
            spine.set_visible(True); spine.set_edgecolor(color); spine.set_linewidth(2.5)
        ax.text(0.5, 0.62, value, ha="center", va="center", fontsize=17, fontweight="bold", color=color, transform=ax.transAxes)
        ax.text(0.5, 0.22, label, ha="center", va="center", fontsize=9, color=PALETTE["subtext"], transform=ax.transAxes)

    # ── Row 2: Spend vs Revenue (wide) + ROI by Platform ──
    ax_svr = fig.add_subplot(gs[2, :2])
    agg = df.groupby("Platform")[["Marketing_Spend","Revenue_Generated"]].sum().reset_index().sort_values("Revenue_Generated", ascending=False)
    x = np.arange(len(agg)); w = 0.35
    ax_svr.bar(x - w/2, agg["Marketing_Spend"],   w, color=PALETTE["accent1"], alpha=0.85, label="Spend")
    ax_svr.bar(x + w/2, agg["Revenue_Generated"], w, color=PALETTE["accent3"], alpha=0.85, label="Revenue")
    ax_svr.set_xticks(x); ax_svr.set_xticklabels(agg["Platform"], fontsize=8)
    ax_svr.yaxis.set_major_formatter(FuncFormatter(currency))
    ax_svr.set_title("Spend vs Revenue by Platform", fontsize=11, fontweight="bold", color=PALETTE["text"])
    ax_svr.legend(facecolor=PALETTE["panel"], edgecolor=PALETTE["grid"], labelcolor=PALETTE["text"], fontsize=8)
    ax_svr.grid(axis="y", alpha=0.3)

    ax_roi = fig.add_subplot(gs[2, 2:4])
    roi = df.groupby("Platform")["ROI_Pct"].mean().sort_values()
    colors_p = [PLATFORM_COLORS.get(p, PALETTE["accent1"]) for p in roi.index]
    ax_roi.barh(roi.index, roi.values, color=colors_p, alpha=0.88)
    ax_roi.axvline(roi.mean(), color=PALETTE["accent4"], linestyle="--", linewidth=1.2, label=f"Mean {roi.mean():.0f}%")
    ax_roi.set_title("Avg ROI % by Platform", fontsize=11, fontweight="bold", color=PALETTE["text"])
    ax_roi.legend(facecolor=PALETTE["panel"], edgecolor=PALETTE["grid"], labelcolor=PALETTE["text"], fontsize=8)
    ax_roi.grid(axis="x", alpha=0.3)

    # ── Row 3: Funnel + Heatmap ──
    ax_funnel = fig.add_subplot(gs[3, :2])
    stages = ["Impressions", "Clicks", "Leads_Generated", "Conversions"]
    totals = [df[s].sum() for s in stages]
    labs   = ["Impressions", "Clicks", "Leads", "Conversions"]
    clrs   = [PALETTE["accent1"], PALETTE["accent5"], PALETTE["accent4"], PALETTE["accent3"]]
    bars_f = ax_funnel.barh(labs, totals, color=clrs, height=0.5, alpha=0.9)
    for bar, val in zip(bars_f, totals):
        ax_funnel.text(bar.get_width()*0.5, bar.get_y()+bar.get_height()/2,
                       f"{val:,.0f}", ha="center", va="center", fontsize=9,
                       fontweight="bold", color=PALETTE["bg"])
    ax_funnel.xaxis.set_major_formatter(FuncFormatter(lambda x,_: f"{x/1e6:.1f}M" if x>=1e6 else f"{x/1e3:.0f}K"))
    ax_funnel.set_title("Conversion Funnel", fontsize=11, fontweight="bold", color=PALETTE["text"])
    ax_funnel.grid(axis="x", alpha=0.3)

    ax_heat = fig.add_subplot(gs[3, 2:4])
    pivot = df.pivot_table(values="ROI_Pct", index="Region", columns="Platform", aggfunc="mean")
    sns.heatmap(pivot, ax=ax_heat, annot=True, fmt=".0f", cmap="RdYlGn",
                linewidths=0.4, linecolor=PALETTE["bg"],
                annot_kws={"size": 7, "weight": "bold"},
                cbar_kws={"label": "ROI%", "shrink": 0.8})
    ax_heat.set_title("Regional ROI Heatmap", fontsize=11, fontweight="bold", color=PALETTE["text"])
    ax_heat.tick_params(axis="x", rotation=30, labelsize=8)
    ax_heat.tick_params(axis="y", rotation=0,  labelsize=8)

    plt.savefig(f"{OUT}/10_full_dashboard.png", dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close()
    print("  ✔ 10_full_dashboard.png")


# ─── 11. Campaign Type ROI Boxplot ─────────────────────────────────────────────
def chart_campaign_type_boxplot(df):
    apply_dark_theme()
    order = df.groupby("Campaign_Type")["ROI_Pct"].median().sort_values(ascending=False).index
    palette = {t: c for t, c in zip(order, [PALETTE["accent1"],PALETTE["accent3"],PALETTE["accent4"],PALETTE["accent5"],PALETTE["accent2"]])}

    fig, ax = plt.subplots(figsize=(13, 5.5))
    sns.boxplot(data=df, x="Campaign_Type", y="ROI_Pct", order=order,
                palette=palette, ax=ax,
                medianprops=dict(color=PALETTE["text"], linewidth=2),
                whiskerprops=dict(color=PALETTE["subtext"]),
                capprops=dict(color=PALETTE["subtext"]),
                flierprops=dict(marker="o", markerfacecolor=PALETTE["accent2"], markersize=4, alpha=0.6))
    ax.axhline(df["ROI_Pct"].mean(), color=PALETTE["accent4"], linestyle="--",
               linewidth=1.5, label=f"Overall Mean ROI: {df['ROI_Pct'].mean():.1f}%")
    ax.set_title("ROI Distribution by Campaign Type", **FONT_TITLE)
    ax.set_xlabel("Campaign Type", **FONT_LABEL)
    ax.set_ylabel("ROI %", **FONT_LABEL)
    ax.legend(facecolor=PALETTE["panel"], edgecolor=PALETTE["grid"], labelcolor=PALETTE["text"])
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{OUT}/11_campaign_type_roi_boxplot.png", dpi=150, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close()
    print("  ✔ 11_campaign_type_roi_boxplot.png")


# ─── Copy key charts to screenshots folder ────────────────────────────────────
def copy_screenshots():
    import shutil
    src = "/home/claude/marketing_dashboard/charts"
    dst = "/home/claude/marketing_dashboard/screenshots"
    key_charts = [
        "10_full_dashboard.png",
        "02_spend_vs_revenue_platform.png",
        "03_roi_by_platform.png",
        "05_conversion_funnel.png",
        "08_regional_roi_heatmap.png",
    ]
    for fn in key_charts:
        shutil.copy(f"{src}/{fn}", f"{dst}/{fn}")
    print(f"\n  ✔ {len(key_charts)} key charts copied to /screenshots/")


if __name__ == "__main__":
    print("=" * 60)
    print("  Marketing Campaign Dashboard — Chart Generation")
    print("=" * 60)

    df = pd.read_csv("/home/claude/marketing_dashboard/data/marketing_campaign_clean.csv")

    print("\nGenerating charts…")
    chart_kpi_cards(df)
    chart_spend_vs_revenue(df)
    chart_roi_by_platform(df)
    chart_ctr_conv_platform(df)
    chart_conversion_funnel(df)
    chart_cac_cpc(df)
    chart_audience_revenue(df)
    chart_regional_heatmap(df)
    chart_monthly_trend(df)
    chart_full_dashboard(df)
    chart_campaign_type_boxplot(df)
    copy_screenshots()
    print("\n✔ All charts generated successfully.")
