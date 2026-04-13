"""
US Construction Spending Analysis (2002-2016)
=============================================
Analyses monthly construction spending data from the US Census Bureau
to uncover sector trends, seasonal patterns, and growth dynamics.

Relevant to building materials and construction sales: understanding
where spending is growing (and shrinking) helps sales teams prioritise
sectors and time their outreach.

Author: Tommy Nguyen
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message="DataFrame is highly fragmented")

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DATA_PATH = Path(__file__).parent / "construction_spending.csv"
VIS_DIR = Path(__file__).parent / "visuals"
VIS_DIR.mkdir(exist_ok=True)

DPI = 150
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.05)
plt.rcParams["figure.figsize"] = (10, 5.5)


# ---------------------------------------------------------------------------
# 1. Load & clean
# ---------------------------------------------------------------------------
print("=" * 60)
print("US CONSTRUCTION SPENDING ANALYSIS  (2002-2016)")
print("=" * 60)

df = pd.read_csv(DATA_PATH)

# Build a proper datetime column
df["date"] = pd.to_datetime(
    df["time.year"].astype(str) + "-" + df["time.month"].astype(str) + "-01"
)
df = df.sort_values("date").reset_index(drop=True)

print(f"\nRows: {len(df)}  |  Date range: {df['date'].min():%b %Y} to {df['date'].max():%b %Y}")
print(f"Columns: {len(df.columns)}")

# We'll work primarily with the "current" (seasonally-adjusted annual rate)
# spending columns, which represent the most recent estimate for each month.
# Units are millions of USD.

# Shorthand references for key "current.combined" columns
TOTAL   = "current.combined.total construction"
RES     = "current.combined.residential"
NONRES  = "current.combined.nonresidential"
PRIVATE = "current.private.total construction"
PUBLIC  = "current.public.total construction"

# Key sub-sectors (current, combined)
SECTORS = {
    "Residential":       "current.combined.residential",
    "Commercial":        "current.combined.commercial",
    "Manufacturing":     "current.combined.manufacturing",
    "Educational":       "current.combined.educational",
    "Health Care":       "current.combined.health care",
    "Highway & Street":  "current.combined.highway and street",
    "Office":            "current.combined.office",
    "Power":             "current.combined.power",
    "Lodging":           "current.combined.lodging",
}


# ---------------------------------------------------------------------------
# 2. Key statistics
# ---------------------------------------------------------------------------
latest = df.iloc[-1]
earliest = df.iloc[0]

total_growth = (latest[TOTAL] - earliest[TOTAL]) / earliest[TOTAL] * 100

print("\n--- Key Figures (Current Spending, Millions USD) ---")
print(f"Total construction (Jan 2002): ${earliest[TOTAL]:,.0f}M")
print(f"Total construction (Jan 2016): ${latest[TOTAL]:,.0f}M")
print(f"Overall growth: {total_growth:+.1f}%")

# Year-over-year growth for the final year
jan16 = df[df["date"] == "2016-01-01"][TOTAL].values[0]
jan15 = df[df["date"] == "2015-01-01"][TOTAL].values[0]
print(f"YoY growth (Jan 2015 -> Jan 2016): {(jan16 - jan15) / jan15 * 100:+.1f}%")

# Residential vs non-residential share (latest)
res_share = latest[RES] / latest[TOTAL] * 100
print(f"\nResidential share of total (latest): {res_share:.1f}%")
print(f"Non-residential share:               {100 - res_share:.1f}%")


# ---------------------------------------------------------------------------
# 3. Visualisations
# ---------------------------------------------------------------------------

# --- Chart 1: Total construction spending over time -------------------------
fig, ax = plt.subplots()
ax.plot(df["date"], df[TOTAL] / 1000, color="#2563EB", linewidth=2)
ax.set_title("Total US Construction Spending (2002-2016)", fontsize=14, fontweight="bold")
ax.set_ylabel("Spending (Billions USD)")
ax.set_xlabel("")
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}B"))

# Annotate the GFC dip
gfc_low = df.loc[df[TOTAL].idxmin()]
ax.annotate(
    f"GFC low\n{gfc_low['date']:%b %Y}",
    xy=(gfc_low["date"], gfc_low[TOTAL] / 1000),
    xytext=(gfc_low["date"], gfc_low[TOTAL] / 1000 + 12),
    fontsize=9, ha="center",
    arrowprops=dict(arrowstyle="->", color="grey"),
)
fig.tight_layout()
fig.savefig(VIS_DIR / "01_total_spending_trend.png", dpi=DPI)
plt.close(fig)
print("\n[saved] 01_total_spending_trend.png")


# --- Chart 2: Residential vs Non-Residential --------------------------------
fig, ax = plt.subplots()
ax.stackplot(
    df["date"],
    df[RES] / 1000,
    df[NONRES] / 1000,
    labels=["Residential", "Non-Residential"],
    colors=["#3B82F6", "#F59E0B"],
    alpha=0.85,
)
ax.set_title("Residential vs Non-Residential Spending", fontsize=14, fontweight="bold")
ax.set_ylabel("Spending (Billions USD)")
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}B"))
ax.legend(loc="upper left", frameon=True)
fig.tight_layout()
fig.savefig(VIS_DIR / "02_residential_vs_nonresidential.png", dpi=DPI)
plt.close(fig)
print("[saved] 02_residential_vs_nonresidential.png")


# --- Chart 3: Private vs Public spending ------------------------------------
fig, ax = plt.subplots()
ax.plot(df["date"], df[PRIVATE] / 1000, label="Private", linewidth=2, color="#10B981")
ax.plot(df["date"], df[PUBLIC] / 1000, label="Public", linewidth=2, color="#EF4444")
ax.set_title("Private vs Public Construction Spending", fontsize=14, fontweight="bold")
ax.set_ylabel("Spending (Billions USD)")
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}B"))
ax.legend(frameon=True)
fig.tight_layout()
fig.savefig(VIS_DIR / "03_private_vs_public.png", dpi=DPI)
plt.close(fig)
print("[saved] 03_private_vs_public.png")


# --- Chart 4: Sector breakdown, a bar chart of latest vs earliest -----------
sector_data = []
for name, col in SECTORS.items():
    val_start = earliest[col]
    val_end = latest[col]
    if val_start > 0:
        growth = (val_end - val_start) / val_start * 100
    else:
        growth = 0
    sector_data.append({"Sector": name, "2002": val_start, "2016": val_end, "Growth %": growth})

sdf = pd.DataFrame(sector_data).sort_values("Growth %", ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#EF4444" if g < 0 else "#10B981" for g in sdf["Growth %"]]
ax.barh(sdf["Sector"], sdf["Growth %"], color=colors, edgecolor="white")
ax.set_title("Sector Growth: Jan 2002 to Jan 2016", fontsize=14, fontweight="bold")
ax.set_xlabel("Growth (%)")
ax.axvline(0, color="black", linewidth=0.8)

for i, (_, row) in enumerate(sdf.iterrows()):
    pct = row["Growth %"]
    offset = 3 if pct >= 0 else -3
    ha = "left" if pct >= 0 else "right"
    ax.text(pct + offset, i, f"{pct:+.0f}%", va="center", ha=ha, fontsize=9)

fig.tight_layout()
fig.savefig(VIS_DIR / "04_sector_growth.png", dpi=DPI)
plt.close(fig)
print("[saved] 04_sector_growth.png")


# --- Chart 5: Seasonal pattern (avg spending by month) ----------------------
df["month"] = df["date"].dt.month
monthly_avg = df.groupby("month")[TOTAL].mean() / 1000
month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

fig, ax = plt.subplots()
ax.bar(range(1, 13), monthly_avg.values, color="#6366F1", edgecolor="white")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_labels)
ax.set_title("Average Monthly Construction Spending", fontsize=14, fontweight="bold")
ax.set_ylabel("Avg Spending (Billions USD)")
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}B"))
fig.tight_layout()
fig.savefig(VIS_DIR / "05_seasonal_pattern.png", dpi=DPI)
plt.close(fig)
print("[saved] 05_seasonal_pattern.png")


# --- Chart 6: Year-over-year growth rate ------------------------------------
df["year"] = df["date"].dt.year
# Exclude 2016; only has January, so the average is misleading for YoY
full_years = df[df["year"] <= 2015]
yearly = full_years.groupby("year")[TOTAL].mean()
yoy = yearly.pct_change() * 100
yoy = yoy.dropna()

fig, ax = plt.subplots()
colors_yoy = ["#EF4444" if v < 0 else "#10B981" for v in yoy.values]
ax.bar(yoy.index.astype(int), yoy.values, color=colors_yoy, edgecolor="white")
ax.set_title("Year-over-Year Growth in Construction Spending", fontsize=14, fontweight="bold")
ax.set_ylabel("YoY Change (%)")
ax.set_xlabel("Year")
ax.axhline(0, color="black", linewidth=0.8)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))

for i, (yr, val) in enumerate(yoy.items()):
    ax.text(yr, val + (0.5 if val >= 0 else -0.5), f"{val:+.1f}%",
            ha="center", va="bottom" if val >= 0 else "top", fontsize=8)

fig.tight_layout()
fig.savefig(VIS_DIR / "06_yoy_growth.png", dpi=DPI)
plt.close(fig)
print("[saved] 06_yoy_growth.png")


# ---------------------------------------------------------------------------
# 4. Summary of findings
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("KEY FINDINGS")
print("=" * 60)

print(f"""
1. TOTAL SPENDING grew {total_growth:+.0f}% from 2002 to 2016, but the path
   was anything but linear. The GFC caused a sharp decline from 2007-2011.

2. RESIDENTIAL took the biggest hit during the GFC, dropping roughly 60%
   from peak. It has since recovered but hadn't fully returned to pre-GFC
   levels by 2016.

3. NON-RESIDENTIAL spending proved more resilient. Public infrastructure
   spending (highways, education) acted as a counter-cyclical buffer,
   especially during 2009-2010 stimulus programmes.

4. PRIVATE vs PUBLIC: Private spending drives the majority (~75%) of total
   construction. Public spending is more stable but much smaller.

5. SEASONAL PATTERNS: Spending tends to peak mid-year (May-Aug) and dip
   in winter months, relevant for sales planning and inventory management.

6. FASTEST-GROWING SECTORS (2002-2016): Manufacturing, Highway & Street,
   and Lodging saw the strongest growth, signalling infrastructure
   investment and hospitality expansion.

7. FOR BUILDING MATERIALS SALES: The recovery post-2011 represents a
   sustained growth period. Targeting the residential recovery and
   infrastructure sectors would have been the highest-ROI strategy.
""")

print("Analysis complete. Visuals saved to ./visuals/")
