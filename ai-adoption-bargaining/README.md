# portfolio-personal-research

# AI Adoption and Collective Bargaining in Europe

## Question
Do EU countries with stronger collective bargaining coverage adopt AI more slowly or more quickly?

## Data
* **AI adoption:** Eurostat, table `isoc_eb_ai`. Indicator `E_AI_TANY` (firms using at least one AI technology), firms with 10+ employees, year 2025.
* **Bargaining coverage:** OECD/AIAS ICTWSS database, adjusted coverage rate (`AdjCov`). Latest available year per country, between 2021 and 2024.
* **GDP per capita:** Eurostat, table `nama_10_pc`, current prices, euro per capita, 2025.

## Methods
Data cleaning and merging with pandas, scatter plot, Pearson and Spearman correlations, simple OLS regression (statsmodels).

## Results

Across 19 EU countries, bargaining coverage is positively correlated with AI adoption (Pearson r = 0.60, Spearman rho = 0.53).

A simple OLS model gives a coefficient of 0.21 (p = 0.006, R² = 0.37). A 10-point increase in coverage is associated with a 2.1-point higher share of firms using AI.

This association mostly disappears once GDP per capita (2025, euros) is added. The coverage coefficient falls to 0.03 (p = 0.59), while GDP per capita is strongly significant (R² = 0.82).

Richer countries have both stronger bargaining coverage and higher AI adoption. With 19 countries, the data cannot rule out a small effect of coverage.

## Limitations
* Only 19 countries and one year of AI data.
* Coverage measures any collective agreement. It is not a measure of bargaining on AI.
* This is a descriptive association, not a causal effect. Wealth or digitalisation may explain both variables.
* Germany, Greece, Ireland, Luxembourg, Slovakia, Slovenia, Estonia and Latvia are excluded. They have no recent adjusted coverage data.
* Coverage years differ slightly across countries (2021 to 2024).

## Next steps
Add firm size and sector, control variables (GDP per capita), panel data and robustness checks in R.
