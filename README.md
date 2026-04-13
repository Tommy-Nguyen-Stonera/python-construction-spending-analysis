# US Construction Spending Analysis (Python)

[View Interactive Report](https://htmlpreview.github.io/?https://raw.githubusercontent.com/Tommy-Nguyen-Stonera/python-construction-spending-analysis/main/report.html)

## Overview

This project analyses 14 years of monthly US construction spending data to understand how different sectors responded to the GFC and the long recovery that followed. It separates private from public spending and tracks which sectors grew or contracted across the full 2002 to 2016 period.

## Dataset

- Source: US Census Bureau construction spending data
- Record count: Monthly observations from 2002 to 2016 (approximately 168 months)
- Key columns: Date, current.combined.total, residential, commercial, manufacturing, healthcare, public, and other sector breakdowns
- Single flat table, no joins required

## Research Questions

1. What is the overall growth trajectory for total construction spending from 2002 to 2016?
2. How did the GFC affect residential vs commercial spending differently in terms of depth and timing?
3. Is private or public spending more sensitive to economic cycles, and by how much?
4. Which individual sectors grew the most over the full period?
5. What seasonal patterns exist in national construction spending data?
6. How does the year-over-year growth rate vary across different phases of the period?

## Data Model

Single flat table: construction_spending. Each row is one monthly observation with spending broken down across multiple sector columns. All analysis is done through Pandas aggregations and time-series operations on this one table.

## What Was Analysed

- Total spending trend from 2002 to 2016 with overall growth calculation
- Residential vs commercial GFC drawdown comparison (timing, depth, and recovery pace)
- Private vs public spending volatility across the full period
- Sector-level growth ranking from 2002 to 2016
- Monthly seasonal index tested across the full dataset
- Year-over-year growth rate charted across the pre-GFC, crash, and recovery phases

## Key Insights

1. Total spending grew approximately 30% over the period, but the path included a severe GFC collapse and a slow, uneven recovery that stretched across most of the back half of the dataset.
2. Residential spending crashed hardest and earliest during the GFC, and was the slowest sector to recover, lagging commercial by several years.
3. Private spending is far more volatile than public spending across economic cycles. Public construction held up relatively well through the GFC, acting as a partial offset to the private collapse.
4. Manufacturing and healthcare were the standout growth sectors over the full period, both recovering faster and growing past pre-GFC peaks while residential was still recovering.
5. Seasonal patterns in national construction data are weaker than expected. The macro-level aggregation smooths out regional seasonality, making month-to-month variation a poor signal at this level.
6. The steepest year-over-year growth rates cluster in the 2012 to 2015 recovery window, which was also the period of greatest divergence between fast-recovering sectors and lagging residential.

## Recommendations

1. Build residential exposure as a lagging indicator into demand planning. It is the last sector to recover after a downturn, which means the recovery signal in residential is a confirmation, not an early warning.
2. Use public construction spending as a stability anchor when modelling downside scenarios. Its relative flatness through the GFC shows it is far less sensitive to credit conditions than private construction.
3. Weight manufacturing and healthcare as growth sectors when prioritising customer acquisition. Both outperformed on recovery and continued growing past pre-GFC baseline within this period.
4. Do not rely on seasonal patterns to drive short-term demand forecasting at a national level. The macro aggregation masks regional seasonality, making it an unreliable guide for operational decisions.

## Tools

Python 3.12, Pandas, Matplotlib, Seaborn

## Files

- `analysis.py` - Full analysis script
- `report.html` - Interactive report with 6 embedded charts
- `construction_spending.csv` - Source dataset
- `visuals/` - 6 chart PNGs
