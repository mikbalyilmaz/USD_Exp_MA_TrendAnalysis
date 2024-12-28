# USD_Exp_MA_TrendAnalysis;

Let us now look at two built-inPython libraries. When it comes to financial data management, two of the most frequently used Python packages/libraries are Pandas as Numpy. A funciton can be easliy called only after we import the library. This is why the command for importing libraries is always put at the beginning of a script. To employ the pandas library, we it on the notebook. This line means that jupyter is told to import the pandas library and assigns it a short name, pd, for ease of reference. One of the first steps of every statistical analysis is importing the dataset to be analysed into the software. Depending on the format of the data there are different weys of accomplishing this task. This study conducts a comprehensive analysis of monthly USD/TRY and EUR/TRY exchange rates from Q1 2012 to October 2024. Data, acquired from the Turkish Central Bank’s EVDS database, consists of separate buying and selling rates, later averaged into a 'basket' rate for consistency. Initially, the analysis focuses on USD/TRY before moving to EUR/TRY in parallel, applying various time series methods to capture both trend and seasonality. The primary methodological framework includes Moving Averages and Smoothing Techniques, such as centered moving averages, simple exponential smoothing, and the Holt-Winters model. These techniques smooth the data, helping reveal trend and seasonal components effectively. Stationarity of the series is then assessed through the Augmented Dickey-Fuller (ADF) test, which identifies whether transformations, like differencing or logarithmic adjustments, are needed to stabilize mean and variance over time. Once stationarity is confirmed, Model Selection and Forecasting proceeds using both additive and multiplicative decompositions to select a model aligned with the data’s structure. Further, advanced forecasting models, including Holt's linear (two-parameter) and seasonal (three-parameter) adjustments, as well as exponential trend modeling, are applied. For series with substantial trend and seasonal components, Box-Jenkins ARMA modeling will enhance forecast precision. Autocorrelation Analysis through autocorrelation and partial autocorrelation functions (normalized via Bartlett’s correction) assesses whether trend components need to be removed. The theoretical basis for these methods rests on stochastic process principles, where a real-valued time series in probability space forms a stochastic process, a sequence of random variables evolving over time. Detailed mathematical formulations supporting each step will follow in later sections. Trend Component Analysis distinguishes between linear and nonlinear growth or decline over the long term, as expressed by the trend function. Seasonal Components are addressed by observing recurring patterns in monthly exchange rates. Additionally, Cyclical Components, characterized by longer-term fluctuations influenced by economic policies, are examined.

Warning: 'alis' means 'buy', 'satis' means 'sale'.



---
The analysis of the `usd_bask` variable reveals an exponential pattern, prompting an investigation into the presence of a trend, which may include seasonality or other distortions. Initial observations suggest that the series demonstrates an exponential trend and the presence of a unit root. The primary components of a time series are:

- **Trend (T):** The long-term movement in the data.
- **Seasonal Change (M):** Repeating patterns at fixed intervals.
- **Cyclical Movements (D):** Fluctuations over longer periods.
- **Random Movements (R):** Irregular, unpredictable variations.

A time series can follow an **additive** or **multiplicative** structure:

- **Additive Structure:**
  \[ Y_t = T_t + M_t + D_t + R_t \]
- **Multiplicative Structure:**
  \[ Y_t = T_t \times M_t \times D_t \times R_t \]

**Stationarity in Time Series:**
Stationarity is classified into two main types:

### 1. Covariance Stationarity (Weak Stationarity):
A time series is covariance stationary if its first and second moments are time-independent. For weak stationarity, the following conditions must hold:

\[ E(Y_t) = \mu \] (Constant mean)
\[ Var(Y_t) = \sigma^2 \] (Constant variance)
\[ Cov(Y_t, Y_{t-k}) = \gamma_k \] (Autocovariance depends only on lag \(k\), not time \(t\))

Example:
Let \( Y_t = \epsilon_t + \alpha \epsilon_{t-1} \), where \( \epsilon_t \) is white noise with mean \( 0 \) and variance \( \sigma^2 \). Then:

- Mean: \( E(Y_t) = 0 \)
- Autocovariance: \( \gamma_k = \alpha^k \sigma^2 \) for all \(k\)

If \( Y_t = t \epsilon_t \), the mean and variance become time-dependent, violating weak stationarity.

### 2. Strong Stationarity:
A time series is strongly stationary if its joint distributions remain constant across time. In most applications, weak stationarity suffices.

**Trend Analysis:**
When analyzing trends, a linear model is appropriate if the series exhibits a constant rate of change:
\[ Y_t = \beta_0 + \beta_1 t + \epsilon_t \]
where \( t \) is time and \( \beta_0 \), \( \beta_1 \) are parameters.

For exponential growth:
\[ Y_t = \beta_0 e^{\beta_1 t} \]
Taking the natural logarithm yields:
\[ \ln(Y_t) = \ln(\beta_0) + \beta_1 t \]
Here, \( \beta_1 \) represents the average growth rate.

**Empirical Analysis:**
The following Python script was employed to fit a log-linear trend model to the `usd_sepet` series:

```
python
foreign_dataset['t'] = range(1, len(foreign_dataset) + 1)
foreign_dataset['log_usd_sepet'] = np.log(foreign_dataset['usd_sepet'])
X = foreign_dataset[['t']]
X = sm.add_constant(X)
y = foreign_dataset['log_usd_sepet']
model = sm.OLS(y, X).fit()
print(model.summary())
foreign_dataset['usd_sepet_pred'] = np.exp(model.predict(X))
print(foreign_dataset[['t', 'usd_sepet', 'usd_sepet_pred']].head())
```

### Model Results:

**OLS Regression Results:**

- **Dependent Variable:** `log_usd_sepet`
- **R-squared:** 0.945
- **Adj. R-squared:** 0.945
- **F-statistic:** 2566
- **Prob (F-statistic):** \( 8.14 \times 10^{-96} \)
- **Number of Observations:** 151
- **AIC:** -36.40
- **BIC:** -30.36

**Coefficients:**
\[ \text{const} = 0.1780, \; \text{t} = 0.0202 \]
Both coefficients are statistically significant (\( p < 0.000 \)), suggesting a robust log-linear relationship.

### Interpretation:
1. The positive \( t \) coefficient (0.0202) implies an average growth rate of approximately 2.02% per unit time.
2. The high R-squared (0.945) indicates that the model explains 94.5% of the variance in the log-transformed series.

### Observed vs. Predicted Values:
| Time (t) | Observed USD Basket | Predicted USD Basket |
|----------|---------------------|-----------------------|
| 1        | 1.784              | 1.219                |
| 2        | 1.801              | 1.244                |
| 3        | 1.820              | 1.269                |
| 4        | 1.809              | 1.295                |
| 5        | 1.790              | 1.321                |

### Recent Values:
- **Last observed value:** 34.20 USD/TRY
- **Last estimated value:** 33.93 USD/TRY

### Conclusion:
The analysis confirms the presence of a significant exponential trend in the `usd_sepet` series. The model’s predictions align closely with observed values, indicating its reliability. Further analysis will incorporate seasonality and cyclicality to refine the forecasting accuracy. This project remains ongoing, with potential enhancements in structural modeling and diagnostics.


