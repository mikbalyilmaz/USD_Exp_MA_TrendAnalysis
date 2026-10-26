# Changes

## Version 2.0.0

### New

- `usdtrend/` holds the data loading and the methods; three analysis scripts, unit tests, CSV tables, figures in the
  style of muhammedikbalyilmaz.com and a project note whose numbers are written from the tables.
- Data updated to September 2026 from EVDS (monthly averages of the CBRT indicative rates) and extended back to
  January 2012.
- The exponential trend is judged by its residuals (Durbin–Watson, autocorrelation, ADF), not by $R^2$.
- Seasonality is tested (F test of month dummies, Kruskal–Wallis) before any seasonal method is used.
- The trend methods are compared on months they were not fitted on (expanding window, 1, 3 and 12 months ahead).

### Corrections to version 1

| # | Version 1 | Version 2 |
|---|---|---|
| 1 | The README said the data run from the first quarter of 2012 to October 2024. | The file of version 1 starts in April 2012. Version 2 uses January 2012 to September 2026. |
| 2 | Six months of version 1's file differ from the current EVDS monthly averages: 2017-08, 2017-09, 2018-01, 2018-04, 2018-05 and 2024-10 (USD buying rate in October 2024: 34.168 against 34.171). | The October 2024 value was probably taken before the month ended; the cause for the other five is not known. Version 2 uses the EVDS values throughout. |
| 3 | The README listed Holt-Winters, decomposition, ADF, ARMA, ACF/PACF and Bartlett bounds. | The notebook contained simple exponential smoothing, an exponential trend and a 3-month moving average only. The README of version 2 lists only what the code does (Holt-Winters, the seasonality tests and ADF are implemented; ARMA and ACF/PACF are not part of this exercise). |
| 4 | The 3-month moving average was described as centred. | It was trailing (centred one month earlier). Version 2 uses the 2 × 12 centred average for the trend. |
| 5 | The band around the smoothed series was ± one standard deviation of the smoothed levels and was read as a confidence band. | That is not a confidence band. Version 2 does not draw it; uncertainty is measured by forecast errors on new months. |
| 6 | The exponential trend was judged by $R^2$ = 0.945. | On the version 2 data the residuals have a first autocorrelation of 0.98 (USD) and the Durbin–Watson statistic is 0.033; on new months the trend has the largest forecast errors. |
| 7 | One cell used a variable (`foreign_dataset`) before it was defined, so the notebook did not run from top to bottom. | Every script runs from a clean start; `tests/run_tests.py` reproduces version 1's numbers from its own file. |
| 8 | A cell derived the moving-average process MA(1). | A moving-average process MA(q) and a moving-average smoother are different things; version 2 uses only the smoother. |
