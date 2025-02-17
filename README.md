# Singapore HDB Rentals

> **Note:** *Common terms used and their definitions.*
> - **SG:** Singapore
> - **HDB:** Housing Development Board (Singapore's public housing authority[^1] and colloquially refers to the public houses themselves).
> - **HDB Flat Types:** HDB apartments or flats, are split into various types indicating the number of rooms included.[^2]
> 
> **Data Source:** [HDB Renting Out of Flats 2024](https://data.gov.sg/datasets/d_c9f57187485a850908655db0e8cfe651/view)
---
**For those who are unable to preview the Jupyter notebook, please use the following links:**
- https://nbviewer.org/github/inezzie/sg_hdb_rentals/blob/main/sgmap.ipynb
- https://nbviewer.org/github/inezzie/sg_hdb_rentals/blob/main/predict.ipynb
---
This project looks at the HDB rental prices in Singapore from Jan-2021 to Nov-2024, the entire duration of data available from the government's official open data portal[^3]. This period happens to cover Singapore's Covid-19 response period up till the end of 2024.

During the Covid-19 pandemic, Singapore enacted the circuit breaker lockdown period[^4] which enforced stay-at-home measures which included deporting any foreigners found to be in non-compliance with safe distancing measures (e.g. throwing parties in large groups). This, along with majority of the foreign workforce returning to their home countries during the pandemic[^5], led to two possible outcomes for HDB rentals.

1. Rental prices will soar as demand lowers and supply doesn't differ whilst landlords aim to maintain profit.
2. Rental prices will drop as demand lowers and landlords attempt to maintain existing renters from leaving, or to entice new renters.

From the findings, it seems that scenario 1 was more likely as HDB rental prices continue to rise over time across all flat-types with no indicators of rental prices decreasing over time. While certain neighborhoods may see fluctuations in rental prices, we do not see that trend when looking at the average prices across flat-types and over time.

Additionally to the findings, a predictive model using SARIMA was used to estimate the overall average rental prices (regardless of flat-type). The predictive model was written with a lot (a large lot) of help from the very informative guide written by Tirthua Mutha on Medium[^6] which includes her very detailed GitHub repository[^7] used for the article. Much thanks to her for the guidance!

[^1]: About Singapore's HDB:<br>https://www.hdb.gov.sg/about-us
[^2]: HDB Types of Flats:<br>https://www.hdb.gov.sg/residential/buying-a-flat/finding-a-flat/types-of-flats
[^3]: Singapore Open Data Portal:<br>https://data.gov.sg
[^4]: Singapore's Covid-19 Response:<br>https://en.wikipedia.org/wiki/2020–21_Singapore_circuit_breaker_measures
[^5]: TODAY's new article on Singapores "Covid-19-induced foreigner exodus":<br>https://www.todayonline.com/big-read/big-read-short-after-exodus-will-foreigners-return-singapore-1802031
[^6] Time Series forecasting by Tirtha Mutha:<br>https://medium.com/@tirthamutha/time-series-forecasting-using-sarima-in-python-8b75cd3366f2
[^7] Time Series forecasting repository by Tirtha Mutha:<br>https://github.com/tirthamutha/repository/blob/main/TimeSeries.ipynb
