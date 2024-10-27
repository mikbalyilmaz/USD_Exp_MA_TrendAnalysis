# USD_Exp_MA_TrendAnalysis;

Let us now look at two built-inPython libraries. When it comes to financial data management, two of the most frequently used Python packages/libraries are Pandas as Numpy. A funciton can be easliy called only after we import the library. This is why the command for importing libraries is always put at the beginning of a script. To employ the pandas library, we it on the notebook. This line means that jupyter is told to import the pandas library and assigns it a short name, pd, for ease of reference. One of the first steps of every statistical analysis is importing the dataset to be analysed into the software. Depending on the format of the data there are different weys of accomplishing this task. This study conducts a comprehensive analysis of monthly USD/TRY and EUR/TRY exchange rates from Q1 2012 to October 2024. Data, acquired from the Turkish Central Bank’s EVDS database, consists of separate buying and selling rates, later averaged into a 'basket' rate for consistency. Initially, the analysis focuses on USD/TRY before moving to EUR/TRY in parallel, applying various time series methods to capture both trend and seasonality. The primary methodological framework includes Moving Averages and Smoothing Techniques, such as centered moving averages, simple exponential smoothing, and the Holt-Winters model. These techniques smooth the data, helping reveal trend and seasonal components effectively. Stationarity of the series is then assessed through the Augmented Dickey-Fuller (ADF) test, which identifies whether transformations, like differencing or logarithmic adjustments, are needed to stabilize mean and variance over time. Once stationarity is confirmed, Model Selection and Forecasting proceeds using both additive and multiplicative decompositions to select a model aligned with the data’s structure. Further, advanced forecasting models, including Holt's linear (two-parameter) and seasonal (three-parameter) adjustments, as well as exponential trend modeling, are applied. For series with substantial trend and seasonal components, Box-Jenkins ARMA modeling will enhance forecast precision. Autocorrelation Analysis through autocorrelation and partial autocorrelation functions (normalized via Bartlett’s correction) assesses whether trend components need to be removed. The theoretical basis for these methods rests on stochastic process principles, where a real-valued time series in probability space forms a stochastic process, a sequence of random variables evolving over time. Detailed mathematical formulations supporting each step will follow in later sections. Trend Component Analysis distinguishes between linear and nonlinear growth or decline over the long term, as expressed by the trend function. Seasonal Components are addressed by observing recurring patterns in monthly exchange rates. Additionally, Cyclical Components, characterized by longer-term fluctuations influenced by economic policies, are examined.

Warning: alis means buy, satis means sale.



---
avor exponential smoothing with 
, where a smaller 
 would ensure historical data are factored into future predictions with more significance than a larger 
.

It is evident that the usd_bask variable exhibits an exponential pattern. In this case, we will examine the presence of a trend, which could be seasonality or another type of distortion. Initially, it appears that the series has an exponential trend and unit root presence. The components forming the time series are Trend (T), Seasonal Change (M), Cyclical Movements (D), and Random Movements (R), with random change being an essential component. Time series can follow either an additive or multiplicative structure. Additive structure: 
; Multiplicative structure: 
. Stationarity is evaluated in two types. 5.2.1 Covariance Stationarity (Weak Stationarity): If the 1st and 2nd moments of the 
 series are independent of time 
, the process is called covariance stationary or weakly stationary. For weak stationarity: 
 and 
 must hold. Autocovariance: 
 must be independent of time difference 
 and 
 for all k; if so, the process is weakly stationary. Example: 
, where 
 is an independent process. Mean: 
 and autocovariance: 
, the process is covariance stationary. However, for 
, 
, indicating that the 1st moment is time-dependent, hence it is not covariance stationary. 5.2.2 Strong Stationarity: If the joint distributions of a time series are identical across different time periods, the process is called strongly stationary; in most applications, weak stationarity suffices. Trend Analysis: A linear trend model is suitable when the 
 series shows a constant increase or decrease, and the model is: 
, where 
 is the time variable (years, periods, etc.), and 
 and 
 are parameters. In the case of an exponential trend model, where 
 series changes at a constant percentage rate, the model is: 
. Taking the natural logarithm gives the log-linear form: 
; 
 represents the average growth rate.

Selection deleted
foreign_dataset['t'] = range(1, len(foreign_dataset) + 1)
foreign_dataset['log_usd_sepet'] = np.log(foreign_dataset['usd_sepet'])
X = foreign_dataset[['t']]
X = sm.add_constant(X)
y = foreign_dataset['log_usd_sepet']
model = sm.OLS(y, X).fit()
print(model.summary())
foreign_dataset['usd_sepet_pred'] = np.exp(model.predict(X))
print(foreign_dataset[['t', 'usd_sepet', 'usd_sepet_pred']].head())
                            OLS Regression Results                            
==============================================================================
Dep. Variable:          log_usd_sepet   R-squared:                       0.945
Model:                            OLS   Adj. R-squared:                  0.945
Method:                 Least Squares   F-statistic:                     2566.
Date:                Mon, 28 Oct 2024   Prob (F-statistic):           8.14e-96
Time:                        00:53:58   Log-Likelihood:                 20.200
No. Observations:                 151   AIC:                            -36.40
Df Residuals:                     149   BIC:                            -30.36
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
const          0.1780      0.035      5.106      0.000       0.109       0.247
t              0.0202      0.000     50.658      0.000       0.019       0.021
==============================================================================
Omnibus:                       42.797   Durbin-Watson:                   0.040
Prob(Omnibus):                  0.000   Jarque-Bera (JB):                8.976
Skew:                           0.206   Prob(JB):                       0.0112
Kurtosis:                       1.879   Cond. No.                         176.
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
            t  usd_sepet  usd_sepet_pred
date                                    
2012-04-01  1   1.784130        1.219114
2012-05-01  2   1.801291        1.243933
2012-06-01  3   1.820452        1.269256
2012-07-01  4   1.809239        1.295095
2012-08-01  5   1.790140        1.321460
---

Last observed value of usd_sepet: 34.20USD/TRY
Last estimated value of MA usd_sepet: 33.93USD/TRY

The project is not over..
